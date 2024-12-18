import subprocess
import requests
import os
import zipfile

def get_chrome_version():   #    Get the Chrome browser version installed on Windows.
    try:
        output = subprocess.check_output(
            r'reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version',
            shell=True,
            encoding='utf-8'
        )
        # Extract version from the command output
        version = output.split()[-1]
        print(f"Chrome Version: {version}")
        return version

    except Exception as e:
        print(f"Error getting Chrome version: {e}")
        return None

def get_chrome_driver_download_url(chrome_version):
    """Get the download URL for the ChromeDriver matching the Chrome version."""
    download_url = f"https://storage.googleapis.com/chrome-for-testing-public/{chrome_version}/win64/chromedriver-win64.zip"
    print(f"Download URL: {download_url}")
    response = requests.head(download_url)

    if response.status_code == 200:
        return download_url
    else:
        raise Exception(f"Failed to get ChromeDriver version for Chrome {chrome_version}")

def download_and_extract_chromedriver(download_url, extract_dir=".//dependencies//chrome-driver"):
    """Download and extract the ChromeDriver zip file."""
    try:
        response = requests.get(download_url, stream=True)
        if response.status_code == 200:
            zip_path = "chromedriver.zip"

            with open(zip_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)

            print(f"Downloaded ChromeDriver zip: {zip_path}")

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
                print(f"Extracted ChromeDriver to: {extract_dir}")

            os.remove(zip_path)

            print(f"ChromeDriver is ready at {extract_dir}\\chromedriver.exe")
            return True

        else:
            raise Exception(f"Failed to download ChromeDriver from {download_url}")

    except Exception as e:
        print(f"Error downloading ChromeDriver: {e}")
        return False


if __name__ == "__main__":
    # Get Chrome version
    chrome_version = get_chrome_version()
    if not chrome_version:
        print("Failed to get Chrome version.")
        exit(1)

    # Get ChromeDriver download URL
    download_url = get_chrome_driver_download_url(chrome_version)
    if not download_url:
        print("Failed to get ChromeDriver download URL.")
        exit(1)

    # Download and extract ChromeDriver
    success = download_and_extract_chromedriver(download_url)
    if success:
        print("ChromeDriver is set up successfully!")
    else:
        print("Failed to set up ChromeDriver.")

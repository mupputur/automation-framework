import subprocess
import requests
import os
import zipfile

class BrowserManager:
    def __init__(self,extract_dir=".//dependencies//chrome-driver"):
        self.extract_dir = extract_dir
    def get_chrome_version(self):   #    Get the Chrome browser version installed on Windows.
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
            raise Exception(f"Error getting Chrome version: {e}")

    def get_chrome_driver_download_url(self, chrome_version):
        try:
            if not chrome_version:
                raise Exception("Chrome version is required to fetch the download URL.")

            download_url = f"https://storage.googleapis.com/chrome-for-testing-public/{chrome_version}/win64/chromedriver-win64.zip"
            print(f"Download URL: {download_url}")

            response = requests.head(download_url)

            if response.status_code != 200:
                raise Exception(
                    f"Failed to get ChromeDriver for Chrome {chrome_version}. HTTP Status Code: {response.status_code}")

            return download_url
        except Exception as e:
            raise Exception(f"Error getting ChromeDriver download URL: {e}")

    def download_and_extract_chromedriver(self,download_url):
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
                    zip_ref.extractall(self.extract_dir)
                    print(f"Extracted ChromeDriver to: {self.extract_dir}")

                os.remove(zip_path)

                print(f"ChromeDriver is ready at {self.extract_dir}\\chromedriver.exe")
                return True

            else:
                raise Exception(f"Failed to download ChromeDriver from {download_url}")

        except Exception as e:
            print(f"Error downloading ChromeDriver: {e}")
            return False


if __name__ == "__main__":
    manager = BrowserManager()
    # Get Chrome version
    chrome_version = manager.get_chrome_version()
    if not chrome_version:
        print("Failed to get Chrome version.")
        exit(1)

        # Get ChromeDriver download URL
    download_url = manager.get_chrome_driver_download_url(chrome_version)
    if not download_url:
        print("Failed to get ChromeDriver download URL.")
        exit(1)

        # Download and extract ChromeDriver
    success = manager.download_and_extract_chromedriver(download_url)
    if success:
        print("ChromeDriver is set up successfully!")
    else:
        print("Failed to set up ChromeDriver.")
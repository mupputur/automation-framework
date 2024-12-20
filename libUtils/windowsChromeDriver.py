import subprocess
import requests
import os
import zipfile
import platform

class BrowserManager:

    def __init__(self):
        self.driver_path = ".//dependencies//chrome-driver"
        # self.base_url = f"https://storage.googleapis.com/chrome-for-testing-public/{chrome_version}/win64/chromedriver-win64.zip"
        self.reg_path = r'reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version'

    def get_chrome_version(self):   #Get the Chrome browser version installed on Windows.
        try:
            output = subprocess.check_output(self.reg_path, shell=True, encoding='utf-8')
            # Extract version from the command output
            version = output.split()[-1]
            print(f"Chrome Version: {version}")
            return version
        except Exception as e:
            print( f"Failed to read chrome browser version from path: {self.reg_path}")
            raise Exception(f"Failed to get chrome browser version. Error: {e}")

    def get_driver_url(self,chrome_version):
        try:
            architecture = 'win64' if platform.architecture()[0] == '64bit' else 'win32'
            print(architecture)
            download_url = f"https://storage.googleapis.com/chrome-for-testing-public/{chrome_version}/{architecture}/chromedriver-{architecture}.zip"
            print(f"Chrome Driver Download URL: {download_url}")

            response = requests.head(download_url)
            if response.status_code != 200:
                raise Exception(f"Failed to get ChromeDriver for Chrome {chrome_version}.")
            return download_url
        except Exception as e:
            raise Exception(f"Error getting ChromeDriver download URL: {e}")

    def download_zip_file(self, download_url):
        try:
            response = requests.get(download_url, stream=True)
            if response.status_code == 200:
                zip_path = "chromedriver.zip"

                with open(zip_path, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)

                print(f"Downloaded ChromeDriver zip: {zip_path}")
                return zip_path
            else:
                raise Exception(f"Failed to download ChromeDriver from {download_url}")
        except Exception as e:
            print(f"Error downloading ChromeDriver: {e}")
            return None

    def extract_zipfile(self, zip_path):
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(self.driver_path)
                print(f"Extracted ChromeDriver to: {self.driver_path}")

            os.remove(zip_path)
            print(f"ChromeDriver is ready at {self.driver_path}\\chromedriver.exe")
            return True

        except Exception as e:
            print(f"Error extracting ChromeDriver: {e}")
            return False


if __name__ == "__main__":
    manager = BrowserManager()

    # Get Chrome version
    chrome_version = manager.get_chrome_version()
    if not chrome_version:
        print("Failed to get Chrome version.")
        exit(1)

    # Get ChromeDriver download URL
    download_url = manager.get_driver_url(chrome_version)
    if not download_url:  # Fixed this line
        print("Failed to get ChromeDriver download URL.")
        exit(1)

    # Download ChromeDriver zip file
    zip_path = manager.download_zip_file(download_url)
    if zip_path:
        success = manager.extract_zipfile(zip_path)
        if success:
            print("ChromeDriver is set up successfully!")
        else:
            print("Failed to extract ChromeDriver.")
    else:
        print("Failed to download ChromeDriver.")

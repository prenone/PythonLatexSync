import requests
import uuid
import os

class PLS:
    def __init__(self, user, write_password, read_password, server_url):
        self.user = user
        self.write_password = write_password
        self.read_password = read_password
        self.server_url = server_url

    def push_txt_str(self, filename, text):
        tmp_filename = uuid.uuid4() + ".txt"
        with open(tmp_filename, 'w') as f:
            f.write(text)
        self.push(filename, tmp_filename)
        os.remove(tmp_filename)

    def push(self, filename, path=None):
        if path is None:
            path = filename

        url = f"{self.server_url}/push/{self.user}/{self.write_password}/{filename}"
        files = {'file': open(path, 'rb')}

        try:
            response = requests.post(url, files=files)
            response.raise_for_status()

            download_url = f"{self.server_url}/pull/{self.user}/{self.read_password}/{filename}"
            print(f"The file can be retrieved using the following URL:\n{download_url}")

        except requests.exceptions.RequestException as e:
            print(f"Failed to upload file '{filename}': {e}")

    def pull(self, filename, destination):
        url = f"{self.server_url}/pull/{self.user}/{self.read_password}/{filename}"
    
        try:
            response = requests.get(url)
            response.raise_for_status()

            with open(destination, 'wb') as file:
                file.write(response.content)

            print(f"File '{filename}' has been successfully downloaded to '{destination}'.")

        except requests.exceptions.RequestException as e:
            print(f"Failed to download file '{filename}': {e}")


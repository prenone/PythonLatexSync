import requests

class PLS:
    def __init__(self, user, write_password, read_password, server_url='http://127.0.0.1:5000'):
        self.user = user
        self.write_password = write_password
        self.read_password = read_password
        self.server_url = server_url

    def push(self, filename):
        url = f"{self.server_url}/push/{self.user}/{self.write_password}/{filename}"
        files = {'file': open(filename, 'rb')}
        
        try:
            response = requests.post(url, files=files)
            response.raise_for_status()

            download_url = f"{self.server_url}/pull/{self.user}/{self.read_password}/{filename}"
            print(f"The file can be retrieved using the following URL:\n{download_url}")
            
        except requests.exceptions.RequestException as e:
            print(f"Failed to upload file '{filename}': {e}")


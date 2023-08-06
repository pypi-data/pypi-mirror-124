from ftplib import FTP

from brsus.interfaces.dataset import DatasetInterface


class FTPWrapper:
    def __init__(self, url: str, dataset: DatasetInterface):
        self.url = url
        self.ftp = FTP(url)
        self.ftp.login()
        self.dataset = dataset

    def download(self):
        cwd, file_name = self.dataset.cwd_and_file_name()
        self.ftp.cwd(cwd)

        with open(file_name, "wb") as f:
            self.ftp.retrbinary(f"RETR {file_name}", f.write)

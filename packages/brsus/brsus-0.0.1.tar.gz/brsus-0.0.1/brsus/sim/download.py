from brsus import DATASUS_FTP_SERVER
from brsus.sim.dataset import DatasetSIM
from brsus.toolbox.ftp import FTPWrapper


def download(state: str, year: int) -> None:
    dataset = DatasetSIM(state, year)
    ftp_server = FTPWrapper(url=DATASUS_FTP_SERVER, dataset=dataset)
    ftp_server.download()


if __name__ == "__main__":
    download("SP", 2018)

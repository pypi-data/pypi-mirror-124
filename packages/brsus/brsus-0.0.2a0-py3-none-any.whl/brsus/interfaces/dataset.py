from abc import ABC, abstractclassmethod
from typing import Tuple


class DatasetInterface(ABC):
    @abstractclassmethod
    def cwd_and_file_name(self) -> Tuple[str, str]:
        raise NotImplementedError("Method not implemented yet.")

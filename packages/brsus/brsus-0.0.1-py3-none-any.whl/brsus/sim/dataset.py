from collections import OrderedDict
from enum import Enum
from typing import Dict, Tuple

from brsus.interfaces.dataset import DatasetInterface


class CIDS(Enum):
    CID10: str = "CID10"
    CID9: str = "CID9"


CID_PATTERNS: Dict = {
    CIDS.CID10: OrderedDict(
        file_pattern=lambda state, year: f"DO{state}{year}.DBC",
        cwd_pattern="/dissemin/publicos/SIM/CID10/DORES",
    ),
    CIDS.CID9: OrderedDict(
        file_pattern=lambda state, year: f"DOR{state}{str(year)[-2:].zfill(2)}.DBC",
        cwd_pattern="/dissemin/publicos/SIM/CID9/DORES",
    ),
}


class DatasetSIM(DatasetInterface):
    def __init__(self, state: str, year: int):
        self.state = state.upper()
        self.year = year
        self.cwd, self.file_name = self.cwd_and_file_name()

    @property
    def _cid(self):
        if self.year <= 1996:
            return CIDS.CID9
        return CIDS.CID10

    def cwd_and_file_name(self) -> Tuple[str, str]:
        return (
            CID_PATTERNS[self._cid]["cwd_pattern"],
            CID_PATTERNS[self._cid]["file_pattern"](self.state, self.year),
        )

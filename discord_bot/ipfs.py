from pinatapy import PinataPy

import typing as tp

from .config.config import PINATA_PUBLIC, PINATA_SECRET
from .utils import to_thread

class IPFSPinner:
    def __init__(self) -> None:
        self.pinata = PinataPy(PINATA_PUBLIC, PINATA_SECRET)
    
    @to_thread
    def pin(self, data: tp.Dict[str, str]) -> str:
        ipfs_hash = self.pinata.pin_json_to_ipfs(data)
        return ipfs_hash
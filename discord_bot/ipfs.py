from pinatapy import PinataPy

import typing as tp

from .config.config import PINATA_PUBLIC, PINATA_SECRET
from .utils import to_thread
from .logger import get_logger

logger = get_logger(__name__)

class IPFSPinner:
    def __init__(self) -> None:
        self.pinata = PinataPy(PINATA_PUBLIC, PINATA_SECRET)
    
    @to_thread
    def pin(self, data: tp.Dict[str, str]) -> str:
        logger.info("Start pinning data to pinata")
        ipfs_hash = self.pinata.pin_json_to_ipfs(data)
        logger.info(f"Data pinned to pinata with hash: {ipfs_hash}")
        return ipfs_hash.get("IpfsHash")
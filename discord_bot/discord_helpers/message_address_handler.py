from discord import Message
from substrateinterface.utils.ss58 import is_valid_ss58_address
import typing as tp

from ..exceptions.message_exceptions import AddressIsInWrongFormat, AddressIsNotED25519, NoAddressInMessage
from ..utils import try_to_encrypt

from ..logger import get_logger

logger = get_logger(__name__)

class MessageWithAddressHandler:
    def __init__(self, message: Message) -> None:
        self.message: Message = message

    def get_address(self) -> str:
        address = self._find_address()
        self._check_address_format(address)
        self._check_address_type(address)
        return address
    
    def _find_address(self) -> tp.Optional[str]:
        words = str(self.message.content).split()
        for word in words:
            word = word.strip()
            if is_valid_ss58_address(word):
                return word
        else:
            logger.info(f"Message {self.message.content} from {self.message.author} does't content address")
            raise NoAddressInMessage
        
    def _check_address_format(self, address: str) -> None:
        if not is_valid_ss58_address(address, valid_ss58_format=32):
            raise AddressIsInWrongFormat
        
    def _check_address_type(self, address: str) -> None:
        res = try_to_encrypt(address)
        if not res:
            raise AddressIsNotED25519
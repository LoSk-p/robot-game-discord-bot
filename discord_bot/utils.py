import asyncio
import typing as tp
import functools
from substrateinterface import Keypair, KeypairType
from robonomicsinterface import Account
import os

from .logger import get_logger

logger = get_logger(__name__)

RELATIVE_PATH_TO_UNUSED_SEEDS = "data/unused_seeds.json"
RELATIVE_PATH_TO_USED_SEEDS = "data/used_seeds.json"

def to_thread(func: tp.Callable) -> tp.Coroutine:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        return await asyncio.to_thread(func, *args, **kwargs)

    return wrapper

def get_path_to_unused_seeds() -> str:
    path_here = os.path.realpath(__file__)
    filename = path_here.split("/")[-1]
    path_to_seeds = path_here.replace(filename, RELATIVE_PATH_TO_UNUSED_SEEDS)
    return path_to_seeds

def get_path_to_used_seeds() -> str:
    path_here = os.path.realpath(__file__)
    filename = path_here.split("/")[-1]
    path_to_seeds = path_here.replace(filename, RELATIVE_PATH_TO_USED_SEEDS)
    return path_to_seeds


def encrypt_message_for_devices(data: str, sender_keypair: Keypair, recepient_addresses: tp.List[str]) -> tp.Dict[str, str]:
    try:
        random_seed = Keypair.generate_mnemonic()
        random_acc = Account(random_seed, crypto_type=KeypairType.ED25519)
        encrypted_data = _encrypt_message(data, sender_keypair, random_acc.keypair.public_key)
        encrypted_keys = {}
        for device in recepient_addresses:
            try:
                receiver_kp = Keypair(ss58_address=device, crypto_type=KeypairType.ED25519)
                encrypted_key = _encrypt_message(random_seed, sender_keypair, receiver_kp.public_key)
                encrypted_keys[device] = encrypted_key
            except Exception as e:
                logger.info(f"Faild to encrypt key for: {device} with error: {e}. Check your RWS devices, you may have SR25519 address in devices.")
        data_final = {"encrypted_keys": encrypted_keys, "data": encrypted_data}
        return data_final
    except Exception as e:
        logger.info(f"Exception in encrypt for devices: {e}")

def try_to_encrypt(receiver_address: str) -> bool:
    random_seed = Keypair.generate_mnemonic()
    random_acc = Account(random_seed, crypto_type=KeypairType.ED25519)
    receiver_kp = Keypair(ss58_address=receiver_address, crypto_type=KeypairType.ED25519)
    test_data = "test data"
    try:
        _encrypt_message(test_data, random_acc.keypair, receiver_kp.public_key)
        return True
    except Exception as e:
        logger.info(f"Can't encrypt test message with error: {e}")
        return False

def _encrypt_message(message: tp.Union[bytes, str], sender_keypair: Keypair, recipient_public_key: bytes) -> str:
    encrypted = sender_keypair.encrypt_message(message, recipient_public_key)
    return f"0x{encrypted.hex()}"


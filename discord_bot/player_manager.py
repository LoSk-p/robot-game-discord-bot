import typing as tp

from .models.player import Player
from .exceptions.players_exceptions import TooManyPlayers
from .config.config import MAX_PLAYERS_COUNT

from .logger import get_logger

logger = get_logger(__name__)


class PlayersManager:
    def __init__(self):
        self.players_list: tp.List[Player] = []

    def add_player(self, discord_acc_name: str, robonomics_address: str) -> None:
        if len(self.players_list) == MAX_PLAYERS_COUNT:
            raise TooManyPlayers
        self.players_list.append(Player(discord_acc_name, robonomics_address))
        logger.info(f"Address {robonomics_address} from user {discord_acc_name} wass added to players")

    def get_players_addresses(self) -> tp.List[str]:
        addresses = []
        for player in self.players_list:
            addresses.append(player.robonomics_address)
        return addresses
    
    def get_player_for_address(self, address: str) -> tp.Optional[Player]:
        for player in self.players_list:
            if player.robonomics_address == address:
                return player
    
    def clear_players(self) -> None:
        logger.info("Clear players list")
        self.players_list.clear()

    def discord_acc_in_players(self, discord_acc_name: str) -> bool:
        for player in self.players_list:
            if discord_acc_name == player.discord_account_name:
                return True
        else:
            return False

    @property
    def empty(self) -> bool:
        return len(self.players_list) == 0

    @property
    def full(self) -> bool:
        return len(self.players_list) >= MAX_PLAYERS_COUNT

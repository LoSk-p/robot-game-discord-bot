import typing as tp
from discord import User, Member

from .models.player import Player
from .exceptions.players_exceptions import TooManyPlayers
from .config.config import MAX_PLAYERS_COUNT


class PlayersManager:
    def __init__(self):
        self.players_list: tp.List[Player] = []

    def add_player(self, discord_acc: tp.Union[User, Member], robonomics_address: str) -> None:
        if len(self.players_list) == MAX_PLAYERS_COUNT:
            raise TooManyPlayers
        self.players_list.append(Player(discord_acc, robonomics_address))
        print(f"Address {robonomics_address} from user {discord_acc} wass added to players")

    def get_players(self) -> tp.List[Player]:
        return self.players_list.copy()
    
    def get_player_for_address(self, address: str) -> tp.Optional[Player]:
        for player in self.players_list:
            if player.robonomics_address == address:
                return player
    
    def clear_players(self) -> None:
        self.players_list.clear()

    def discord_acc_in_players(self, discord_acc: tp.Union[User, Member]) -> bool:
        for player in self.players_list:
            if discord_acc == player.discord_account:
                return True
        else:
            return False

    @property
    def empty(self) -> bool:
        return len(self.players_list) == 0

    @property
    def full(self) -> bool:
        return self.players_list >= MAX_PLAYERS_COUNT

from discord import Message, User, Member
import typing as tp

from ..models.player import Player

class MessageManager:

    @staticmethod
    def wrong_format_message(address: str, message: Message) -> str:
        return f"Address {address} from {message.author} has wrong format."
    
    @staticmethod
    def wrong_type_message(address: str, message: Message) -> str:
        return f"Address {address} from {message.author} has wrong type. Please, use only addresses with ED25519 type."
    
    @staticmethod
    def start_round_message() -> str:
        return "Round is starting, присылайте адреса"
    
    @staticmethod
    def winner_message(address: str, author: str) -> str:
        return f"Address {address} from {author} has winned this round."
    
    @staticmethod
    def second_address_from_one_user(user: tp.Union[User, Member]) -> str:
        return "One address from one user in this round"
    
    @staticmethod
    def message_with_dapp() -> str:
        return "Робот закончил, можете идти отсматривать дапп (и ссылка)"
    
    def message_with_winner(winner_player: Player) -> str:
        return f"The winner of this round is {winner_player.discord_account.name}, with address {winner_player.robonomics_address}"
import typing as tp
from discord import User, Member

class Player:
    def __init__(self, discord_account: tp.Union[User, Member], robonomics_address: str):
        self.discord_account = discord_account
        self.robonomics_address = robonomics_address
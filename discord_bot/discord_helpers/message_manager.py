import typing as tp

from discord import Member, Message, User


class MessageManager:

    @staticmethod
    def wrong_format_message(message: Message) -> str:
        return f"Address from {message.author} has wrong format."

    @staticmethod
    def wrong_type_message(message: Message) -> str:
        return f"Address from {message.author} has wrong type. Please, use only addresses with ED25519 type."

    @staticmethod
    def start_round_message() -> str:
        return """Hey there, hackers, @everyone! Just so you know, the gathering of addresses for a friendly hack into Johnny's laboratory has begun. The addresses we get in ED25519 format will be given the green light to take a peek at the lab logs.\n \nThe rulebook for this hacking showdown can be found right over at this link: https://robonomics.network/blog/robonomics-school-2024-hack-johnny-lab/ \n \nYou've got 60 minutes left 'til the digital doors open…"""

    @staticmethod
    def timer_finished_no_address_message() -> str:
        return """Hey, hackers! No more waiting. The hacking of the lab kicks off with the first sent address."""

    @staticmethod
    def timer_finished_start_message(addresses: tp.List[str]) -> str:
        addresses_text = ""
        for address in addresses:
            addresses_text += f"- {address}\n"
        return f"""The hacking of the laboratory has started! Participating addresses:\n{addresses_text}\nHackers, hold tight for the robot hack and result of its recon mission…"""

    @staticmethod
    def winner_message(address: str, author: str) -> str:
        return f"Address {address} from {author} has winned this round."
    
    @staticmethod
    def address_added_message(address: str) -> str:
        return f"Address {address} was added"

    @staticmethod
    def second_address_from_one_user(user: tp.Union[User, Member]) -> str:
        return "One address from one user in this round"

    @staticmethod
    def message_with_dapp() -> str:
        return """Hey, hackers! Robot's done with its mission, you can find all the juicy logs over in the dapp: \nhttps://robonomics.academy/en/demoapps/johnnyb-lab/ \nJust hanging out here, waiting for some log hacking and token theft…"""

    def message_with_winner(winner_address: str) -> str:
        return f"Good job, hackers! You totally nailed the hack, {winner_address} address grabbed all tokens."

    def timer_reminder_message(minutes_left: int) -> str:
        if minutes_left == 20:
            return "Only 20 minutes to go until we start hacking…"
        elif minutes_left == 10:
            return "Only 10 more minutes to go before the hacking fun starts…"
        elif minutes_left == 5:
            return "Only 5 minutes to go until we start hacking…"
        elif minutes_left == 1:
            return "Only 1 minute to go before the hacking fun starts…" 
        else:
            return f"Only {minutes_left} minute to go before the hacking fun starts…" 
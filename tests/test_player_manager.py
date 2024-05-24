import pytest

from discord_bot.player_manager import PlayersManager
from discord_bot.models.player import Player
from discord_bot.exceptions.players_exceptions import TooManyPlayers

def test_add_player():
    players_manager = PlayersManager()
    players_manager.add_player("name", "address")
    assert len(players_manager.players_list) == 1

def test_add_two_players():
    players_manager = PlayersManager()
    players_manager.add_player("name", "address")
    players_manager.add_player("name1", "address1")
    assert len(players_manager.players_list) == 2

def test_add_three_players():
    players_manager = PlayersManager()
    players_manager.add_player("name", "address")
    players_manager.add_player("name1", "address1")
    players_manager.add_player("name2", "address2")
    assert len(players_manager.players_list) == 3

def test_add_more_than_three_players():
    players_manager = PlayersManager()
    players_manager.add_player("name", "address")
    players_manager.add_player("name1", "address1")
    players_manager.add_player("name2", "address2")
    with pytest.raises(TooManyPlayers):
        players_manager.add_player("name3", "address3")

def test_discord_acc_in_players():
    players_manager = PlayersManager()
    players_manager.add_player("name", "address")
    assert players_manager.discord_acc_in_players("name")

def test_discord_acc_not_in_players():
    players_manager = PlayersManager()
    players_manager.add_player("name", "address")
    assert not players_manager.discord_acc_in_players("name1")

def test_get_player_for_address():
    players_manager = PlayersManager()
    players_manager.add_player("name", "address")
    player = players_manager.get_player_for_address("address")
    assert player.discord_account_name == "name"
    assert player.robonomics_address == "address"
    player1 = players_manager.get_player_for_address("address1")
    assert player1 is None

def test_empty():
    players_manager = PlayersManager()
    assert players_manager.empty

def test_not_empty():
    players_manager = PlayersManager()
    players_manager.add_player("name", "address")
    assert not players_manager.empty

def test_full():
    players_manager = PlayersManager()
    players_manager.add_player("name", "address")
    players_manager.add_player("name1", "address1")
    players_manager.add_player("name2", "address2")
    assert players_manager.full

def test_not_full():
    players_manager = PlayersManager()
    players_manager.add_player("name", "address")
    assert not players_manager.full

def test_clear_players():
    players_manager = PlayersManager()
    players_manager.add_player("name", "address")
    players_manager.add_player("name1", "address1")
    players_manager.add_player("name2", "address2")
    players_manager.clear_players()
    assert players_manager.empty
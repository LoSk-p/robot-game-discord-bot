class TooManyPlayers(Exception):
    def __str__(self):
        return "Trying to add extra player."
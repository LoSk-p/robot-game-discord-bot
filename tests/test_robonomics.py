from discord_bot.robonomics import Robonomics

def test_get_address_for_seed():
    test_seed = "pull auction arch phrase waste question trade monkey pulse outer picnic ring"
    test_address = "4FfjTZ8ZPZMvKhqfJ6tTcE3FvgK1uKxqyowKFW3WAnYCq7fN"
    robonomics = Robonomics()
    assert robonomics._get_address_for_seed(test_seed) == test_address
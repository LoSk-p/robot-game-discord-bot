from substrateinterface import Keypair
import json

from discord_bot.utils import get_path_to_unused_seeds

SEEDS_COUNT = 18

seeds = []
for i in range(SEEDS_COUNT):
    generated_mnemonic = Keypair.generate_mnemonic()
    seeds.append(generated_mnemonic)

with open(get_path_to_unused_seeds(), "w") as f:
    json.dump(seeds, f)
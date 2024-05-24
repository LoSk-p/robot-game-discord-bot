import json
import typing as tp
from io import TextIOWrapper

from .logger import get_logger
from .utils import get_path_to_unused_seeds, get_path_to_used_seeds

logger = get_logger(__name__)


class SeedManager:
    def __init__(self) -> None:
        self.path_to_unused_seeds_file: str = get_path_to_unused_seeds()
        self.path_to_used_seeds_file: str = get_path_to_used_seeds()
        self.current_seed: tp.Optional[str] = None
        self.unused_seeds_count: tp.Optional[int] = self._get_unused_seeds_count()
        logger.info(
            f"Seed Manager is ready, path to unused seeds: {self.path_to_unused_seeds_file}, path to used seeds: {self.path_to_used_seeds_file}"
        )

    def get_new(self) -> str:
        logger.info("Get new seed request")
        new_seed = self._get_new_unused_seed_and_delete_it_from_file()
        self._add_seed_to_used(new_seed)
        logger.info(f"New seed for game is: {new_seed}")
        self.current_seed = new_seed
        return new_seed

    def get_unused_seeds_count(self) -> int:
        return self.unused_seeds_count

    def _get_new_unused_seed_and_delete_it_from_file(self) -> str:
        with open(self.path_to_unused_seeds_file, "r") as f:
            seeds = self._load_seeds_list(f)
            new_seed = seeds[0]
            seeds.remove(seeds[0])
        with open(self.path_to_unused_seeds_file, "w") as f:
            json.dump(seeds, f)
        self._update_unused_seeds_count(len(seeds))
        return new_seed

    def _add_seed_to_used(self, seed: str) -> None:
        with open(self.path_to_used_seeds_file, "r") as f:
            used_seeds = self._load_seeds_list(f)
            used_seeds.append(seed)
        with open(self.path_to_used_seeds_file, "w") as f:
            json.dump(used_seeds, f)

    def _load_seeds_list(self, f: TextIOWrapper) -> tp.List[str]:
        try:
            seeds = json.load(f)
        except json.decoder.JSONDecodeError:
            seeds = []
        return seeds

    def _get_unused_seeds_count(self) -> int:
        with open(self.path_to_unused_seeds_file, "r") as f:
            seeds = json.load(f)
            seeds_count = len(seeds)
        return seeds_count

    def _update_unused_seeds_count(self, new_count: int) -> None:
        logger.info(f"unused seed count: {new_count}")
        self.unused_seeds_count = new_count

import hashlib
import json
from typing import Optional
import logging
import os
import dill

logger = logging.getLogger(__name__)


class ObjectCache:
    def __init__(
        self,
        dict_object: Optional[dict[str, str]] = None,
        df: Optional[list[object]] = None,
    ):
        self.dict_object = dict_object
        self.df = df
        self.logger = logging.getLogger(__name__)

    def __get_hash(self) -> str:
        serialized_data = json.dumps(self.dict_object, sort_keys=True)
        # Generate an SHA-256 hash from the string
        hasher = hashlib.sha256()
        hasher.update(serialized_data.encode("utf-8"))
        hash_value = hasher.hexdigest()

        return hash_value

    def save(self, to_file_name: str = None) -> None:
        self.logger.info(
            f"ObjectCache.save() in directory {os.getcwd()}/cache type={type(self.df)}"
        )
        if to_file_name is not None:
            if not to_file_name.endswith(".pkl"):
                to_file_name = f"{to_file_name}.pkl"
            file_path = f"cache/{to_file_name}"
        else:
            file_path = f"cache/{self.__get_hash()}.pkl"
        with open(file_path, "wb") as file:
            dill.dump(self.df, file)
            self.logger.info(f"ObjectCache.save() saved to {file_path}")

    @staticmethod
    def load_from_file(file_path: str) -> Optional[list[dict[str, str]]]:
        try:
            with open(file_path, "rb") as file:
                data_loaded = dill.load(file)
                logger.info(
                    f"ObjectCache.load_with_hash() loaded from {file_path}, type={type(data_loaded)}"
                )
                return data_loaded
        except FileNotFoundError:
            logger.warning(f"ObjectCache.load_with_hash() file not found: {file_path}")
            return None

    def load(self) -> Optional[list[object]]:
        file_path = f"cache/{self.__get_hash()}.pkl"
        return ObjectCache.load_from_file(file_path)

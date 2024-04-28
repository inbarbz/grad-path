import pandas as pd
import hashlib
import json
from typing import Optional
import brotli
import logging
import os


class DataFrameCache:
    def __init__(self, dict_object: dict[str, str], df: Optional[pd.DataFrame] = None):
        self.dict_object = dict_object
        self.df = df
        self.logger = logging.getLogger(__name__)

    def __get_hash(self) -> str:
        # data = brotli.compress(
        #     json.dumps(self.dict_object, sort_keys=True, indent=0)
        #     .replace("\n", "")
        #     .encode("utf-8"),
        #     mode=(brotli.MODE_TEXT,),
        # )
        serialized_data = json.dumps(self.dict_object, sort_keys=True)
        # Generate a SHA-256 hash from the string
        hasher = hashlib.sha256()
        hasher.update(serialized_data.encode("utf-8"))
        hash_value = hasher.hexdigest()

        return hash_value

    def save(self) -> None:
        self.logger.info(f"DataFrameCache.save() in directory {os.getcwd()}/cache")
        file_path = f"cache/{self.__get_hash()}.csv"
        self.df.to_csv(file_path, index=False)

    def load(self) -> Optional[pd.DataFrame]:
        file_path = f"cache/{self.__get_hash()}.csv"
        try:
            return pd.read_csv(file_path)
        except FileNotFoundError:
            return None

import json
from utils.path_utils import ParentPath
from pathlib import Path


class JSONReader:

    @staticmethod
    def _get_base_dir():
        return ParentPath().config_path

    @staticmethod
    def read_file(filename):
        base_dir = JSONReader._get_base_dir()
        with Path(f"{base_dir}/" + filename).open("r",encoding="utf-8") as f:
            return json.load(f)

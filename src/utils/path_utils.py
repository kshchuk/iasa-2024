import sys
from pathlib import Path


class ParentPath:
    """This class is used to find the absolute path of the project folder in the system."""

    def __init__(self):
        project_folder = "iasa-2024"
        current_directory = Path(__file__).resolve().parent.parent

        # try:
        #     config_path = next(
        #         ancestor
        #         for ancestor in current_directory.parents
        #         if ancestor.name == project_folder
        #     )
        # except StopIteration:
        #     print(f"Folder '{project_folder}' not found in the path.")
        #     raise
        #
        # self.config_path = config_path

        self.config_path = current_directory


def debugger_is_active() -> bool:
    """Return if the debugger is currently active"""
    return hasattr(sys, 'gettrace') and sys.gettrace() is not None

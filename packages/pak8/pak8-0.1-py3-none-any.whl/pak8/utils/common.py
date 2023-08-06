import pickle
from pathlib import Path
from typing import Any, List, Optional, Type

from pak8.utils.log import logger


def isinstanceany(obj: Any, class_list: List[Type]) -> bool:
    for cls in class_list:
        if isinstance(obj, cls):
            return True
    return False


def unpickle_object_from_file(
    file_path: Path, verify_class: Optional[Any] = None
) -> Any:
    """Reads the contents of file_path and unpickles the binary content into an object.
    If verify_class is provided, checks if the object is an instance of that class.
    """
    _obj = None
    if file_path.exists() and file_path.is_file():
        _obj = pickle.load(file_path.open("rb"))

    if _obj and verify_class and not isinstance(_obj, verify_class):
        logger.error(f"Unpickled object does not match {verify_class}")
        _obj = None

    return _obj


def pickle_object_to_file(obj: Any, file_path: Path) -> Any:
    """Pickles and saves object to file_path"""

    _obj_parent = file_path.parent
    if not _obj_parent.exists():
        _obj_parent.mkdir(parents=True, exist_ok=True)
    pickle.dump(obj, file_path.open("wb"))


def print_section_break() -> None:
    print("-" * 10, "*", "-" * 10)


def is_empty(val: Any) -> bool:
    if val is None or len(val) == 0 or val == "":
        return True
    return False

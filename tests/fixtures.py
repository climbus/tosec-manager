from parser import FLAG, TosecFile
from typing import Any, Dict, List, Union


def create_tosec_file(title: str, **kwargs: Any) -> TosecFile:
    """Factory function to create TosecFile with default values."""
    defaults: Dict[str, Union[str, List[FLAG]]] = {
        "filename": f"{title}.tap",
        "year": "1989",
        "publisher": "Mastertronic",
        "extension": "tap",
        "flags": [],
        "language": "",
    }
    defaults.update(kwargs)
    return TosecFile(title=title, **defaults)  # type: ignore

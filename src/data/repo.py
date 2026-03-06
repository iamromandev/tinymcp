"""Recore repo: provides dummy data list."""

# Default dummy data list for Recore.
DUMMY_DATA_LIST: list[dict[str, str | int | float]] = [
    {"id": 1, "name": "Item A", "value": 10.5},
    {"id": 2, "name": "Item B", "value": 20.0},
    {"id": 3, "name": "Item C", "value": 15.25},
    {"id": 4, "name": "Item D", "value": 8.75},
    {"id": 5, "name": "Item E", "value": 32.0},
]


class RecoreRepo:
    """Repo for Recore: access to dummy data list."""

    def __init__(self, data: list[dict] | None = None) -> None:
        self._data = list(data) if data is not None else list(DUMMY_DATA_LIST)

    def get_dummy_data_list(self) -> list[dict]:
        """Return the dummy data list."""
        return self._data

    def get_by_id(self, id: int) -> dict | None:
        """Return the first item with the given id, or None."""
        for item in self._data:
            if item.get("id") == id:
                return item
        return None


def get_dummy_data_list() -> list[dict]:
    """Return the default dummy data list."""
    return list(DUMMY_DATA_LIST)

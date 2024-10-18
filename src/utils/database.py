import tinydb
import os
import threading
import json
from typing import TypeVar, Generic, Union, List
from pydantic import BaseModel
from utils import json_helper


_lock_object = threading.Lock()
_database: tinydb.TinyDB = None
_tables = {}
database_path: str = None

T = TypeVar("T")

class DatabaseTable(Generic[T]):
    """A class representing a database table."""

    def __init__(self, table: tinydb.database.Table, table_type: type):
        self.table = table
        self.table_type = table_type

    def insert_data(self, data: Union[T, List[T]]) -> List[int]:
        """Insert data into the database.

        Args:
            data (Union[T, List[T]]): The data to insert.

        Returns:
            List[int]: The list of inserted document IDs.
        """
        with _lock_object:
            data_dict = json.loads(json_helper.object_to_json(data))

            if isinstance(data, list):
                return self.table.insert_multiple(data_dict)

            return [self.table.insert(data_dict)]

    def get_data(self, query: tinydb.Query) -> List[T]:
        """Get data from the database.

        Args:
            query (tinydb.Query): The query to filter the data.

        Returns:
            List[T]: The list of data.
        """
        with _lock_object:
            results = self.table.search(query)

            # Convert the results back to the original type.
            return [self.table_type(**result) for result in results]

    def update_data(self, query: tinydb.Query, data: T) -> List[int]:
        """Update data in the database.

        Args:
            query (tinydb.Query): The query to filter the data.
            data (T): The data to update it with.

        Returns:
            List[int]: The list of updated document IDs.
        """
        with _lock_object:
            data_dict = json.loads(json_helper.object_to_json(data))

            return self.table.update(data_dict, query)

    def delete_data(self, query: tinydb.Query) -> List[int]:
        """Delete data from the database.
        
        Args:
            query (tinydb.Query): The query to filter the data.

        Returns:
            List[int]: The list of removed document IDs.
        """
        with _lock_object:
            return self.table.remove(query)


def setup_database(database_name: str = "database"):
    """Setup the database.

    Args:
        database_name (str): The name of the database. Defaults to "database".
    """
    global _database, database_path

    database_path = os.path.join(os.path.dirname(__file__), "data", f"{database_name}.json")
    _database = tinydb.TinyDB(database_path)

def close_database():
    """Close the database."""
    with _lock_object:
        _database.close()

def get_table(table_type: type) -> DatabaseTable[T]:
    """Get a table from the database.

    Args:
        table_type (type): The type of the table.

    Returns:
        DatabaseTable[T]: The database table.
    """
    # Check if type inherits from BaseModel.
    if not issubclass(table_type, BaseModel):
        raise ValueError("The table type must inherit from BaseModel!")

    type_name = table_type.__name__

    if type_name not in _tables:
        table = _database.table(type_name)
        database_table = DatabaseTable(table, table_type)

        _tables[type_name] = database_table

    return _tables[type_name]

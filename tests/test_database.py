from utils import database
import os
from pydantic import BaseModel
import pytest


class TestDatabase:
    """A class to test the database module."""

    @classmethod
    def setup_class(cls):
        """Setup the test class."""
        database.setup_database("test_database")
        cls.table: database.DatabaseTable[TestUser] = database.get_table(TestUser)

    @classmethod
    def teardown_class(cls):
        """Clean up the test class."""
        database.close_database()
        os.remove(database.database_path)

    def test_get_table_not_base_model_throws(self):
        """Test if get_table throws an exception when the type is not a BaseModel."""
        # Act & Assert
        with pytest.raises(ValueError):
            database.get_table(dict)

    def test_insert_data(self):
        """Test the insert_data method."""
        # Arrange
        data = TestUser(name="Francis", age=1)
        query = database.tinydb.Query()

        # Act
        self.table.insert_data(data)
        found_data = self.table.get_data(query.name == data.name)[0]

        # Assert
        assert found_data.name == data.name
        assert isinstance(found_data, TestUser)

    def test_insert_multiple_data(self):
        """Test the insert_data method."""
        # Arrange
        data = [TestUser(name="Tom", age=1), TestUser(name="Tedd", age=2)]
        query = database.tinydb.Query()
        found_data = []

        # Act
        self.table.insert_data(data)

        for user in data:
            found_data.append(self.table.get_data(query.name == user.name)[0])

        # Assert
        assert found_data[0].name == data[0].name
        assert found_data[1].name == data[1].name

    def test_update_data(self):
        """Test the update_data method."""
        # Arrange
        data = TestUser(name="Marlene", age=1)
        query = database.tinydb.Query()
        insert_id = self.table.insert_data(data)

        # Act
        data.age = 2
        update_id = self.table.update_data(query.name == data.name, data)
        found_data = self.table.get_data(query.name == data.name)[0]

        # Assert
        assert found_data.age == data.age
        assert insert_id == update_id

    def test_delete_data(self):
        """Test the delete_data method."""
        # Arrange
        data = TestUser(name="Arthur", age=1)
        query = database.tinydb.Query()
        insert_id = self.table.insert_data(data)

        # Act
        deleted_id = self.table.delete_data(query.name == data.name)
        found_data = self.table.get_data(query.name == data.name)

        # Assert
        assert len(found_data) == 0
        assert insert_id == deleted_id


class TestUser(BaseModel):
    """A class representing a user."""
    name: str
    age: int

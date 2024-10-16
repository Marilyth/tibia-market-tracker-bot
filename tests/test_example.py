class TestExample:
    """Test class for example."""

    @classmethod
    def setup_class(cls):
        """Setup the test class."""

    @classmethod
    def teardown_class(cls):
        """Clean up the test class."""

    def test_method_case_expected_result(self):
        """Test method for case returns expected result."""
        # Arrange
        test = 1

        # Act
        test += 1

        # Assert
        assert test == 2

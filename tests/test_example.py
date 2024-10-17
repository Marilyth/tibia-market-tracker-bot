class TestExample:
    """Test class for example."""

    @classmethod
    def setup_class(cls):
        """Setup the test class for all tests."""

    def setup_method(self):
        """Setup the test class for the current method."""

    @classmethod
    def teardown_class(cls):
        """Clean up the test class for all tests."""

    def teardown_method(self):
        """Clean up the test class for the current method."""

    def test_method_case_expected_result(self):
        """Test method for case returns expected result."""
        # Arrange
        test = 1

        # Act
        test += 1

        # Assert
        assert test == 2

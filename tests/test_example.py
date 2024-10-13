class TestExample:
    # Run this method once before any test.
    @classmethod
    def setup_class(cls):
        pass

    # Run this method once after all tests.
    @classmethod
    def teardown_class(cls):
        pass

    def test_StartGame_WhenCalled_ReturnsTrue(self):
        # Arrange
        test = 1
        
        # Act
        test += 1

        # Assert
        assert test == 2
        
from utils.data.market_values import MarketValues
from time import time
from io import BytesIO


def get_sample_market_values(sample_size: int) -> MarketValues:
    """Returns a list of sample market values for testing.
    
    Args:
        sample_size (int): The number of sample market values to return.

    Returns:
        MarketValues: The sample market values.
    """
    market_values = []

    for i in range(sample_size):
        market_values.append(MarketValues(id=22118, time=time() - (60 * 60 * 24 * i),
                                          day_average_sell=100 + i * 10,
                                          day_average_buy=90 + i * 10,
                                          sell_offer=110 + i * 10,
                                          buy_offer=80 + i * 10))

    return market_values

def test_generate_price_history_plot():
    """Test that the price history plot is generated correctly."""
    sample = get_sample_market_values(30)

    bytesio: BytesIO = MarketValues.generate_price_history_plot(sample)
    # Save the image to a file for manual inspection.
    with open("price_history_plot.png", "wb") as file:
        file.write(bytesio.getbuffer())

    assert bytesio is not None

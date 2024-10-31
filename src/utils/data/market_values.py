from pydantic import BaseModel
from typing import List
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from io import BytesIO


class MarketValues(BaseModel):
    """A data class containing information about the market values of an item.
    """
    id: int
    time: float
    is_full_data: bool = False
    buy_offer: int = -1
    sell_offer: int = -1
    month_average_sell: int = -1
    month_average_buy: int = -1
    month_sold: int = -1
    month_bought: int = -1
    active_traders: int = -1
    month_highest_sell: int = -1
    month_lowest_buy: int = -1
    month_lowest_sell: int = -1
    month_highest_buy: int = -1
    buy_offers: int = -1
    sell_offers: int = -1
    day_average_sell: int = -1
    day_average_buy: int = -1
    day_sold: int = -1
    day_bought: int = -1
    day_highest_sell: int = -1
    day_lowest_sell: int = -1
    day_highest_buy: int = -1
    day_lowest_buy: int = -1
    total_immediate_profit: int = -1
    total_immediate_profit_info: str = ""

    @staticmethod
    def generate_price_history_plot(market_values: List["MarketValues"]) -> BytesIO:
        """Returns a pyplot plot of the price history of the item.

        Args:
            market_values (List[MarketValues]): The market values of the item.

        Returns:
            str: The path to the saved plot.
        """
        plt.ioff()

        time = [market_value.time / (24 * 3600) for market_value in market_values]
        sell = [market_value.day_average_sell if market_value.day_average_sell > 0 else market_value.sell_offer if market_value.sell_offer > 0 else None for market_value in market_values]
        buy = [market_value.day_average_buy if market_value.day_average_buy > 0 else market_value.buy_offer if market_value.buy_offer > 0 else None for market_value in market_values]

        line_color = "#A9A9A9"
        buy_color = "#8884d8"
        sell_color = "#82ca9d"

        # Create a new figure.
        figure = plt.figure(facecolor=None)
        figure.tight_layout()

        subplot = figure.add_subplot(111, facecolor=None)
        subplot.spines["top"].set_visible(False)
        subplot.spines["right"].set_visible(False)
        subplot.spines["bottom"].set_color(line_color)
        subplot.spines["left"].set_color(line_color)
        subplot.tick_params(colors=line_color)
        subplot.yaxis.label.set_color(line_color)
        subplot.xaxis.label.set_color(line_color)

        # Set the x-axis to display dates.
        subplot.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        figure.autofmt_xdate()

        # Plot the sell and buy values.
        subplot.plot(time, sell, label="Sell price", linestyle="-", color=sell_color)
        subplot.plot(time, buy, label="Buy price", linestyle="-", color=buy_color)

        # Set the labels and title.
        subplot.set_xlabel("Time", color=line_color)
        subplot.set_ylabel("Price", color=line_color)

        # Add a legend.
        subplot.legend(facecolor=None, edgecolor=None, labelcolor=line_color, framealpha=0)

        # Save the plot to a BytesIO object.
        plot_bytes = BytesIO()
        figure.savefig(plot_bytes, format="png", transparent=True)
        plot_bytes.seek(0)

        # Clear the figure.
        figure.clear()

        return plot_bytes

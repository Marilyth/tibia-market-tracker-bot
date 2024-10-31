from pydantic import BaseModel
from typing import List
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
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

        time = np.array([market_value.time / (24 * 3600) for market_value in market_values], dtype=np.float64)
        sell = [market_value.day_average_sell if market_value.day_average_sell > -1 else market_value.sell_offer for market_value in market_values]
        buy = [market_value.day_average_buy if market_value.day_average_buy > -1 else market_value.buy_offer for market_value in market_values]

        sell = np.array([price if price > 0 else None for price in sell], dtype=np.float64)
        buy = np.array([price if price > 0 else None for price in buy], dtype=np.float64)
        sell_mask = np.isfinite(sell)
        buy_mask = np.isfinite(buy)

        line_color = "#A9A9A9"
        buy_color = "#8884d8"
        sell_color = "#82ca9d"

        # Create a new figure.
        figure = plt.figure(facecolor=None)
        figure.tight_layout()

        subplot = figure.add_subplot(111, facecolor=None)
        subplot.grid(True, color=line_color, linestyle="--", linewidth=0.5, which="major", axis="both", alpha=0.25)
        subplot.set_xlim(min(time), max(time))
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
        subplot.plot(time[sell_mask], sell[sell_mask], label="Sell price", linestyle="-", color=sell_color, marker="o" if len(sell) < 31 else None)
        subplot.plot(time[buy_mask], buy[buy_mask], label="Buy price", linestyle="-", color=buy_color, marker="o" if len(buy) < 31 else None)

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

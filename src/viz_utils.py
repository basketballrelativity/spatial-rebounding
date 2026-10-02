"""
This code contains the functionality to plot
relevant visualizations
"""

import pandas as pd

import matplotlib.pyplot as plt
from mplbasketball import Court


def initialize_court():
    """ Small utility function to generate
    a court visualization

    Returns:
        Matplotlib figure and axis objects
    """

    court = Court(court_type="nba", origin="center", units="ft")
    fig, ax = court.draw(showaxis=True)

    return fig, ax


def plot_rebound_locations(rebound_df):
    """ This function plots the rebounding location
    of shots in the provided DataFrame

    Args:
        rebound_df (pd.DataFrame): DataFrame of rebound
            locations

    Returns:
        Figure saved to the local directory
    """

    fig, ax = initialize_court()

    # Subset to valid rebounds
    rebound_df = rebound_df[
        (pd.notnull(rebound_df["rebound_x"])) &
        (pd.notnull(rebound_df["rebound_y"]))
    ]

    ax.scatter(rebound_df["rebound_x"], rebound_df["rebound_y"], marker="o", color="blue", alpha=0.5)

    plt.savefig("rebound_test.png")
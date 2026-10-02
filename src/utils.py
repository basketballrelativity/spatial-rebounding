"""
This script contains utility functions that
process the rebounding, shot, and tracking data
in order to get the data in a suitable format
for modeling
"""

import pandas as pd

def merge_rebounds_and_shots(
    rebound_df: pd.DataFrame,
    shot_df: pd.DataFrame,
):
    """ This function merges rebounds and shots together.
    The overall purpose is to get the shot frameIdx for
    the eventual mapping of full tracking data, but this can
    be used in the interim to construct intermediate models
    (rebound location probability distribution, for example)

    Args:
        rebound_df (pd.DataFrame): DataFrame containing rebound
            information
        shot_df (pd.DataFrame): DataFrame containing shot
            information

    Returns:
        rebound_df (pd.DataFrame): DataFrame containing rebound
            and relevant shot data
    """

    rebound_df = rebound_df.merge(
        shot_df[["gameId", "id", "startFrame", "location"]],
        left_on=["gameId", "shotId"],
        right_on=["gameId", "id"],
        how="left",
        suffixes=("", "_shot")
    )

    # Unpack coordinates
    rebound_df["rebound_x"] = [x[0] for x in rebound_df["location"]]
    rebound_df["rebound_y"] = [x[1] for x in rebound_df["location"]]

    rebound_df["shot_x"] = [x[0] for x in rebound_df["location_shot"]]
    rebound_df["shot_y"] = [x[1] for x in rebound_df["location_shot"]]

    return rebound_df

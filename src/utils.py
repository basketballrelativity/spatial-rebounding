"""
This script contains utility functions that
process the rebounding, shot, and tracking data
in order to get the data in a suitable format
for modeling
"""

import numpy as np
import pandas as pd

def merge_rebounds_and_shots(
    rebound_df: pd.DataFrame,
    shot_df: pd.DataFrame
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
        shot_df[["gameId", "id", "startFrame", "location", "distance"]],
        left_on=["gameId", "shotId"],
        right_on=["gameId", "id"],
        how="left",
        suffixes=("", "_shot")
    )

    # Unpack coordinates
    rebound_x = []
    rebound_y = []
    shot_x = []
    shot_y = []
    for _, row in rebound_df.iterrows():
        if row["location"] and type(row["location"]) != float:
            rebound_x.append(row["location"][0])
            rebound_y.append(row["location"][1])
        else:
            rebound_x.append(np.nan)
            rebound_y.append(np.nan)

        if row["location_shot"] and type(row["location_shot"]) != float:
            shot_x.append(row["location_shot"][0])
            shot_y.append(row["location_shot"][1])
        else:
            shot_x.append(np.nan)
            shot_y.append(np.nan)

    # Store in original DataFrame
    rebound_df["rebound_x"] = rebound_x
    rebound_df["rebound_y"] = rebound_y

    rebound_df["shot_x"] = shot_x
    rebound_df["shot_y"] = shot_y

    return rebound_df

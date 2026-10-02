"""
This script provides functionality to load data
"""

import json
import pandas as pd

def read_dynamic_events(match_id: int) -> pd.DataFrame:
    """ This function reads in the dynamic events file
    for a given `match_id`

    Args:
        match_id (int): Unique identifier of the match

    Returns:
        - tuple of three DataFrames
            - rebound_df (pd.DataFrame): DataFrame containing
                every rebound in the match
            - shot_df (pd.DataFrame): DataFrame containing every
                shot in the match
            - chance_df (pd.DataFrame): DataFrame containing every
                chance in the match (will be used to get tracking data
                between shot and rebound)
    """

    file_name = f"{match_id}_dynamic_events.json"
    with open(f"../data/matches/{match_id}/{file_name}", 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Unpack
    rebound_df = pd.DataFrame(data["rebounds"])
    shot_df = pd.DataFrame(data["shots"])
    chance_df = pd.DataFrame(data["chance_players"])

    return rebound_df, shot_df, chance_df


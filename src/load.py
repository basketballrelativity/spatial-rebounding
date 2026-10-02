"""
This script provides functionality to load data
"""

import json

import numpy as np
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


def process_tracking_row(row: pd.Series, player_row: pd.Series, actor_type: str) -> pd.DataFrame:
    """ This function unpacks the nested player and
    ball tracking rows present in the tracking data

    Args:
        row (pd.Series): Row from the tracking data
        actor_type (str): One of "ball", "home", or "away"
        player_row (pd.Series): Row with player specific info

    Returns:
        temp_df (pd.DataFrame): One-row DataFrame storing
            the unpacked data
    """

    # Initialize DataFrame
    temp_df = pd.DataFrame()

    # Unpack
    if actor_type == "ball":
        if row["ball"]:
            x, y, z = row["ball"]["xyz"]
            speed = row["ball"]["speed"]
        else:
            x, y, z = np.nan, np.nan, np.nan
            speed = np.nan
        actor_id = -1
        home = np.nan
    else:
        if player_row:
            x, y, z = player_row["xyz"]
            speed = player_row["speed"]
            actor_id = player_row["playerId"]
        else:
            x, y, z = np.nan, np.nan, np.nan
            speed = np.nan
            actor_id = np.nan
        home = 1 if actor_type == "home" else 0

    # Restore
    temp_df = pd.DataFrame(
        {
            "frameIdx": [row["frameIdx"]],
            "wallClock": [row["wallClock"]],
            "gameClock": [row["gameClock"]],
            "gameClockStopped": [row["gameClockStopped"]],
            "period": [row["period"]],
            "shotClock": [row["shotClock"]],
            "x": [x],
            "y": [y],
            "z": [z],
            "speed": [speed],
            "id": [actor_id],
            "home": [home]
        }
    )

    return temp_df


def read_tracking_data(match_id: int) -> pd.DataFrame():
    """ This function reads in the tracking data for a
    given given `match_id`

    Args:
        match_id (int): Unique identifier of the match

    Returns:
        - tracking_df (pd.DataFrame): Tracking data
    """

    path = f"../data/matches/{match_id}/{match_id}_tracking_data.jsonl.gz"

    tracking_df = pd.read_json(path, lines=True, compression="gzip")

    # long_tracking_df = pd.DataFrame()
    # for _, row in tracking_df.iterrows():
    #     temp_df = process_tracking_row(row, row, "ball")
    #     long_tracking_df = pd.concat([long_tracking_df, temp_df])
    #     for side in ["home", "away"]:
    #         for player in row[f"{side}Players"]:
    #             temp_df = process_tracking_row(row, player, side)
    #             long_tracking_df = pd.concat([long_tracking_df, temp_df])

    return long_stracking_df
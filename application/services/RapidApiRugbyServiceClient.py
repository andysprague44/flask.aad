
from application import appsettings as config
import requests
import pandas as pd
from typing import Tuple

def get_rugby_standings(comp_id: int = 1218, season: int = 2020) -> Tuple[str, pd.DataFrame]:
    """Using a rugby API to get some test data. 
    
    Args:
        comp_id: Look up Id from https://rugby-live-data.p.rapidapi.com/competitions, default is 1218 = gallagher premiership(UK)
        season: year season ends (so 2019/2020 -> 2020), default 2020

    Returns:
        tuple of (table name, dataframe of team standings)
    """
    url = f'https://rugby-live-data.p.rapidapi.com/standings/{comp_id}/{season}'
    headers = {
        'x-rapidapi-key': config.RAPIDAPI_KEY,
        'x-rapidapi-host': config.RAPIDAPI_HOST
        }
    response = requests.request("GET", url, headers=headers)
    results_json = response.json()['results']

    title = results_json['standings'][0]['table_name'] + f' {season-1}/{season}'

    team_standings = results_json['standings'][0]['teams']
    df = pd.DataFrame(team_standings)

    return title, df

import os
import sys
import logging


from app.parser import get_anime_filler_list
from app.sonarr import configure_monitoring, get_sonarr_episodes
from app.plex import create_plex_collection

from constants.logger import LOG_LEVELS
from constants.variables import UserConfig


var = UserConfig()

log_level = os.environ.get("LOG_LEVEL", "INFO").upper()

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=LOG_LEVELS.get(log_level, logging.INFO),
    handlers=[logging.StreamHandler(sys.stdout)],
)

if __name__ == "__main__":
    episodes_to_monitor = []

    logging.info("Initializing SoFE...")
    logging.info("Address is set to '%s'", var.listen_address)
    logging.info("Port is set to '%s'", var.listen_port)

    fillers_from_api = get_anime_filler_list(var.afl_anime_name)
    sonarr_episodes_id = get_sonarr_episodes(int(var.sonarr_series_id))

    if var.create_plex_collection is True:
        create_plex_collection(fillers=fillers_from_api)

    for episode in sonarr_episodes_id:
        if episode["episode_number"] not in fillers_from_api:
            episodes_to_monitor.append(episode.get("id"))

    logging.debug("Non-Filler Episodes: %s", episodes_to_monitor)

    if episodes_to_monitor and var.monitor_non_filler_sonarr_episodes is True:
        configure_monitoring(monitored_list=episodes_to_monitor)

from app.parser import get_anime_filler_list
from app.sonarr import configure_monitoring, get_sonarr_episodes
from app.plex import create_plex_collection

from constants.variables import UserConfig
from constants.logger import logger, log_level, LOG_LEVELS


logger.setLevel(LOG_LEVELS[log_level])

var = UserConfig()

if __name__ == "__main__":
    episodes_to_monitor = []

    logger.info("Initializing SoFE...")
    logger.info("Address is set to '%s'", var.listen_address)
    logger.info("Port is set to '%s'", var.listen_port)

    fillers_from_api = get_anime_filler_list(var.afl_anime_name)
    sonarr_episodes_id = get_sonarr_episodes(int(var.sonarr_series_id))

    if var.create_plex_collection is True:
        create_plex_collection(
            sonarr_episodes=sonarr_episodes_id, fillers=fillers_from_api
        )

    for episode in sonarr_episodes_id:
        if episode["episode_number"] not in fillers_from_api:
            episodes_to_monitor.append(episode.get("id"))

    logger.debug("Non-Filler Episodes: %s", episodes_to_monitor)

    if not episodes_to_monitor or var.monitor_non_filler_sonarr_episodes is True:
        configure_monitoring(monitored_list=episodes_to_monitor)

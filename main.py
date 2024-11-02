import json
import logging


from app.plex import create_plex_collection
from app.parser import get_anime_filler_list
from app.sonarr import get_sonarr_episodes, configure_monitoring
from app.variables import USER_CONFIG


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

if USER_CONFIG.debug is True:
    logger.setLevel("DEBUG")


def main():
    nonfillers_episodes = []

    fillers_from_api = get_anime_filler_list(USER_CONFIG.afl_anime_name)
    sonarr_episodes = get_sonarr_episodes(int(USER_CONFIG.sonarr_series_id))

    for episode in sonarr_episodes:
        if episode["absolute_episode_number"] not in fillers_from_api:
            nonfillers_episodes.append(
                {
                    "id": episode.get("id"),
                    "season": episode.get("season"),
                    "episode_number": episode.get("episode_number"),
                    "absolute_episode_number": episode.get("absolute_episode_number"),
                }
            )

    episodes_in_season_episode_format = [
        f"s{episode['season']:02d}e{episode['episode_number']:02d}"
        for episode in nonfillers_episodes
    ]

    episodes_to_monitor = [episode.get("id") for episode in nonfillers_episodes]

    if USER_CONFIG.create_plex_collection is True:
        create_plex_collection(collection_items=episodes_in_season_episode_format)

    logger.debug(f"Non-Filler Episodes: {json.dumps(nonfillers_episodes, indent=4)}")

    if nonfillers_episodes and USER_CONFIG.monitor_non_filler_sonarr_episodes is True:
        configure_monitoring(monitored_list=episodes_to_monitor)


if __name__ == "__main__":
    logger.info("Initializing SoFE...")
    main()

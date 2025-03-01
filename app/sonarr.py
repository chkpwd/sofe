import sonarr
import logging

from app.variables import USER_CONFIG

logger = logging.getLogger(__name__)


CONFIGURATION = sonarr.Configuration(host=USER_CONFIG.sonarr_url)
CONFIGURATION.api_key["X-Api-Key"] = USER_CONFIG.sonarr_api_key


def get_sonarr_episodes(series_id: int):
    """Get the sonarr episodes."""
    episodes = []

    with sonarr.ApiClient(configuration=CONFIGURATION) as api_client:
        api_instance = sonarr.EpisodeApi(api_client)

        try:
            api_response = api_instance.list_episode(series_id=series_id)

            for item in api_response:
                if item.season_number != 0:
                    episodes.append(
                        {
                            "id": item.id,
                            "title": item.title,
                            "season": item.season_number,
                            "monitored": item.monitored,
                            "episode_number": item.episode_number,
                            "absolute_episode_number": item.absolute_episode_number,
                        }
                    )
        except Exception as e:
            logger.error("Exception when calling EpisodeApi->list_episode: %s\n" % e)

        return episodes


def configure_monitoring(monitored_list: list[int]):
    """Configure the sonarr episodes to be monitored."""
    with sonarr.ApiClient(configuration=CONFIGURATION) as api_client:
        api_instance = sonarr.EpisodeApi(api_client)

        episodes_monitored_resource = sonarr.EpisodesMonitoredResource(
            episodeIds=[*monitored_list], monitored=True
        )

        try:
            api_instance.put_episode_monitor(
                episodes_monitored_resource=episodes_monitored_resource
            )
        except Exception as e:
            logger.error(
                "Exception when calling EpisodeApi->put_episode_monitor: %s\n" % e
            )

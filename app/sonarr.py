import os
import sonarr
import logging


CONFIGURATION = sonarr.Configuration(host="https://sonarr.local.chkpwd.com")
CONFIGURATION.api_key["X-Api-Key"] = os.environ["SONARR_API_KEY"]


def get_sonarr_episodes(series_id: int):
    """Get the sonarr episodes."""
    episodes = []

    with sonarr.ApiClient(configuration=CONFIGURATION) as api_client:
        api_instance = sonarr.EpisodeApi(api_client)
        series_id = series_id

        try:
            api_response = api_instance.list_episode(series_id=series_id)

            for item in api_response:
                episodes.append(
                    {
                        "id": item.id,
                        "title": item.title,
                        "number": item.absolute_episode_number,
                        "monitored": item.monitored,
                    }
                )

        except Exception as e:
            logging.error("Exception when calling EpisodeApi->list_episode: %s\n" % e)

        return episodes


def configure_monitoring(episodes: list):
    """Configure the sonarr episodes to be monitored."""
    with sonarr.ApiClient(configuration=CONFIGURATION) as api_client:
        api_instance = sonarr.EpisodeApi(api_client)

        episodes_monitored_resource = sonarr.EpisodesMonitoredResource(
            episodeIds=[*episodes]
        )
        episodes_monitored_resource.monitored = True

        try:
            api_instance.put_episode_monitor(
                episodes_monitored_resource=episodes_monitored_resource
            )
        except Exception as e:
            logging.error(
                "Exception when calling EpisodeApi->put_episode_monitor: %s\n" % e
            )

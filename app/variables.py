import os
import sys
import logging

from dotenv import load_dotenv
from attrs.converters import to_bool


load_dotenv(dotenv_path=".env.priv")

logger = logging.getLogger(__name__)


class UserConfig:
    """
    Configuration constants for the application.

    Attributes:
        debug (bool): Whether or not to enable debug logging. Defaults to False.
        afl_anime_name (str): The name of the anime to fetch filler episodes for.
        sonarr_url (str): The URL of the Sonarr server.
        sonarr_series_id (int): The ID of the Sonarr series to update.
        sonarr_api_key (str): The API key for the Sonarr server.
        monitor_non_filler_sonarr_episodes (bool): Whether or not to monitor non-filler episodes. Defaults to False.
        plex_url (str): The URL of the Plex server. Optional.
        plex_token (str): The token for the Plex server. Optional.
        create_plex_collection (bool): Whether or not to create a Plex collection for the anime. Defaults to False.
        plex_anime_library (str): The name of the Plex library to add the anime collection to.
        plex_anime_name (str): The name of the anime as shown in Plex.
    """

    def __init__(self):
        self.debug: bool = to_bool(os.environ.get("DEBUG", default="False"))
        self.afl_anime_name: str = self._get_env_var("AFL_ANIME_NAME", required=True)
        self.sonarr_url: str = self._get_env_var("SONARR_URL", required=True)
        self.sonarr_series_id: int = int(
            self._get_env_var("SONARR_SERIES_ID", required=True)
        )
        self.sonarr_api_key: str = self._get_env_var("SONARR_API_KEY", required=True)
        self.monitor_non_filler_sonarr_episodes: bool = to_bool(
            self._get_env_var(
                "MONITOR_NON_FILLER_SONARR_EPISODES", required=True, default="True"
            )
        )
        self.create_plex_collection: bool = to_bool(
            self._get_env_var("CREATE_PLEX_COLLECTION", required=True, default="False")
        )
        self.plex_url: str = self._get_env_var("PLEX_URL")
        self.plex_token: str = self._get_env_var("PLEX_TOKEN")
        self.plex_anime_library: str = self._get_env_var("PLEX_ANIME_LIBRARY")
        self.plex_anime_name: str = self._get_env_var("PLEX_ANIME_NAME")

    @staticmethod
    def _get_env_var(
        key: str,
        required: bool = False,
        default: str = "",
    ) -> str:
        """Helper method to get and validate environment variables."""
        value = os.environ.get(key, default)
        if required and value is None:
            logger.error(f"{key} must be set")
            sys.exit(1)
        try:
            return value
        except ValueError:
            logger.error(f"Invalid value for {key}: {value}")
            sys.exit(1)


USER_CONFIG = UserConfig()

"""
Configuration constants for the application.

Attributes:
    listen_address (str): The IP address to listen on. Defaults to 0.0.0.0.
    listen_port (int): The port to listen on. Defaults to 7979.
    anime_name (str): The name of the anime to fetch filler episodes for.
    sonarr_url (str): The URL of the Sonarr server.
    sonarr_series_id (int): The ID of the Sonarr series to update.
    sonarr_api_key (str): The API key for the Sonarr server.
    plex_url (str): The URL of the Plex server. Optional.
    plex_token (str): The token for the Plex server. Optional.
    create_plex_collection (bool): Whether or not to create a Plex collection for the anime. Defaults to False.
    plex_anime_library (str): The name of the Plex library to add the anime collection to.
"""

import os
import sys
import logging

from dotenv import load_dotenv


load_dotenv(dotenv_path=".env.priv")

logging.basicConfig(level=logging.INFO)


class UserConfig:
    """Configuration constants for the application."""

    def __init__(self):
        self.listen_address: str = self._get_env_var(
            "ADDRESS", default="0.0.0.0"
        )
        self.listen_port: int = int(self._get_env_var(
            "PORT", default="7979"
        ))
        self.anime_name: str = self._get_env_var("ANIME_NAME", required=True)
        self.sonarr_url: str = self._get_env_var("SONARR_URL", required=True)
        self.sonarr_series_id: int = int(self._get_env_var(
            "SONARR_SERIES_ID", required=True, default=""
        ))
        self.sonarr_api_key: str = self._get_env_var("SONARR_API_KEY", required=True)
        self.monitor_sonarr_episodes: bool = bool(
            self._get_env_var("MONITOR_NON_FILLER_EPISODES", default=""
        ))
        self.plex_url: str = self._get_env_var("PLEX_URL")
        self.plex_token: str = self._get_env_var(
            "PLEX_TOKEN", required=bool(self.plex_url)
        )
        self.create_plex_collection: bool = bool(self._get_env_var(
            "CREATE_PLEX_COLLECTION", default=""
        ))
        self.plex_anime_library: str = self._get_env_var("PLEX_ANIME_LIBRARY")

    @staticmethod
    def _get_env_var(
        key: str,
        required: bool = False,
        default: str = "",
    ) -> str:
        """Helper method to get and validate environment variables."""
        value = os.environ.get(key, default)
        if required and value is None:
            logging.error(f"{key} must be set")
            sys.exit(1)
        try:
            return value
        except ValueError:
            logging.error(f"Invalid value for {key}: {value}")
            sys.exit(1)

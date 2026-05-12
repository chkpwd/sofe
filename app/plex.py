import logging

from typing import Any

try:
    from plexapi.video import Episode
    from plexapi.server import PlexServer
    from plexapi.base import MediaContainer
    from plexapi.library import ShowSection
except ModuleNotFoundError:
    Episode = Any
    PlexServer = None
    MediaContainer = Any
    ShowSection = Any

from app.variables import USER_CONFIG


logger = logging.getLogger(__name__)


def _get_plex_server():
    if PlexServer is None:
        logger.warning("Plex features disabled: plexapi is not installed.")
        return None

    if not USER_CONFIG.plex_url or not USER_CONFIG.plex_token:
        logger.warning("Plex features disabled: PLEX_URL or PLEX_TOKEN not configured.")
        return None

    try:
        return PlexServer(baseurl=USER_CONFIG.plex_url, token=USER_CONFIG.plex_token)
    except Exception as err:
        logger.warning(f"Plex unavailable; skipping Plex operations: {err}")
        return None


def create_plex_collection(collection_items: list[str] | None = None):
    if collection_items is None:
        collection_items = []

    plex = _get_plex_server()
    if plex is None:
        return

    if not USER_CONFIG.plex_anime_library or not USER_CONFIG.plex_anime_name:
        logger.warning(
            "Plex features disabled: PLEX_ANIME_LIBRARY or PLEX_ANIME_NAME not configured."
        )
        return

    nonfillers_items: list[Episode] = []
    fillers_items: list[Episode] = []

    media: ShowSection = plex.library.section(title=USER_CONFIG.plex_anime_library)

    shows: MediaContainer = media.search(title=USER_CONFIG.plex_anime_name)

    for show in shows:
        plex_episodes: list[Episode] = show.episodes()

        for episode in plex_episodes:
            if episode.seasonEpisode in collection_items:
                nonfillers_items.append(episode)
            else:
                fillers_items.append(episode)

        # create collections if they don't exist
        for items, collection_name in [
            (nonfillers_items, f"{show.title} - Non-Filler Episodes"),
            (fillers_items, f"{show.title} - Filler Episodes"),
        ]:
            if not plex.library.search(title=collection_name):
                if items:
                    plex.createCollection(
                        title=collection_name,
                        section=USER_CONFIG.plex_anime_library,
                        items=items,
                    )
                else:
                    logger.info(f"No {collection_name.split(' - ')[1].lower()} found.")

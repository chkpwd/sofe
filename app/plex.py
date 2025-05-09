import logging

from plexapi.video import Episode
from plexapi.server import PlexServer
from plexapi.base import MediaContainer
from plexapi.library import ShowSection

from app.variables import USER_CONFIG


logger = logging.getLogger(__name__)

plex = PlexServer(baseurl=USER_CONFIG.plex_url, token=USER_CONFIG.plex_token)


def create_plex_collection(collection_items: list[str] = []):
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

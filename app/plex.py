import logging

from plexapi.collection import Collection
from plexapi.video import Episode
from plexapi.server import PlexServer
from plexapi.base import MediaContainer
from plexapi.library import ShowSection
from constants.variables import UserConfig

var = UserConfig()

logging.basicConfig(level=logging.INFO)

plex = PlexServer(baseurl=var.plex_url, token=var.plex_token)

def create_plex_collection(sonarr_episodes: list[int], fillers: list[int] = []):
    nonfillers_items: list[Episode] = []

    media: ShowSection = plex.library.section(title=var.plex_anime_library)

    shows: MediaContainer = media.search(title=var.anime_name)

    for show in shows:
        show_name: str = show.title
        plex_episodes: list[Episode] = show.episodes()

        for episode in plex_episodes:
            if episode.episodeNumber not in fillers:
                nonfillers_items.append(episode)

        if nonfillers_items:
            plex.createCollection(
                title=f"{show_name} - Non-Filler Episodes", # FIXME: title gets modified for some reason
                section=var.plex_anime_library,
                items=nonfillers_items,
            )
        else:
            logging.info("No non-filler episodes found.")

# # Create a smart collection
# collection = plex.createCollection(
#     title="Recently Aired Comedy TV Shows",
#     section="TV Shows",
#     smart=True,
#     sort="episode.originallyAvailableAt:desc",
#     filters={"episode.originallyAvailableAt>>": "4w", "genre": "comedy"},
# )

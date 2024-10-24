import os
import sys
import logging

from flask import Flask, jsonify
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

app = Flask(__name__)

@app.route("/fillers", methods=["GET"])
def get_filler_list():
    """Returns the filler list for the specified anime."""
    filler_list = get_anime_filler_list(anime_name=var.anime_name)
    return jsonify({"value": filler_list})

if __name__ == "__main__":
    episodes_to_monitor = []

    logging.info("Initializing SOFE API...")
    logging.info("Address is set to '%s'", var.listen_address)
    logging.info("Port is set to '%s'", var.listen_port)

    fillers_from_api = get_anime_filler_list(var.anime_name)
    sonarr_episodes = get_sonarr_episodes(int(var.sonarr_series_id))

    if var.create_plex_collection is True:
        create_plex_collection(sonarr_episodes=sonarr_episodes, fillers=fillers_from_api)

    for episode in sonarr_episodes:
        if episode['number'] not in fillers_from_api:
            episodes_to_monitor.append(episode.get('id'))

    logging.debug("Non-Filler Episodes: %s", episodes_to_monitor)
    configure_monitoring(monitored_list=episodes_to_monitor)

    app.run(host=var.listen_address, port=var.listen_port)

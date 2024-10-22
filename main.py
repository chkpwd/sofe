import os
import sys
import logging

from flask import Flask, jsonify
from app.parser import get_anime_filler_list
from app.sonarr import configure_monitoring, get_sonarr_episodes
from constants.logging import LOG_LEVELS

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
    filler_list = get_anime_filler_list(anime_name=os.environ["ANIME_NAME"])
    return jsonify({"value": filler_list})

if __name__ == "__main__":
    logging.info("Initializing SOFE API...")
    result  = []

    listen_address = os.environ.get("ADDRESS", "0.0.0.0")
    listen_port = os.environ.get("PORT", 7979)

    if not os.environ.get("ANIME_NAME"):
        logging.error("ANIME_NAME must be set")
        sys.exit(1)

    if not os.environ.get("SONARR_SERIES_ID"):
        logging.error("SERIES_ID must be set")
        sys.exit(1)

    if not os.environ.get("SONARR_API_KEY"):
        logging.error("SONARR_API_KEY not set")
        sys.exit(1)

    if not os.environ.get("ADDRESS"):
        logging.info("Address is not set. Defaulting to 0.0.0.0.")
    else:
        logging.info("Address is set to '%s'", listen_address)

    if not os.environ.get("PORT"):
        logging.info("Port is not set. Defaulting to 7979.")
    else:
        logging.info("Port is set to '%s'", listen_port)

    fillers = get_anime_filler_list(os.environ["ANIME_NAME"])
    episodes = get_sonarr_episodes(int(os.environ["SONARR_SERIES_ID"]))

    for episode in episodes:
        if episode['number'] not in fillers:
            result.append(episode.get('id'))

    configure_monitoring(result)

    app.run(host=listen_address, port=int(listen_port))


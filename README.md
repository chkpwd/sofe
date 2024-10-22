# SoFE (Sonarr Anime Filler Excluder)

The SoFE (Sonarr Anime Filler Excluder) is a Python application designed to collect real-time anime data from [AnimeFillerList](https://www.animefillerlist.com/), such as filler episodes, and configure Anime to only monitor non-filler episodes. Additionally, expose data as metrics that can be scraped by Prometheus. As well, in conjunction with visualization tools like Grafana.

## Features

- Fetch and expose information about filler episodes for various anime shows.
- Expose anime-related metrics for monitoring and analysis.
- Easy integration with Prometheus and Grafana for visualization and alerting.

## Prerequisites

- Sonarr
- Docker / Docker Compose
- Prometheus server setup for collecting metrics. (Optional)

## Installation

The SoFE can be easily run as a container. This section covers pulling the Container Image from the GitHub Container Registry and running it.

### Pulling the Container Image

To pull the latest version of SoFE, use the following command:
```sh
docker pull ghcr.io/chkpwd/sofe:latest
```
Run the container:
```sh
docker run --rm -p 7979:7979 \
  -e SONARR_SERIES_ID=187 \
  -e ANIME_NAME="one-piece" \
  -e SONARR_API_KEY="your_api_key" \
  ghcr.io/chkpwd/sofe:latest
```
Alternatively, create docker-compose.yml file with the following content:
```yaml
version: '3.8'
services:
  sofe:
    image: ghcr.io/chkpwd/sofe:latest
    ports:
      - "7979:7979"
    environment:
      SONARR_SERIES_ID: 187
      ANIME_NAME: "one-piece"
      SONARR_API_KEY: "your_api_key"
```
Then run with:
```sh
docker-compose up -d
```
Accessing Data (Not done yet)

With the container running, you can access the exposed metrics by navigating to http://localhost:5000/fillers in your web browser or using a tool like curl:
```sh
curl http://<ip-address>:5000/fillers
```

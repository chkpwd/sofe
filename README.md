<p align="center">
  <img src="metadata/logo.png?raw=true" alt="Sofe's Logo"/>
</p>

<p align="center" >
  <picture><img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/chkpwd/sofe?style=flat&logo=github&logoColor=white&label=Stars"></picture>
  <picture><img alt="GitHub commit activity" src="https://img.shields.io/github/commit-activity/m/chkpwd/sofe?style=flat&logo=github&logoColor=white&label=COMMITS"></picture>
  <picture><img alt="GitHub Issues or Pull Requests" src="https://img.shields.io/github/issues-closed/chkpwd/sofe?style=flat&logo=github&logoColor=white"></picture>
  <picture><img alt="GitHub Issues or Pull Requests" src="https://img.shields.io/github/issues/chkpwd/sofe?style=flat&logo=github&logoColor=white"></picture>
  <picture><img alt="GitHub License" src="https://img.shields.io/github/license/chkpwd/sofe?style=flat"></picture>
</p>

SoFE (Sonarr Anime Filler Excluder) is a Python application that configures Sonarr to monitor only non-filler anime episodes sourced from [Anime Filler List](https://www.animefillerlist.com). It also creates separate Plex collections for non-filler and filler episodes, depending on the download status.

## Features

- Parses filler episodes from AnimeFillerList
- Monitors non-filler episodes in Sonarr
- Creates Plex Collections for non-filler and filler episodes

## Prerequisites

- Sonarr
- Plex
- Docker / Docker Compose

> [!Note]
> Make sure to obtain the anime name from [Anime Filler List](https://www.animefillerlist.com/) URL.

![alt text](./metadata/image.png)

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
  -e SONARR_URL="https://sonarr.local" \
  -e SONARR_API_KEY="<your_api_key>" \
  -e SONARR_SERIES_ID="187" \
  -e AFL_ANIME_NAME="one-piece" \
  -e PLEX_URL="http://127.0.0.1:32400" \
  -e PLEX_TOKEN="<your_plex_token>" \
  -e CREATE_PLEX_COLLECTION="True" \
  -e MONITOR_NON_FILLER_SONARR_EPISODES="True" \
  -e PLEX_ANIME_LIBRARY="<your_plex_anime_library>" \
  ghcr.io/chkpwd/sofe:latest
```
[

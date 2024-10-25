import requests
from lxml import html
from constants.logger import logger, log_level, LOG_LEVELS


logger.setLevel(LOG_LEVELS[log_level])


def get_anime_filler_list(afl_anime_name: str):
    """Get the anime filler list."""

    base_url = f"https://www.animefillerlist.com/shows/{afl_anime_name}/"
    url = f"{base_url}"
    data = html.fromstring(requests.get(url).content)
    filler_ranges = data.xpath(
        '//div[@class="filler"]/span[@class="Episodes"]/a/text()'
    )

    fillers = []
    for text in filler_ranges:
        if "-" in text:
            start, end = map(int, text.split("-"))
            fillers.extend(range(start, end + 1))
        else:
            fillers.append(int(text))

    if logger.getEffectiveLevel() == logger.debug:
        logger.debug(filler_ranges)

    return fillers

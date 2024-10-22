from lxml import html
import logging
import requests


def get_anime_filler_list(anime_name: str):
    """Get the anime filler list."""

    base_url = f"https://www.animefillerlist.com/shows/{anime_name}/"
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

    if logging.getLogger().getEffectiveLevel() == logging.DEBUG:
        logging.debug(filler_ranges)

    return fillers

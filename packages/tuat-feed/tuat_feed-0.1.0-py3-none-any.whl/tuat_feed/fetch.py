from typing import List
from tuat_feed.post import Post, parse_post
import requests


def fetch(
    category: str = "all", url: str = "https://api.ihavenojob.work/tuat/"
) -> List[Post]:
    if category == "all":
        response = requests.get(url)
    elif category == "academic":
        response = requests.get(url + "academic")
    elif category == "campus":
        response = requests.get(url + "campus")
    else:
        raise ValueError(
            f'category must be one of "all", "academic" or "campus". {category} was supplied.'
        )

    try:
        feed = response.json()
        posts = []
        for p in feed:
            posts.append(parse_post(p))
        return posts
    except:
        pass

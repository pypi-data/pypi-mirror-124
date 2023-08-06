from dataclasses import dataclass
from datetime import datetime, date
from typing import Dict, List


@dataclass(repr=True, eq=True)
class Attachment:
    name: str
    url: str


@dataclass(repr=True)
class Post:
    post_id: int
    title: str
    description: str
    update_date: date
    show_date_start: date
    show_date_end: date
    author: str
    origin: str
    category: str
    attachment: List[Attachment]
    other: Dict[str, str]


def parse_post(post_raw) -> Post:
    post_data_raw: dict[str, str] = post_raw["data"]
    post_id = post_raw["id"]
    title = post_data_raw.pop("タイトル")
    description = post_data_raw.pop("本文")
    update_date_raw = post_data_raw.pop("最終更新日")
    update_date = datetime.strptime(update_date_raw[:-5], "%Y/%m/%d").date()
    show_date_raw = post_data_raw.pop("公開期間")
    show_date_start_raw, show_date_end_raw = show_date_raw.split(" 〜 ")
    show_date_start = datetime.strptime(show_date_start_raw[:-5], "%Y/%m/%d").date()
    show_date_end = datetime.strptime(show_date_end_raw[:-5], "%Y/%m/%d").date()
    author = post_data_raw.pop("担当者")
    origin = post_data_raw.pop("発信元")
    category = post_data_raw.pop("カテゴリー")
    attachment_raw = post_data_raw.pop("添付ファイル") if "添付ファイル" in post_data_raw else None
    attachment = []
    if attachment_raw is not None:
        for s in attachment_raw.split("\n"):
            name, url = s[1:-1].split("](")
            attachment.append(Attachment(name=name, url=url))
    return Post(
        post_id=post_id,
        title=title,
        description=description,
        update_date=update_date,
        show_date_start=show_date_start,
        show_date_end=show_date_end,
        author=author,
        origin=origin,
        category=category,
        attachment=attachment,
        other=post_data_raw,
    )

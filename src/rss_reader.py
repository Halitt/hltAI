import feedparser
from typing import List, Dict
import datetime
import time
import os, re

class RSSReader:
    LAST_TIME_FILE = "last_news_time.txt"

    def __init__(self, feed_url: str):
        self.feed_url = feed_url

    def _read_last_time(self) -> datetime.datetime | None:
        if not os.path.exists(self.LAST_TIME_FILE):
            return None
        with open(self.LAST_TIME_FILE, "r") as f:
            time_str = f.read().strip()
            if not time_str:
                return None
            try:
                return datetime.datetime.fromisoformat(time_str)
            except Exception:
                return None

    def _write_last_time(self, dt: datetime.datetime):
        with open(self.LAST_TIME_FILE, "w") as f:
            f.write(dt.isoformat())

    def fetch_latest(self) -> List[str]:
        news_items = []
        last_time = self._read_last_time()
        tz_gmt1 = datetime.timezone(datetime.timedelta(hours=1))
        newest_time = last_time
        
        feed = feedparser.parse(self.feed_url)
        for entry in feed.entries:
            pub_date_str = entry.get('published', entry.get('pubDate'))
            pub_date_utc = None
            parsed_struct = entry.get('published_parsed') or entry.get('updated_parsed')
            if isinstance(parsed_struct, time.struct_time):
                pub_date = datetime.datetime(
                    parsed_struct.tm_year,
                    parsed_struct.tm_mon,
                    parsed_struct.tm_mday,
                    parsed_struct.tm_hour,
                    parsed_struct.tm_min,
                    parsed_struct.tm_sec,
                    tzinfo=tz_gmt1
                )
                pub_date_utc = pub_date.astimezone(datetime.timezone.utc)
            elif isinstance(pub_date_str, str):
                try:
                    pub_date = datetime.datetime.strptime(pub_date_str, "%a, %d %b %Y %H:%M:%S %z")
                    pub_date_utc = pub_date.astimezone(datetime.timezone.utc)
                except Exception:
                    pub_date_utc = None
            if pub_date_utc:
                if (last_time is None) or (pub_date_utc > last_time):
                    news_items.append(entry.get('link'))
                    if (newest_time is None) or (pub_date_utc > newest_time):
                        newest_time = pub_date_utc

        if newest_time and (last_time is None or newest_time > last_time):
            self._write_last_time(newest_time)
        return news_items

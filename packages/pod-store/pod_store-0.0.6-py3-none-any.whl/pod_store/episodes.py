"""Podcast episodes tracked in the pod store.

Episode objects are created/managed using the `pod_store.podcasts.PodcastEpisodes`
class.
"""
import os
from datetime import datetime
from typing import Any, List, Optional, Type, TypeVar

import requests

from . import util

DOWNLOAD_CHUNK_SIZE = 2000

E = TypeVar("E", bound="Episode")


class Episode:
    """Podcast episode tracked in the store.

    id (str): store ID (parsed from RSS feed ID)
    download_path (str): where episode will be downloaded on file system
    episode_number (str): zero-padded episode number from podcast feed
    title (str): episode title
    short_description (str): short description of episode
    long_description (str): longer description of episode
    url (str): download URL
    tags (list): arbitrary text tags. `new` tag is used to determine if an episode has
        been downloaded yet.
    downloaded_at (datetime): if set to `None`, the episode hasn't been downloaded yet

    created_at (datetime)
    updated_at (datetime)
    """

    def __init__(
        self,
        id: str,
        download_path: str,
        episode_number: str,
        title: str,
        short_description: str,
        long_description: str,
        url: str,
        created_at: datetime,
        updated_at: datetime,
        tags: List[str] = None,
        downloaded_at: Optional[datetime] = None,
    ) -> None:
        self.id = id
        self.download_path = download_path
        self.episode_number = episode_number
        self.title = title
        self.short_description = short_description
        self.long_description = long_description
        self.url = url
        self.tags = tags or []
        self.created_at = created_at
        self.updated_at = updated_at
        self.downloaded_at = downloaded_at

    @classmethod
    def from_json(
        cls: Type[E],
        created_at: str,
        updated_at: str,
        downloaded_at: Optional[str] = None,
        **kwargs,
    ) -> E:
        """Load a `pod_store.episodes.Episode` object from json data.

        Parses `datetime` objects from json strings where appropriate.
        """
        created_at = util.parse_datetime_from_json(created_at)
        updated_at = util.parse_datetime_from_json(updated_at)
        downloaded_at = util.parse_datetime_from_json(downloaded_at)

        return cls(
            created_at=created_at,
            updated_at=updated_at,
            downloaded_at=downloaded_at,
            **kwargs,
        )

    def __eq__(self, other: Any) -> bool:
        try:
            other_json = other.to_json()
        except AttributeError:
            return False
        return self.to_json() == other_json

    def __repr__(self) -> str:
        return f"Episode({self.episode_number}, {self.title})"

    def download(self) -> None:
        """Download the audio file of the episode to the file system."""
        os.makedirs(os.path.dirname(self.download_path), exist_ok=True)

        resp = requests.get(self.url, stream=True)
        with open(self.download_path, "wb") as f:
            for chunk in resp.iter_content(DOWNLOAD_CHUNK_SIZE):
                f.write(chunk)
        self.downloaded_at = datetime.utcnow()
        self.untag("new")

    def update(self, **data: Any) -> None:
        """Update arbitrary attributes by passing in a dict."""
        for key, value in data.items():
            setattr(self, key, value)

    def tag(self, tag_name: str) -> None:
        """Apply a tag to the episode."""
        self.tags.append(tag_name)

    def untag(self, tag_name: str) -> None:
        """Remove a tag from the episode."""
        self.tags = [t for t in self.tags if t != tag_name]

    def to_json(self) -> dict:
        """Convert episode data into a json-able dict.

        Parses datetime fields into isoformat strings for json storage.
        """
        created_at = util.parse_datetime_to_json(self.created_at)
        updated_at = util.parse_datetime_to_json(self.updated_at)
        downloaded_at = util.parse_datetime_to_json(self.downloaded_at)

        return {
            "id": self.id,
            "download_path": self.download_path,
            "episode_number": self.episode_number,
            "title": self.title,
            "short_description": self.short_description,
            "long_description": self.long_description,
            "url": self.url,
            "tags": self.tags,
            "created_at": created_at,
            "updated_at": updated_at,
            "downloaded_at": downloaded_at,
        }

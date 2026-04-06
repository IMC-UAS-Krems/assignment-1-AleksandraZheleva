from __future__ import annotations

from datetime import date
from typing import Optional

from .artists import Artist


class Track:
    def __init__(self, track_id: str, title: str, duration_seconds: int, genre: str) -> None:
        self.track_id = track_id
        self.title = title
        self.duration_seconds = duration_seconds
        self.genre = genre

    def duration_minutes(self) -> float:
        return self.duration_seconds / 60.0

    def __str__(self) -> str:
        return f"{self.title}"

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}("
            f"track_id={self.track_id!r}, "
            f"title={self.title!r}, "
            f"duration_seconds={self.duration_seconds!r}, "
            f"genre={self.genre!r})"
        )


class Song(Track):
    def __init__(
        self,
        track_id: str,
        title: str,
        duration_seconds: int,
        genre: str,
        artist: Artist,
    ) -> None:
        super().__init__(track_id, title, duration_seconds, genre)
        self.artist = artist
        self.artist.add_track(self)


class SingleRelease(Song):
    def __init__(
        self,
        track_id: str,
        title: str,
        duration_seconds: int,
        genre: str,
        artist: Artist,
        release_date: date,
    ) -> None:
        super().__init__(track_id, title, duration_seconds, genre, artist)
        self.release_date = release_date


class AlbumTrack(Song):
    def __init__(
        self,
        track_id: str,
        title: str,
        duration_seconds: int,
        genre: str,
        artist: Artist,
        track_number: int,
        album: Optional["Album"] = None,
    ) -> None:
        super().__init__(track_id, title, duration_seconds, genre, artist)
        self.track_number = track_number
        self.album = album


class Podcast(Track):
    def __init__(
        self,
        track_id: str,
        title: str,
        duration_seconds: int,
        genre: str,
        host: str,
        description: str,
    ) -> None:
        super().__init__(track_id, title, duration_seconds, genre)
        self.host = host
        self.description = description


class NarrativeEpisode(Podcast):
    def __init__(
        self,
        track_id: str,
        title: str,
        duration_seconds: int,
        genre: str,
        host: str,
        description: str,
        season: int,
        episode_number: int,
    ) -> None:
        super().__init__(track_id, title, duration_seconds, genre, host, description)
        self.season = season
        self.episode_number = episode_number


class InterviewEpisode(Podcast):
    def __init__(
        self,
        track_id: str,
        title: str,
        duration_seconds: int,
        genre: str,
        host: str,
        description: str,
        guest: str,
    ) -> None:
        super().__init__(track_id, title, duration_seconds, genre, host, description)
        self.guest = guest


class AudiobookTrack(Track):
    def __init__(
        self,
        track_id: str,
        title: str,
        duration_seconds: int,
        genre: str,
        author: str,
        narrator: str,
    ) -> None:
        super().__init__(track_id, title, duration_seconds, genre)
        self.author = author
        self.narrator = narrator


from .albums import Album

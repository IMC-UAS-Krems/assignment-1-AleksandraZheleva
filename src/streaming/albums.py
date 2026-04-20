"""
albums.py
---------
Implement the Album class for collections of AlbumTrack objects.

Classes to implement:
  - Album
"""
from .artists import Artist
from .tracks import AlbumTrack


class Album:
    def __init__(self, album_id: str, title: str, artist: Artist, release_year: int):
        self.album_id = album_id
        self.title = title
        self.artist = artist
        self.release_year = release_year
        self.tracks: list[AlbumTrack] = []

    def add_track(self, track: AlbumTrack):
        if track not in self.tracks:
            track.album = self
            self.tracks.append(track)
            self.tracks.sort(key=lambda t: t.track_number)

    def track_ids(self) -> list[str]:
        return [track.track_id for track in self.tracks]

    def duration_seconds(self) -> int:
        return sum(track.duration_seconds for track in self.tracks)

    def __str__(self) -> str:
        return f"Album({self.title})"

    def __repr__(self) -> str:
        return (
            f"Album(album_id={self.album_id!r}, title={self.title!r}, "
            f"artist={self.artist.name!r}, release_year={self.release_year!r})"
        )

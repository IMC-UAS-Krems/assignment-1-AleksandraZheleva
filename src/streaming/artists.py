"""
artists.py
----------
Implement the Artist class representing musicians and content creators.

Classes to implement:
  - Artist
"""
from .tracks import Track
class Artist:
    def __init__(self, artist_id: str, name: str, genre: str) -> None:
        self.artist_id = artist_id
        self.name = name
        self.genre = genre
        self.tracks: list["Track"] = []

    def add_track(self, track: "Track"):
        if track not in self.tracks:
            self.tracks.append(track)

    def track_count(self) -> int:
        return len(self.tracks)

    def __str__(self) -> str:
        return f"Artist({self.name})"

    def __repr__(self) -> str:
        return f"Artist(artist_id={self.artist_id!r}, name={self.name!r}, genre={self.genre!r})"
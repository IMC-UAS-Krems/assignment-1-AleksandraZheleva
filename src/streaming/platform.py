"""
platform.py
-----------
Implement the central StreamingPlatform class that orchestrates all domain entities
and provides query methods for analytics.

Classes to implement:
  - StreamingPlatform
"""
from datetime import datetime

from .albums import Album
from .artists import Artist
from .playlists import Playlist, CollaborativePlaylist
from .sessions import ListeningSession
from .tracks import Track, Song
from .users import User, PremiumUser, FamilyMember

class StreamingPlatform:
    def __init__(self, name: str):
        self.name = name
        self._catalogue: dict[str, Track] = {}
        self._users: dict[str, User] = {}
        self._artists: dict[str, Artist] = {}
        self._albums: dict[str, Album] = {}
        self._playlists: dict[str, Playlist] = {}
        self._sessions: list[ListeningSession] = []

    def add_track(self, track: Track) :
        self._catalogue[track.track_id] = track

    def add_user(self, user: User):
        self._users[user.user_id] = user

    def add_artist(self, artist: Artist):
        self._artists[artist.artist_id] = artist

    def add_album(self, album: Album):
        self._albums[album.album_id] = album

    def add_playlist(self, playlist: Playlist):
        self._playlists[playlist.playlist_id] = playlist

    def record_session(self, session: ListeningSession):
        self._sessions.append(session)
        session.user.add_session(session)

    def get_track(self, track_id: str):
        return self._catalogue.get(track_id)

    def get_user(self, user_id: str):
        return self._users.get(user_id)

    def get_artist(self, artist_id: str):
        return self._artists.get(artist_id)

    def get_album(self, album_id: str):
        return self._albums.get(album_id)

    def all_users(self):
        return list(self._users.values())

    def all_tracks(self):
        return list(self._catalogue.values())

#Q1
    def total_listening_time_minutes(self, start: datetime, end: datetime) -> float:
        total_seconds = 0

        for session in self._sessions:
            if start <= session.timestamp <= end:
                total_seconds += session.duration_listened_seconds

        return total_seconds / 60.0

#Q2
    def avg_unique_tracks_per_premium_user(self, days: int = 30) -> float:
        premium_users = [
            user for user in self._users.values() if isinstance(user, PremiumUser)
        ]

        if not premium_users:
            return 0.0

        if not self._sessions:
            return 0.0

        latest_session_time = max(session.timestamp for session in self._sessions)
        start_time = latest_session_time - timedelta(days=days)

        total_unique = 0

        for user in premium_users:
            unique_track_ids = set()

            for session in user.sessions:
                if start_time <= session.timestamp <= latest_session_time:
                    unique_track_ids.add(session.track.track_id)

            total_unique += len(unique_track_ids)

        return total_unique / len(premium_users)

#Q3
    def track_with_most_distinct_listeners(self) -> Track | None:
        if not self._sessions:
            return None

        listeners_per_track: dict[str, set[str]] = {}

        for session in self._sessions:
            track_id = session.track.track_id
            user_id = session.user.user_id

            if track_id not in listeners_per_track:
                listeners_per_track[track_id] = set()

            listeners_per_track[track_id].add(user_id)

        best_track_id = None
        best_count = -1

        for track_id, listeners in listeners_per_track.items():
            if len(listeners) > best_count:
                best_count = len(listeners)
                best_track_id = track_id

        if best_track_id is None:
            return None

        return self._catalogue.get(best_track_id)

#Q4
    def avg_session_duration_by_user_type(self) -> list[tuple[str, float]]:
        grouped: dict[str, list[int]] = {}

        for session in self._sessions:
            type_name = type(session.user).__name__

            if type_name not in grouped:
                grouped[type_name] = []

            grouped[type_name].append(session.duration_listened_seconds)

        result = []
        for type_name, durations in grouped.items():
            average = sum(durations) / len(durations)
            result.append((type_name, average))

        result.sort(key=lambda item: item[1], reverse=True)
        return result

#Q5
    def total_listening_time_underage_sub_users_minutes(self, age_threshold: int = 18) -> float:
        total_seconds = 0

        for session in self._sessions:
            if isinstance(session.user, FamilyMember) and session.user.age < age_threshold:
                total_seconds += session.duration_listened_seconds

        return total_seconds / 60.0

#Q6
    def top_artists_by_listening_time(self, n: int = 5) -> list[tuple[Artist, float]]:
        artist_seconds: dict[Artist, int] = {}

        for session in self._sessions:
            if isinstance(session.track, Song):
                artist = session.track.artist
                if artist not in artist_seconds:
                    artist_seconds[artist] = 0
                artist_seconds[artist] += session.duration_listened_seconds

        ranked = sorted(
            artist_seconds.items(),
            key=lambda item: item[1],
            reverse=True,
        )

        return [(artist, seconds / 60.0) for artist, seconds in ranked[:n]]

#Q7
    def user_top_genre(self, user_id: str) -> tuple[str, float] | None:
        user = self.get_user(user_id)

        if user is None:
            return None

        if not user.sessions:
            return None

        genre_seconds: dict[str, int] = {}
        total_seconds = 0

        for session in user.sessions:
            genre = session.track.genre

            if genre not in genre_seconds:
                genre_seconds[genre] = 0

            genre_seconds[genre] += session.duration_listened_seconds
            total_seconds += session.duration_listened_seconds

        if total_seconds == 0:
            return None

        top_genre = max(genre_seconds, key=genre_seconds.get)
        percentage = (genre_seconds[top_genre] / total_seconds) * 100

        return (top_genre, percentage)

#Q8
    def collaborative_playlists_with_many_artists(
        self, threshold: int = 3
    ) -> list[CollaborativePlaylist]:
        result: list[CollaborativePlaylist] = []

        for playlist in self._playlists.values():
            if isinstance(playlist, CollaborativePlaylist):
                artist_ids = set()

                for track in playlist.tracks:
                    if isinstance(track, Song):
                        artist_ids.add(track.artist.artist_id)

                if len(artist_ids) > threshold:
                    result.append(playlist)

        return result

#Q9
    def avg_tracks_per_playlist_type(self) -> dict[str, float]:
        normal_playlists: list[Playlist] = []
        collaborative_playlists: list[CollaborativePlaylist] = []

        for playlist in self._playlists.values():
            if isinstance(playlist, CollaborativePlaylist):
                collaborative_playlists.append(playlist)
            elif type(playlist) is Playlist:
                normal_playlists.append(playlist)

        playlist_avg = 0.0
        collaborative_avg = 0.0

        if normal_playlists:
            playlist_avg = sum(len(p.tracks) for p in normal_playlists) / len(normal_playlists)

        if collaborative_playlists:
            collaborative_avg = (
                sum(len(p.tracks) for p in collaborative_playlists)
                / len(collaborative_playlists)
            )

        return {
            "Playlist": playlist_avg,
            "CollaborativePlaylist": collaborative_avg,
        }

#Q10
    def users_who_completed_albums(self) -> list[tuple[User, list[str]]]:
        result: list[tuple[User, list[str]]] = []

        for user in self._users.values():
            listened_track_ids = {session.track.track_id for session in user.sessions}
            completed_album_titles: list[str] = []

            for album in self._albums.values():
                if not album.tracks:
                    continue

                all_tracks_listened = True

                for track in album.tracks:
                    if track.track_id not in listened_track_ids:
                        all_tracks_listened = False
                        break

                if all_tracks_listened:
                    completed_album_titles.append(album.title)

            if completed_album_titles:
                result.append((user, completed_album_titles))

        return result

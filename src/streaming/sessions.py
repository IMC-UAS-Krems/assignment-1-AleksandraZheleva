
from datetime import datetime
from .tracks import Track
from .users import User

class ListeningSession:
    def __init__(
        self,
        session_id: str,
        user: User,
        track: Track,
        timestamp: datetime,
        duration_listened_seconds: int,
    ):
        self.session_id = session_id
        self.user = user
        self.track = track
        self.timestamp = timestamp
        self.duration_listened_seconds = duration_listened_seconds

    def duration_listened_minutes(self) -> float:
        return self.duration_listened_seconds / 60.0

    def __str__(self) -> str:
        return f"Session({self.session_id})"

    def __repr__(self) -> str:
        return (
            f"ListeningSession(session_id={self.session_id!r}, "
            f"user={self.user.user_id!r}, track={self.track.track_id!r}, "
            f"timestamp={self.timestamp!r}, "
            f"duration_listened_seconds={self.duration_listened_seconds!r})"
        )
"""
users.py
--------
Implement the class hierarchy for platform users.

Classes to implement:
  - User (base class)
    - FreeUser
    - PremiumUser
    - FamilyAccountUser
    - FamilyMember
"""
from datetime import date
from .sessions import ListeningSession

class User:
    def __init__(self, user_id: str, name: str, age: int):
        self.user_id = user_id
        self.name = name
        self.age = age
        self.sessions: list["ListeningSession"] = []

    def add_session(self, session: "ListeningSession"):
        if session not in self.sessions:
            self.sessions.append(session)

    def total_listening_seconds(self) -> int:
        return sum(session.duration_listened_seconds for session in self.sessions)

    def total_listening_minutes(self) -> float:
        return self.total_listening_seconds() / 60.0

    def unique_tracks_listened(self) -> set[str]:
        return {session.track.track_id for session in self.sessions}

    def __str__(self) -> str:
        return f"{type(self).__name__}({self.name})"

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}(user_id={self.user_id!r}, "
            f"name={self.name!r}, age={self.age!r})"
        )

class FreeUser(User):
    MAX_SKIPS_PER_HOUR = 6

class PremiumUser(User):
    def __init__(self, user_id: str, name: str, age: int, subscription_start: date):
        super().__init__(user_id, name, age)
        self.subscription_start = subscription_start

class FamilyAccountUser(User):
    def __init__(self, user_id: str, name: str, age: int, subscription_start: date):
        super().__init__(user_id, name, age)
        self.subscription_start = subscription_start
        self.sub_users: list["FamilyMember"] = []

    def add_sub_user(self, sub_user: "FamilyMember"):
        if sub_user not in self.sub_users:
            self.sub_users.append(sub_user)
            sub_user.parent = self

    def all_members(self) -> list[User]:
        return [self] + self.sub_users

class FamilyMember(User):
    def __init__(
        self,
        user_id: str,
        name: str,
        age: int,
        parent: FamilyAccountUser | None = None,
    ):
        super().__init__(user_id, name, age)
        self.parent = None

        if parent is not None:
            parent.add_sub_user(self)



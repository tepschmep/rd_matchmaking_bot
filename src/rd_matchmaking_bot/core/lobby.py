from dataclasses import dataclass, field
from rd_matchmaking_bot.core import DictEntry


@dataclass
class Lobby(DictEntry):
    host_id: str
    message_id: str

    status: int = 0

    players: dict = field(default_factory=dict)

    def to_dict(self, exclude: list[str] = None) -> dict:
        return super().to_dict(exclude=["players"])
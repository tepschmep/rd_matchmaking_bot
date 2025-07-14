from dataclasses import dataclass, field
from rd_matchmaking_bot.core import DictEntry, User


@dataclass
class Lobby(DictEntry):
    host_id: str
    message_id: str

    status: int = 0

    players: dict = field(default_factory=dict)


    def swap_host(self, new_host: User):
        self.host_id = new_host.key


    def add_player(self, user: User):
        self.players |= { user.key: { "ready_status": 0, "miss_count": -1 } }


    def remove_player(self, user: User):
        self.players.pop(user.key)


    def to_dict(self, exclude: list[str] = None) -> dict:
        return super().to_dict(exclude=["players"])
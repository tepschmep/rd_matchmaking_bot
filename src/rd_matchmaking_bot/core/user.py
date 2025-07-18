from dataclasses import dataclass, field
from rd_matchmaking_bot.core import DictEntry


@dataclass
class User(DictEntry):
    xp: int = 0
    matches_played: int = 0

    players_won: int = 0
    players_beaten: list[str] = field(default_factory=list)

    current_lobby: str = None


    def in_lobby(self, lobby_name: str = None):

        return (self.current_lobby is not None
                if lobby_name is None else
                self.current_lobby == lobby_name)
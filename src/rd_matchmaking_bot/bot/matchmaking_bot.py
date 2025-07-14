from discord import Bot
from rd_matchmaking_bot.core import User, Lobby
import rd_matchmaking_bot.utils.data as data


class MatchmakingBot(Bot):
    def __init__(self, *cogs: str):
        super().__init__()

        self.load_cogs(*cogs)

        self.user_dict = {}
        self.save_dict = {}
        self.lobby_dict = {}
        self.load_data()


    def load_cogs(self, *cogs: str) -> None:
        for cog in cogs:
            self.load_extension(f"rd_matchmaking_bot.bot.cogs.{cog}")


    def load_data(self):
        path = data.get_path("resources/data")

        users_contents = data.read_file(path, "users.json")
        self.user_dict = {uid: User.from_dict(uid, user) for uid, user in users_contents.items()}

        lobbies_contents = data.read_file(path, "lobbies.json")
        self.lobby_dict = {name: Lobby.from_dict(name, lobby) for name, lobby in lobbies_contents.items()}

        self.save_dict = data.read_file(path, "rdsaves.json")


    def update_data(self):
        path = data.get_path("resources/data")

        user_dict = {}
        for user in self.user_dict.values():
            user_dict |= user.to_dict()
        data.write_json(user_dict, path, "users.json")

        lobby_dict = {}
        for lobby in self.lobby_dict.values():
            lobby_dict |= lobby.to_dict()
        data.write_json(lobby_dict, path, "lobbies.json")

        data.write_json(self.save_dict, path, "rdsaves.json")


    def get_user_id(self, ctx) -> str:
        uid = str(ctx.user.id)

        if uid not in self.user_dict:
            self.user_dict[uid] = User(uid)

        return uid

    async def on_ready(self):
        print(f"{self.user.name} is alive!")
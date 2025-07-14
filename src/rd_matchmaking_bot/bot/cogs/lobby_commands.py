import discord
from discord.ext import commands
from rd_matchmaking_bot.core import Lobby
from rd_matchmaking_bot import MatchmakingBot


class LobbyCommands(commands.Cog):
    lobby = discord.SlashCommandGroup("lobby", "Lobby commands")


    def __init__(self, bot: MatchmakingBot):
        self.bot = bot


    @lobby.command(description="Create a lobby")
    async def create(self, ctx,
                     name: discord.Option(str, description="Lobby name"),
                     auto_join: discord.Option(bool, default=True, description="Whether or not to join the lobby")):
        uid = self.bot.get_user_id(ctx)
        user = self.bot.user_dict[uid]

        if user.in_lobby():
            await ctx.respond(f"Unable to create: you are already in the lobby `{user.current_lobby}`.", ephemeral=True)
            return

        if name in self.bot.lobby_dict:
            await ctx.respond(f"Unable to create: the name `{name}` is already in use.", ephemeral=True)
            return

        lobby_message: discord.Message = await ctx.channel.send(f"Creating lobby: `{name}`...")
        new_lobby = Lobby(name, uid, str(lobby_message.id))

        if auto_join:
            new_lobby.add_player(user)

        self.bot.lobby_dict[name] = new_lobby
        self.bot.update_data()

        await lobby_message.edit(content=f"Lobby `{name}`: tbd\nPlayers: {new_lobby.players}") # -> Edit lobby_message into something beautiful
        await ctx.respond("Lobby created!", ephemeral=True)


def setup(bot: MatchmakingBot):
    cog = LobbyCommands(bot)
    bot.add_cog(cog)
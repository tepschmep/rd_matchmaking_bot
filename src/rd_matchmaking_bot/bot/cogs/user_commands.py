import json
import discord
from discord import Attachment
from discord.ext import commands
from rd_matchmaking_bot import MatchmakingBot


class UserCommands(commands.Cog):
    def __init__(self, bot: MatchmakingBot):
        self.bot = bot

    @discord.slash_command()
    async def debug(self, ctx):
        await ctx.respond(f"Users:\n{self.bot.user_dict}\n\nLobbies:\n{self.bot.lobby_dict}\n\nUser rdsettings saved:\n{self.bot.save_dict.keys()}")


    @discord.slash_command(description="Upload your \"settings.rdsave\" file, located in the \"User\" directory of your RD installation")
    async def upload_rdsave(self, ctx,
                            attachment: discord.Option(Attachment, description="settings.rdsave file")):
        if attachment.filename == "settings.rdsave":
            uid = self.bot.get_user_id(ctx)

            file = await attachment.read()
            rdsave = json.loads((file.decode('utf-8-sig')).encode('utf-8'))

            played_levels = []
            for level, rank in rdsave.items():
                is_custom = level.startswith("CustomLevel_") and level.endswith("_normal")
                was_played = rank != "NotFinished"

                if is_custom and was_played:
                    level_hash = level[12:-7]
                    played_levels.append(level_hash)

            self.bot.save_dict[uid] = played_levels
            self.bot.update_data()

            await ctx.respond("Your `settings.rdsave` file was updated!", ephemeral=True)
        else:
            await ctx.respond(f"`{attachment.filename}` is an invalid file. Make sure it's an `settings.rdsave`!", ephemeral=True)


def setup(bot: MatchmakingBot):
    cog = UserCommands(bot)
    bot.add_cog(cog)
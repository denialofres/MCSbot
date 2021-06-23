import discord, os, datetime, asyncio
from discord.ext import commands, tasks
from discord import Embed

print("imported modules")

intents = discord.Intents.all()
bot = commands.Bot("+", intents=intents)

class vc_roles(commands.Cog):
    @tasks.loop(seconds=30.0)
    async def voice_chat_monitoring(self) -> None:

        for guild in bot.guilds:

            for channel in guild.voice_channels:

                if channel.id not in self.roles:
                    role = await guild.create_role(name=channel.name, mentionable=True)
                    self.roles[channel.id] = role.id

                else:
                    role = discord.utils.find(lambda m: m.id == self.roles[channel.id], guild.roles)

                for member in channel.members:
                    if member not in role.members:
                        await member.add_roles(role, reason=f"joined vc: {channel.name} at {datetime.datetime.now()}")
                    
                for member in role.members:
                    if member not in channel.members:
                        await member.remove_roles(role, reason=f"left vc: {channel.name} at {datetime.datetime.now()}")

    def cog_unload(self):
        for channel, role in self.roles.items():
            role = discord.utils.find(lambda m: m.id == role, channel.guild.roles)
            asyncio.run(role.delete(reason="removed section"))
        return super().cog_unload()

    async def __init__(self, bot):
        self.bot = bot
        self.roles = {}
        print(f"Logged in as {bot.user} ({bot.user.id})")
        self.voice_chat_monitoring.start()


if __name__ == "__main__":
    bot.add_cog(vc_roles(bot))
    bot.run("")
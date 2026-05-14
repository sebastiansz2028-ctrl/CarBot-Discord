#Imports
import os
import discord
import dotenv
from dotenv import load_dotenv
from discord.ext import commands
load_dotenv()


#Variables


DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.all()
intents.message_content = True


#Bot Startup

class CarBot(commands.Bot):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        await self.tree.sync()
        print('Synced Commands Globally!')
        await self.tree.sync(guild=discord.Object(id=1504288510650093570))
        print('Synced Commands in Home Server!')


bot = CarBot(command_prefix="CB!", intents=intents)

#Commands


@bot.tree.command(name="ping", description="Check the bot's latency")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Latency: {round(bot.latency * 1000)}ms")


@bot.tree.command(name="profile", description="Check out a discord profile!")
async def profile_checker(interaction: discord.Interaction, user: discord.Member):
    embed_profile = discord.Embed()
    await interaction.response.defer(ephemeral=False)
    #Create and set up embed
    embed_profile.title = f"{user.display_name}"
    embed_profile.description = f"{user.name}"
    embed_profile.add_field(name="User ID:", value=f"{user.id}")
    embed_profile.set_image(url=f"{user.display_avatar.url}")
    await interaction.followup.send(embed=embed_profile)


#Loop
bot.run(DISCORD_TOKEN)

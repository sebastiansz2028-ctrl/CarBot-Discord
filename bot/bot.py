#Imports
import os
import datetime
import discord
import dotenv
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands
from datetime import timedelta, datetime
load_dotenv()


#Variables
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.all()
intents.message_content = True

#Functions
def signature_print():
    return datetime.now().strftime('[%Y-%m-%d %H:%M:%S]') + " [CarBot] "

#Bot Startup
class CarBot(commands.Bot):
    async def on_ready(self):
        print(signature_print() + f'Logged on as {self.user}!')
        await self.tree.sync()
        print(signature_print() + 'Synced Commands Globally!')
        await self.tree.sync(guild=discord.Object(id=1504288510650093570))
        print(signature_print() + 'Synced Commands in Home Server!')
        await bot.change_presence(activity=discord.Game(name="In Development"))
        print(signature_print() + f"{bot.user.name} presence set!")


bot = CarBot(command_prefix='CB!', intents=intents)

#Error Handler
@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error):
    err_msg = ""
    print(signature_print() + f"Error: {str(error)}")
    if isinstance(error, app_commands.CommandInvokeError):
        error = error.original
        err_msg = "An error has occurred, please try again."
    elif isinstance(error, app_commands.MissingPermissions):
        err_msg = "You do not have the necessary permission(s) for this command."
    elif isinstance(error, app_commands.BotMissingPermissions):
        err_msg = "Bot does not have required permission(s)."
    elif isinstance(error, discord.HTTPException):
        err_msg = "An HTTP Exception has occurred, try again."
    elif isinstance(error, discord.HTTPException) and error.status == 429:
        err_msg = "We are being rate limited, please try again after a couple seconds."
    else:
        err_msg = f"A fatal error has occurred: {str(error)}"


    if interaction.response.is_done():
        await interaction.followup.send(f"{err_msg}", ephemeral=True)
    else:
        await interaction.response.send_message(f"{err_msg}", ephemeral=True)

#Commands
@bot.tree.command(name="ping", description="Check the bot's latency")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Latency: {round(bot.latency * 1000)}ms")


@bot.tree.command(name="profile", description="Check out a discord profile!")
@app_commands.describe(user="User's profile to fetch")
async def profile_checker(interaction: discord.Interaction, user: discord.Member):
    await interaction.response.defer(ephemeral=False)
    fetch_user = await bot.fetch_user(user.id)
    #Initialize Embed w/ title and color for main profile
    embed_profile = discord.Embed(title=f"Profile of {user.display_name}", color=discord.Color.dark_orange())
    #Add to embed_profile
    embed_profile.add_field(name="Display Name:", value=f"{user.display_name}")
    embed_profile.add_field(name="User Name:", value=f"{user.name}", inline=False)
    embed_profile.add_field(name="User ID:", value=f"`{user.id}`", inline=False)
    embed_profile.add_field(name="Joined Discord:", value=f"{user.created_at.strftime('%Y-%m-%d')}", inline=False)
    embed_profile.add_field(name="User Profile:", value="", inline=False)
    embed_profile.set_image(url=f"{user.display_avatar.url}")
    await interaction.followup.send(embed=embed_profile)

    #Initialize Another Embed w/ title and color for banner
    embed_profile_banner = discord.Embed(title=f"{user.display_name}'s banner")
    #Checks if user has a custom banner and if not, does not send an image
    #Bots don't seem to work.
    if fetch_user.banner is not None:
        embed_profile_banner.add_field(name="User Banner:", value="\u200b", inline=False)
        embed_profile_banner.set_image(url=f"{fetch_user.banner.url}")
    else:
        embed_profile_banner.add_field(name="User does not have a banner", value="\u200b", inline=False)
    await interaction.followup.send(embed=embed_profile_banner)

@bot.tree.command(name="printer", description="Bot repeats whatever you input!")
async def printer(interaction: discord.Interaction, msg: str):
    await interaction.response.send_message(f"'{msg}' \n-# -By {interaction.user.name}")

@bot.tree.command(name="help", description="Shows commands.")
async def help_cmd(interaction: discord.Interaction):
    embed_help_cmd = discord.Embed(title="Help", color=discord.Color.purple(), description="Commands:")
    embed_help_cmd.add_field(name="Profile", value="Check some basic info about someones profile!")
    embed_help_cmd.add_field(name="Printer", value="Prints message you input!", inline=False)
    embed_help_cmd.add_field(name="Ping", value="Shows bot latency.", inline=False)
    await interaction.response.send_message(embed=embed_help_cmd)

@bot.tree.command(name="purge", description="Purge messages")
@app_commands.describe(amount="How many messages you want to purge (1-100)")
@app_commands.checks.has_permissions(manage_messages=True)
async def purge(interaction: discord.Interaction, amount: int):
    await interaction.response.defer(ephemeral=True)

    if 100 > amount < 1:
        await interaction.followup.send("Whoa, that is over/under the limit.", ephemeral=True)
    else:
        deleted_msg = await interaction.channel.purge(limit=amount, reason=f"{interaction.user} used purge command.", check=lambda msg: not msg.pinned)
        await interaction.followup.send(f"{len(deleted_msg)} message(s) deleted.", ephemeral=True)


#Loop
bot.run(DISCORD_TOKEN)

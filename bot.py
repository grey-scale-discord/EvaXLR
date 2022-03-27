import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from developers.cog_manager import CogManager
load_dotenv()

intents = discord.Intents.default()
intents.members = True

token = os.getenv("TOKEN")
bot = commands.Bot(
    command_prefix = "$",
    intents=intents
)

category_list = [
    "economy",
    "moderation",
]
cog_manager = CogManager(bot, category_list)
cog_manager.load_all()

# Cog Manager Discord Interface (Developer Tool)
@bot.command(aliases = ["load_all", "load", "l"])
async def _load_all_cogs(ctx):
    try:
        cog_manager.load_all()
        await ctx.send("All cogs has been loaded.")
    except discord.ext.commands.errors.ExtensionAlreadyLoaded:
        await ctx.send("All the cogs are already loaded.")

@bot.command(aliases = ["unload_all", "unload", "u"])
async def _unload_all_cogs(ctx):
    try:
        cog_manager.unload_all()
        await ctx.send("All cogs has been unloaded.")
    except discord.ext.commands.errors.ExtensionNotLoaded:
        await ctx.send("All the cogs are already not loaded.")

@bot.command(aliases = ["reload_all", "reload", "r"])
async def _reload_all_cogs(ctx):
    cog_manager.reload_all()
    await ctx.send("All cogs has been reloaded.")

bot.run(token)

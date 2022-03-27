import os
import discord
from discord.ext import commands

class CogManager():
    def __init__(self, bot, category_list):
        self.bot = bot
        self.category_list = category_list
    
    def load_category(self, category):
        for filename in os.listdir(f"./cogs/{ category }"):
            if filename.endswith('.py'):
                self.bot.load_extension(f'cogs.{ category }.{ filename[:-3] }')

    def unload_category(self, category):
        for filename in os.listdir(f"./cogs/{ category }"):
            if filename.endswith('.py'):
                self.bot.unload_extension(f'cogs.{ category }.{ filename[:-3] }')

    def load_all(self):
        self.bot.load_extension("cogs.initialize")
        for category in self.category_list:
            self.load_category(category)

    def unload_all(self):
        self.bot.unload_extension("cogs.initialize")
        for category in self.category_list:
            self.unload_category(category)

    def reload_all(self):
        try:
            self.unload_all()
        except discord.ext.commands.errors.ExtensionNotLoaded:
            # Pass if cogs were already unloaded
            pass 
        finally:
            self.load_all()
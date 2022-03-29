import time
import discord
from discord.ext import commands
import json


def get_afk_data():
	with open("cogs/moderation/afklist.json" , "r") as f:
		users = json.load(f)
	return users

class Afk(commands.Cog):
	def __init__(self , bot):
		self.author = None
		self.bot = bot

	@commands.command(aliases = ["afk"])
	async def _afk(self , ctx , reason = None):
		try:
			users = get_afk_data()

			users[str(ctx.author.name)] = {}
			users[str(ctx.author.name)]["user_id"] = ctx.author.id
			users[str(ctx.author.name)]["reason"] = reason if reason!= None else None

			with open("cogs/moderation/afklist.json" , "w") as f:
				json.dump(users , f , indent = 2)

			await ctx.send(f" {ctx.author.mention} ``is now Afk``- {reason}")
			self.initial = time.time()
			self.author = ctx.author
			self.reason = reason

		except discord.errors.Forbidden:
			await ctx.send("Error!")

	@commands.Cog.listener()
	async def on_message(self , message):
		users = get_afk_data()

		if message.author.name in users and "afk" not in message.content:
			self.final = time.time()

			time_afk_seconds = (self.final - self.initial)

			if time_afk_seconds > 60 :
				time_afk = f"{round(time_afk_seconds / 60)} Minutes"
			elif time_afk_seconds > 3600 :
				time_afk = f"{round(time_afk_seconds / 3600)} Hours"
			else:
				time_afk = f"{round(time_afk_seconds)} Seconds"

			del users[str(self.author.name)]

			with open("cogs/moderation/afklist.json", "w") as f:
				json.dump(users, f, indent=2)

			await message.channel.send(f"Welcome!{message.author.mention} You were afk for {time_afk}")

		mention = f"<@!{self.author.id}>"
		print(mention)
		if mention in message.content and self.author.name in users:
			await message.channel.send(f"{self.author.name}`` is Afk`` - {self.reason} ")

def setup(bot):
	bot.add_cog(Afk(bot))
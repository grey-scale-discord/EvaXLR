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

			_id = f"<@!{ctx.author.id}>"
			users[str(_id)] = {}
			users[str(_id)]["user_name"] = ctx.author.name
			users[str(_id)]["reason"] = reason if reason!= None else None

			with open("cogs/moderation/afklist.json" , "w") as f:
				json.dump(users , f , indent = 2)

			await ctx.send(f" {ctx.author.mention} ``is now Afk``- {reason}")
			self.initial = time.time()
			self._id = _id
			self.reason = reason

		except discord.errors.Forbidden:
			await ctx.send("Error!")

	@commands.Cog.listener()
	async def on_message(self , message):
		users = get_afk_data()

		re_id = f"<@!{message.author.id}>"
		if str(re_id) in users.keys() and "afk" not in message.content:

			final = time.time()
			time_afk_seconds = (final - self.initial)

			if time_afk_seconds >= 60 and time_afk_seconds < 3600:
				time_afk = f"{round(time_afk_seconds / 60)} Minutes"
			elif time_afk_seconds >= 3600:
				time_afk = f"{round(time_afk_seconds / 3600)} Hours"
			else:
				time_afk = f"{round(time_afk_seconds)} Seconds"

			del users[str(self._id)]

			with open("cogs/moderation/afklist.json", "w") as f:
				json.dump(users, f, indent=2)

			await message.channel.send(f"Welcome! {message.author.mention} You were Afk for {time_afk}")

		mention = [f"<@!{key}>" for key in users.keys()]

		for _mention in mention:
			if _mention in message.content:
				await message.channel.send(f'{users[str(_mention)]["user_id"]}`` is Afk`` - {users[str(key)]["reason"]} ')

def setup(bot):
	bot.add_cog(Afk(bot))

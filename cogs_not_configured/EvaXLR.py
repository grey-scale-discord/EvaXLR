import discord
from discord.ext import commands
import random
import json
import os

os.chdir("E:\\Discord Bot.py")


client = commands.Bot(command_prefix = "!")

@client.event
async def on_ready():
	print(f"{client.user.name} is ready!")

async def open_account(user):

	users = await get_bank_data()

	if str(user.id) in users:
		return False
	else:
		users[str(user.id)] = {}
		users[str(user.id)]["Wallet"] = 0

	with open("Economy System.json" , "w") as f:
		json.dump(users , f , indent = 2)
	return True

async def get_bank_data():
	with open("Economy System.json" , "r") as f:
		users = json.load(f)
	return users

class Economy_System:

	class Balance:
		@client.command()
		async def balance(ctx,user : discord.User):
			await open_account(user)
			
			users = await get_bank_data()

			wallet = users[str(user.id)]["Wallet"]

			em = discord.Embed(
				description = f":euro: | {user.mention}'s current Bank Balance is ${wallet}",
				color = 0x3498db
				)

			await ctx.send(embed = em)
		@balance.error
		async def error_balance(ctx: commands.Context , error : commands.CommandError):
			if isinstance(error,commands.MissingRequiredArgument):
				await open_account(ctx.author)
			
				users = await get_bank_data()

				wallet = users[str(ctx.author.id)]["Wallet"]

				em = discord.Embed(
					description = f":euro: | {ctx.author.mention}'s current Bank Balance is ${wallet}",
					color = 0x3498db
					)

				await ctx.send(embed = em)

		@client.command()
		async def beg(ctx):
			user = ctx.author
			await open_account(ctx.author)
			
			users = await get_bank_data() 

			case = int(random.choice([0,1]))

			if case == 0:
				embed = discord.Embed(
					description = f":x: | Seems like you are cursed by Evil Spirits. Better Luck Next time! Donation : $0" ,
					color = discord.Color.from_rgb(255, 255, 0)
				)
			elif case == 1:
				earnings = random.randrange(150)

				users[str(user.id)]["Wallet"] += earnings

				with open("Economy System.json","w") as f:
					json.dump(users,f)

				embed = discord.Embed(
					description = f":white_check_mark: | Congratulations! You got a donation of ${earnings}",
					color = discord.Color.from_rgb(255, 255, 0)
				)
			await ctx.send(embed = embed)

	class Donation:
		@client.command()
		async def donate(ctx, user : discord.User , amount):
			await open_account(user)
			users = await get_bank_data()

			users[str(ctx.author.id)]["Wallet"] -= int(amount)
			users[str(user.id)]["Wallet"] += int(amount)

			em = discord.Embed(
				description = f":white_check_mark: | {user.mention} received ${amount} from {ctx.author.mention}",
				color = discord.Color.green()
				)
			await ctx.send(embed = em)

			with open("Economy System.json" , "w") as f:
				json.dump(users , f ,indent=2)
		@donate.error
		async def error_donate(ctx: commands.Context , error : commands.CommandError):
			if isinstance(error, commands.MissingRequiredArgument):
				message = f":no_entry_sign: | {ctx.author.name} , Invalid Arguments"

			em = discord.Embed(
				description = message,
				color = discord.Color.red()
				)
			await ctx.send(embed = em)

	class Steal:
		@client.command() 
		async def steal(ctx , user : discord.User):
			await open_account(user)
			users = await get_bank_data()

			case = random.choice([0,1,2])

			if users[str(user.id)]["Wallet"] < 1000:
				bal = users[str(user.id)]["Wallet"]
				message = f":no_entry_sign: | Cannot Steal from {user.name} | Minimum Balance : $1000 , {user.name} has ${bal}"
				colour = discord.Color.red()
			elif case == 0:
				steal_percent = random.randint(2,15) 

				steal_am = users[str(user.id)]["Wallet"] * int(steal_percent) // 100

				users[str(ctx.author.id)]["Wallet"] += steal_am
				users[str(user.id)]["Wallet"] -= steal_am

				message = f":white_check_mark: | {ctx.author.name} stole ${steal_am} from {user.name}"
				colour = discord.Color.green()

			elif case == 1:
				penalty_percent = random.randint(2,20) 
				penalty = users[str(user.id)]["Wallet"] * int(penalty_percent) // 100

				users[str(ctx.author.id)]["Wallet"] -= penalty
				users[str(user.id)]["Wallet"] += penalty

				message = f":no_entry_sign: | Oh No! You were Caught by {user.name}. Penalty : ${penalty}"
				colour = discord.Color.red()

			elif case == 2:
				message = f":x: | Oh Poor {ctx.author.name}! You were unable to steal from {user.name}"
				colour = discord.Color.red()

			em = discord.Embed(
				description = message,
				color = colour
				)
			await ctx.send(embed = em)

			with open("Economy System.json" , "w") as f:
				json.dump(users,f,indent = 2)
		@steal.error 
		async def error_steal(ctx : commands.Context , error : commands.CommandError):
			if isinstance(error , commands.MissingRequiredArgument):
				message = f":no_entry_sign: | {ctx.author.name} , Invalid Arguments"

			em = discord.Embed(
				description = message,
				color = discord.Color.red()
				)
			await ctx.send(embed = em)

class Moderation:

	class kick:
		@client.command(aliases = ["kick"])
		@commands.has_permissions(kick_members = True)
		async def kick_member(ctx , user : discord.User , reason = None):
			try: 
				await ctx.guild.kick(user)

				em = discord.Embed(
					title = "Member Kicked",
					description = f"{user.name} was kicked from {ctx.guild}",
					color = discord.Color.red()
					)
				em.add_field(
					name = "Moderator",
					value = ctx.author.mention,
					inline = True
					)
				if reason != None:
					em.add_field(
						name = "Reason",
						value = reason,
						inline = True
						)
				await ctx.send(embed = em)
			except discord.errors.Forbidden:
				message = f":x: | oops! I cannot kick {user.name}"
				em = discord.Embed(
					description = message,
					color = discord.Color.red()
					)
				await ctx.send(embed = em)
		@kick_member.error 
		async def error_kick(ctx : commands.Context , error : commands.CommandError):
			if isinstance(error , commands.MissingRequiredArgument ):
				message = f":x: | Missing Required Argument : **{error.param.name.upper()}**"
			elif isinstance(error , commands.MissingPermissions):
				message = ":x: | You are missing the required permissions to run this command!"
			elif isinstance(error , commands.BadArgument):
				message = ":x: | User not found"
			else:
				message = ":x: | Error! Something went Wrong"

			em = discord.Embed(
				description = message,
				color = discord.Color.red()
				)
			await ctx.send(embed = em)


	class ban:
		@client.command(aliases = ["ban"])
		@commands.has_permissions(ban_members = True)
		async def ban_member(ctx , user : discord.User , reason = None):
			try: 
				await ctx.guild.ban(user)

				em = discord.Embed(
					title = "Member Kicked",
					description = f"{user.name} was banned from {ctx.guild}",
					color = discord.Color.red()
					)
				em.add_field(
					name = "Moderator",
					value = ctx.author.mention,
					inline = True
					)
				if reason != None:
					em.add_field(
						name = "Reason",
						value = reason,
						inline = True
						)
				await ctx.send(embed = em)
			except discord.errors.Forbidden:
				message = f":x: | oops! I cannot ban {user.name}"
				em = discord.Embed(
					description = message,
					color = discord.Color.red()
					)
				await ctx.send(embed = em)
		@ban_member.error 
		async def error_ban(ctx : commands.Context , error : commands.CommandError):
			if isinstance(error , commands.MissingRequiredArgument ):
				message = f":x: | Missing Required Argument : **{error.param.name.upper()}**"
			elif isinstance(error , commands.MissingPermissions):
				message = ":x: | You are missing the required permissions to run this command!"
			elif isinstance(error , commands.BadArgument):
				message = ":x: | User not found"
			else:
				message = ":x: | Error! Something went Wrong"

			em = discord.Embed(
				description = message,
				color = discord.Color.red()
				)
			await ctx.send(embed = em)











client.run('OTMzMTk0NjI3ODk1NDE0ODA0.Yed_OQ.GQEsS3WG9la3tQCkmW8o3xgy5w8')
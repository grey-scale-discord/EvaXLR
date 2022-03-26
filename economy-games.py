import email
import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import requests
import random
import asyncio
from dotenv import load_dotenv
import os
load_dotenv()

client = commands.Bot(command_prefix = "$")
url = "https://www.sacnilk.com/entertainmenttopbar/Top_500_Bollywood_Movies_Of_All_Time"

r = requests.get(url)
htmlContent = r.content
soup = BeautifulSoup(htmlContent , 'html.parser')

tgs = []
for tag in soup.find_all('a'):
    tgs.append(tag.text)

bollywood_movies = tgs[45:1045]


gifs = [
	"https://i.pinimg.com/originals/09/9a/57/099a57d2fe430ea56cdc5ed4979ff909.gif",
	"https://i.pinimg.com/originals/9b/da/90/9bda90c406615bfb08c1deee5eac12f0.gif",
	"https://i.pinimg.com/originals/5a/4b/42/5a4b42b5f67ad5ff2ee40e05b9f6791b.gif",
	"https://i.pinimg.com/originals/74/51/d6/7451d6db75d6ee321bfc88dcba21d157.gif",
	"https://i.pinimg.com/originals/fe/0e/21/fe0e21af0db0b29c33a866d16b7e5392.gif",
	"https://pa1.narvii.com/6085/f1c0e054e6cf2215ee577b19b49f0ff575eccd6f_hq.gif",
	"https://thumbs.gfycat.com/TightDeliciousCurassow-size_restricted.gif",
	"https://c.tenor.com/P7VCJlbT_bAAAAAC/anime-pink.gif",
	"https://c.tenor.com/-hvLFXU487AAAAAC/anime-pink.gif",
	"https://i.pinimg.com/originals/94/fa/4b/94fa4b126901a1a2b79951f0a62d6a6c.gif",
	"https://media0.giphy.com/media/GEkAU4EckSumA/200.gif?cid=95b279446d9d7ba976690f7ce405d6f4785e967a75f2ba75&rid=200.gif&ct=g",
	"https://c.tenor.com/cQAPfeSNRlYAAAAC/aesthetic-japan.gif",
	"https://thumbs.gfycat.com/IllfatedGreenBison-size_restricted.gif",
	"https://data.whicdn.com/images/354225933/original.gif",
	"https://data.whicdn.com/images/350786973/original.gif",
	"https://i.pinimg.com/originals/f5/6c/8b/f56c8bcf538d1ed7ee1a959f4a643173.gif",
	"https://data.whicdn.com/images/355689898/original.gif"
]

rules = """
1. Enter any alphabet as a Guess for the given Movie 
2. Guesses should be of Single Character 
3. There's a time limit of 60 seconds for Each Guess 
4. You get 15 chances to guess the movie 
5. If you are able to Guess it correctly , You get Currency between $(500-1000)
6. Unsuccessfull attempts will cost you $100
"""

@client.event
async def on_ready():
	print(f"{client.user.name} is ready!") 

def rules_embed():
	thumbnail = random.choice(gifs)
	embed = discord.Embed(
		title = "Guess the Movie",
		color = discord.Color.red()
	)
	embed.add_field(
		name = "Rules : ",
		value = f"```{rules}```")
	embed.set_image(url = thumbnail)

	return embed

def guess_movie_embed(guess_movie, chances_left, is_wrong = False, is_correct = False):
	guess_movie_name = "".join([ char if guess_movie[char] != "blank" else " _ " for char in guess_movie ])
	actual_movie_name = "".join(guess_movie.keys())

	digit_count = 0
	alpha_count = 0

	for count in range(len(actual_movie_name)):
		if actual_movie_name[count].isdigit():
			digit_count += 1
		elif actual_movie_name[count].isalpha():
			alpha_count += 1

	embed = discord.Embed(
		title = "Guess the Movie",
		description = f"```{guess_movie_name}```",
		color = discord.Color.red()
	)

	embed.add_field(
		name = "Movie Details",
		value = f"Alphabet Count : {alpha_count} \n Digit Count : {digit_count}",
		inline = False
	)

	embed.add_field(
		name = "❌ Wrong Guess" if is_wrong else  "✅ Correct Guess" if is_correct else "🔎 Chances Left",
		value = f"You have **{chances_left}** chances left",
		inline = True
	)

	embed.set_footer(
		text = "Enter 'exit' to exit the game"
	)

	return embed

class Game:
	@client.command()
	async def work(ctx):
		# Sending game rules
		await ctx.send(embed = rules_embed())

		# Setting up the game
		movie = random.choice(bollywood_movies).lower()
		guess_movie = dict(
			(char, "blank") if random.randint(0, 1) and char != " "  else 
			(char, "not_blank")
				for char in movie
		) 

		# Starting the game
		total_chances = 15

		await ctx.send(embed = guess_movie_embed(guess_movie, total_chances))
		total_chances -= 1

		for chances in range(total_chances):
			chances_left = total_chances - chances

			try:
				guess = await client.wait_for(
					"message" , 
					check = lambda m: m.author == ctx.author and m.channel == ctx.channel, 
					timeout = 60.0
				)
				guess = guess.content.lower()

				# Checking if the attempt is correct
				if guess in guess_movie and guess_movie[guess] == "blank":
					guess_movie[guess] = "not_blank"
					await ctx.send(embed = guess_movie_embed(guess_movie, chances_left, is_correct = True))
					continue

				# Is exit command
				if guess in ["exit", "quit", "stop", "end", "$exit"]:
					await ctx.send("Let's play again next time!")
					break
				
				await ctx.send(embed = guess_movie_embed(guess_movie, chances_left, is_wrong = True))

			except asyncio.TimeoutError:
				await ctx.send("Time's up!")
				break


TOKEN = os.environ.get("TOKEN")
client.run(TOKEN)

import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import requests
import random
import asyncio
from dotenv import load_dotenv
from assets.gif_collection import gifs
load_dotenv()

rules = """
1. Enter any alphabet as a Guess for the given Movie 
2. Guesses should be of Single Character 
3. There's a time limit of 60 seconds for Each Guess 
4. You get 15 chances to guess the movie 
5. If you are able to Guess it correctly , You get Currency between $(500-1000)
6. Unsuccessfull attempts will cost you $100
"""

class Greetings(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	def get_bollywood_movies(self):
		url = "https://www.sacnilk.com/entertainmenttopbar/Top_500_Bollywood_Movies_Of_All_Time"

		request = requests.get(url)
		content = request.content
		soup = BeautifulSoup(content , 'html.parser')

		links = []
		for tag in soup.find_all('a'):
			links.append(tag.text)

		bollywood_movies = links[45:1045]
		return bollywood_movies

	def rules_embed(self):
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
	
	def guess_movie_embed(self, guess_movie, chances_left, is_wrong = False, is_correct = False, history = []):
		guess_movie_name = "".join([ char["char"] if not char["is_blank"] else "_" for char in guess_movie ])
		actual_movie_name = "".join([ char["char"] for char in guess_movie ])

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

		if len(history):
			embed.add_field(
				name = "📋 Previous Guesses",
				value = f"```" + ", ".join(history) + "```",
				inline = False
			)

		embed.set_footer(
			text = "Enter 'exit' to exit the game"
		)

		return embed

	@commands.command(aliases = ["guess_movie", "guess"])
	async def _guess_movie(self, ctx):
		# Sending game rules
		await ctx.send(embed = self.rules_embed())

		# Setting up the game
		bollywood_movies = self.get_bollywood_movies()
		movie = random.choice(bollywood_movies).lower()

		vowel = ["a", "e", "i", "o", "u"]
		guess_movie = [
			{"char": char, "is_blank": True} if not char in vowel and char != " " else
			{"char": char, "is_blank": False}
				for char in movie
		]
		history = []

		# Starting the game
		total_chances = 15
		is_win = False

		await ctx.send(embed = self.guess_movie_embed(guess_movie, total_chances))

		while True:
			try:
				guess_letter = await self.bot.wait_for(
					"message" , 
					check = lambda m: m.author == ctx.author and m.channel == ctx.channel, 
					timeout = 60.0
				)
				guess_letter = guess_letter.content.lower()

				# Is exit command
				if guess_letter in ["exit", "quit", "stop", "end", "$exit"]:
					await ctx.send("Let's play again next time!")
					break

				# Is single character?
				if len(guess_letter) != 1:
					await ctx.send("Enter a single character!")
					continue

				history.append(guess_letter)

				# Checking if the attempt is correct
				is_correct = False
				match_indices = []
				value_index = 0

				for char in guess_movie:
					if guess_letter == char["char"] and char["is_blank"]:
						is_correct = True
						match_indices.append(value_index)
					value_index += 1

				# Correct Answer
				if is_correct:
					total_chances += 1

					for index in match_indices:
						guess_movie[index]["is_blank"] = False

					await ctx.send(embed = self.guess_movie_embed(guess_movie, total_chances, is_correct = True, history = history))

					# Is game won?
					if all(not char["is_blank"] for char in guess_movie):
						await ctx.send(f"You won the game! The movie was {movie}")
						is_win = True
						break
					
					continue

				# Is chances over?
				if total_chances <= 0:
					await ctx.send(f"You lost the game! The movie was {movie}")
					break
				
				# Wrong Guess
				total_chances -= 1
				await ctx.send(embed = self.guess_movie_embed(guess_movie, total_chances, is_wrong = True, history = history))

			except asyncio.TimeoutError:
				await ctx.send("Time's up!")
				break
		
		if not is_win:
			await ctx.send("Better luck next time!")



def setup(bot):
	bot.add_cog(Greetings(bot))

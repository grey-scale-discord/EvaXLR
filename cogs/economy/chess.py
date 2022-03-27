import discord
import chess
import urllib.parse
from discord.ext import commands
from dotenv import load_dotenv
import asyncio
load_dotenv()

class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def fen_to_image(self, fen):
        params = urllib.parse.urlencode({
            'fen': fen,
            'raw': 'true'
        })
        return f"https://fen2png.com/api/?{params}"
    
    def progress_bar_url(self, progress, total):
        white_progress = progress
        black_progress = total - progress
        params = urllib.parse.urlencode({
            'chco': 'FCFCFC,191919',
            'chd': f'a:{str(white_progress)}|{str(black_progress)}',
            'chf': 'bg,s,E3E3E300',
            'chma': '-10,0,0,-10',
            'chs': '700x80',
            'cht': 'bhs',
            'chxs': '0,FFFFFF00,0,-1,_,FFFFFF00,FFFFFF00|1,FFFFFF00,0,-1,_,FFFFFF00,FFFFFF00',
            'chxt': 'x,y'
        })
        return f"https://image-charts.com/chart?{params}"

    def chess_board_embed(self, board, player_one, player_two, current_player):
        board_fen = board.fen()
        board_image_url = self.fen_to_image(board_fen)

        embed = discord.Embed(
            title = f"Chess Board",
            description = f"{player_one.mention} vs {player_two.mention}",
            color = discord.Color.red()
        )

        embed.add_field(
            name = "Players",
            value = f"{player_one.mention} is **white** \n {player_two.mention} is **black**",
        )

        embed.add_field(
            name = "Current Turn",
            value = current_player.mention,
        )

        embed.set_image(
            url = board_image_url
        )

        embed.set_footer(
            text = "Enter 'exit' to exit the game"
        )

        return embed

    @commands.command(aliases = ["chess"])
    async def _chess(self, ctx, opponent: discord.Member):
        players = [
            ctx.author,
            opponent
        ]
        current_player = players[0]
        
        board = chess.Board()
        await ctx.send(
            embed = self.chess_board_embed(
                board = board, 
                player_one = ctx.author, 
                player_two = opponent, 
                current_player = current_player
            )
        )

        is_win = False
        while not is_win:
            try:
                san = await self.bot.wait_for(
                    "message" , 
                    check = lambda m: m.author == current_player and m.channel == ctx.channel, 
                    timeout = 60.0
                )
                san = san.content

                # Exit
                if san == "exit":
                    is_win = True
                    current_player = players[0] if current_player == players[1] else players[1]
                    break
                
                # Move
                board.push_san(san)
                
                # Is checkmate?
                if board.is_game_over():
                    is_win = True
                    await ctx.send(
                        embed = self.chess_board_embed(
                            board = board, 
                            player_one = ctx.author, 
                            player_two = opponent, 
                            current_player = current_player
                        )
                    )
                    break

                current_player = players[0] if current_player == players[1] else players[1]
                await ctx.send(
                    embed = self.chess_board_embed(
                        board = board, 
                        player_one = ctx.author, 
                        player_two = opponent, 
                        current_player = current_player
                    )
                )

            except ValueError:
                await ctx.send("Invalid move!")
                continue
            
            except asyncio.TimeoutError:
                await ctx.send("Time's up!")
                break
        
        if is_win:
            await ctx.send(f"{current_player.mention} won the game!")


def setup(bot):
    bot.add_cog(Greetings(bot))

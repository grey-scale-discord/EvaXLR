import discord
from discord.ext import commands

class Kick(commands.Cog):
    @commands.command(aliases = ["kick"])
    @commands.has_permissions(kick_members = True)
    async def _kick_member(self, ctx, user: discord.User, reason = None):
        try: 
            await ctx.guild.kick(user)

            embed = discord.Embed(
                title = "Member Kicked",
                description = f"{user.name} was kicked from {ctx.guild}",
                color = discord.Color.red()
                )

            embed.add_field(
                name = "Moderator",
                value = ctx.author.mention,
                inline = True
                )

            if reason != None:
                embed.add_field(
                    name = "Reason",
                    value = reason,
                    inline = True
                )

            await ctx.send(embed = embed)

        except discord.errors.Forbidden:
            message = f":x: | oops! I cannot kick {user.name}"
            embed = discord.Embed(
                description = message,
                color = discord.Color.red()
            )
            await ctx.send(embed = embed)

    @_kick_member.error 
    async def error_kick(self, ctx: commands.Context, error: commands.CommandError):

        if isinstance(error , commands.MissingRequiredArgument ):
            message = f"❌ | Missing Required Argument : **{error.param.name.upper()}**"
        elif isinstance(error , commands.MissingPermissions):
            message = "❌ | You are missing the required permissions to run this command!"
        elif isinstance(error , commands.BadArgument):
            message = "❌ | User not found"
        else:
            message = "❌ | Error! Something went Wrong"

        embed = discord.Embed(
            description = message,
            color = discord.Color.red()
        )

        await ctx.send(embed = embed)

def setup(bot):
	bot.add_cog(Kick(bot))
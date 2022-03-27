import discord
from discord.ext import commands

class Ban(commands.Cog):
    @commands.command(aliases = ["ban"])
    @commands.has_permissions(ban_members = True)
    async def _ban_member(self, ctx, user: discord.User, reason = None):
        try: 
            await ctx.guild.ban(user)

            embed = discord.Embed(
                title = "Member Kicked",
                description = f"{user.name} was banned from {ctx.guild}",
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
            message = f":x: | oops! I cannot ban {user.name}"
            
            embed = discord.Embed(
                description = message,
                color = discord.Color.red()
            )

            await ctx.send(embed = embed)

    @_ban_member.error 
    async def error_ban(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.MissingRequiredArgument ):
            message = f":x: | Missing Required Argument : **{error.param.name.upper()}**"
        
        elif isinstance(error, commands.MissingPermissions):
            message = ":x: | You are missing the required permissions to run this command!"
        
        elif isinstance(error, commands.BadArgument):
            message = ":x: | User not found"
        
        else:
            message = ":x: | Error! Something went Wrong"

        embed = discord.Embed(
            description = message,
            color = discord.Color.red()
        )

        await ctx.send(embed = embed)

def setup(bot):
	bot.add_cog(Ban(bot))
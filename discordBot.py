import os
import random

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')


@bot.command(name='purpose', help='Proudly displays the bots purpose', usage='!purpose')
async def purpose(ctx):
    purposeQuotes = [
        'My purpose is to track all the reports in this server.',
        'I try my best to serve the president of RCW'
        'Might as well call ourselves Report Commend Warriors'
    ]
    response = random.choice(purposeQuotes)
    await ctx.send(response)


@bot.command(name='randreport', help='Reports a random RCW member for the luls', usage='!randreport')
async def randreport(ctx):
    toReport = random.choice(ctx.guild.members)
    await ctx.send('{0} has been reported randomly!'.format(toReport.mention))


@bot.command(name='report', help='Personally report someone', usage='!report @member')
async def report(ctx, arg):
    member = ctx.guild.get_member_named(arg)
    await ctx.send('{0} has been reported by {1.author.mention}'.format(arg, ctx))
bot.run(TOKEN)

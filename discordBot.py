import os
import random
import sqlite3

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
    await ctx.send('{0} has been reported by {1.author.mention}'.format(arg, ctx))


@bot.command(name='feedTableData')
@commands.is_owner()
async def feedTableData(ctx):
    conn = sqlite3.connect("RCWdatabase.db")
    cursor = conn.cursor()
    memberList = []
    for member in ctx.guild.members:
        memberList.append((member.name, 0, 0, 10))
    cursor.executemany('INSERT INTO RCWDB VALUES (?,?,?,?)', memberList)
    conn.commit()
    conn.close()
bot.run(TOKEN)

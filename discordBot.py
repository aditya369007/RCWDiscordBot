import os
import random
import sqlite3
import re
import asyncio
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')


# Purpose definition
@bot.command(name='purpose', help='Proudly displays the bots purpose', usage='!purpose')
async def purpose(ctx):
    purposeQuotes = [
        'My purpose is to track all the reports in this server.',
        'I try my best to serve the president of RCW',
        'Might as well call ourselves Report Commend Warriors',
        'I try track reports perfectly. Who cares about the commends?'
    ]
    response = random.choice(purposeQuotes)
    await ctx.send(response)


# random report implementation
@bot.command(name='randreport', help='Reports a random RCW member for the luls', usage='!randreport')
async def randreport(ctx):
    toReport = random.choice(ctx.guild.members)
    await ctx.send('{0} has been reported randomly!'.format(toReport.mention))


# reporting another guild member
@bot.command(name='report', help='Personally report someone', usage='!report @member')
async def report(ctx, arg):
    conn = sqlite3.connect("RCWdatabase.db")
    cursor = conn.cursor()
    cursor.execute('SELECT Currency FROM RCWDB WHERE Name=?', [ctx.author.name])
    currencyReturnResult = cursor.fetchone()
    currencyReturnResult = int(''.join(map(str, currencyReturnResult)))
    if currencyReturnResult > 0:
        for mention in ctx.message.mentions:
            cursor.execute('UPDATE RCWDB SET Currency = (Currency - 1) WHERE Name = ?', [ctx.author.name])
            cursor.execute('UPDATE RCWDB SET Reports = (Reports + 1) WHERE Name = ?', [mention.name])
        conn.commit()
        conn.close()
        await ctx.send('{0} has been reported by {1.author.mention}!'.format(arg, ctx))
    else:
        await ctx.send('Sorry {0.author.mention}, you do not have enough duddu for a report'.format(ctx))


# commending another guild member
@bot.command(name='commend', help='Commend them,show them some love', usage='!commend @member')
async def commend(ctx, arg):
    conn = sqlite3.connect("RCWdatabase.db")
    cursor = conn.cursor()
    cursor.execute('SELECT Currency FROM RCWDB WHERE Name=?', [ctx.author.name])
    currencyReturnResult = cursor.fetchone()
    currencyReturnResult = int(''.join(map(str, currencyReturnResult)))
    if currencyReturnResult > 0:
        for mention in ctx.message.mentions:
            cursor.execute('UPDATE RCWDB SET Currency = (Currency - 1) WHERE Name = ?', [ctx.author.name])
            cursor.execute('UPDATE RCWDB SET Commends = (Commends + 1) WHERE Name = ?', [mention.name])
        conn.commit()
        conn.close()
        await ctx.send('{0} has been commended by {1.author.mention}!'.format(arg, ctx))
    else:
        await ctx.send('Sorry {0.author.mention}, you do not have enough duddu for a commend.'.format(ctx))


# checking your current currency balance
@bot.command(name='currencybal', help='Shows the amount of 💰 left', usage='!currencybal')
async def currencybal(ctx):
    conn = sqlite3.connect("RCWdatabase.db")
    cursor = conn.cursor()
    cursor.execute('SELECT Currency FROM RCWDB WHERE Name=?', [ctx.author.name])
    currencyReturnResult = cursor.fetchone()
    currencyReturnResult = int(''.join(map(str, currencyReturnResult)))
    conn.close()
    await ctx.send('You currently have {0} 💰 left'.format(currencyReturnResult))


# shows the users reports
@bot.command(name='myreports', help='Shows the amount of reports🔪 you got', usage='!myreports')
async def myreports(ctx):
    conn = sqlite3.connect("RCWdatabase.db")
    cursor = conn.cursor()
    cursor.execute('SELECT Reports FROM RCWDB WHERE Name=?', [ctx.author.name])
    reportReturnResult = cursor.fetchone()
    reportReturnResult = int(''.join(map(str, reportReturnResult)))
    conn.close()
    await ctx.send('You currently have {0} reports🔪'.format(reportReturnResult))


#shows the users Commends
@bot.command(name='mycommends', help='Shows the amount of commends🎉 you got', usage='!myreports')
async def mycommends(ctx):
    conn = sqlite3.connect("RCWdatabase.db")
    cursor = conn.cursor()
    cursor.execute('SELECT Commends FROM RCWDB WHERE Name=?', [ctx.author.name])
    commendReturnResult = cursor.fetchone()
    commendReturnResult = int(''.join(map(str, commendReturnResult)))
    conn.close()
    await ctx.send('You currently have {0} commends🎉'.format(commendReturnResult))


# 'admin' only resets the table data.
@bot.command(name='resetTableData')
@commands.is_owner()
async def resetTableData(ctx):
    conn = sqlite3.connect("RCWdatabase.db")
    cursor = conn.cursor()
    for member in ctx.guild.members:
        # memberList.append((member.name, 0, 0, 10))
        cursor.execute('UPDATE RCWDB SET Commends = ?, Reports = ?, Currency = ? WHERE Name = ?', (0, 0, 10, member.name))
    conn.commit()
    conn.close()
bot.run(TOKEN)

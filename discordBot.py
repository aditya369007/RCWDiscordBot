import os
import random
import sqlite3
import re
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

print(discord.__version__)

intents = discord.Intents.default()
intents.members = True
# client = discord.Client(intents=intents)

client = commands.Bot(command_prefix='!',intents=intents)


# Purpose definition
@client.command(name='purpose', help='Proudly displays the bots purpose', usage='!purpose')
async def purpose(ctx):
    purposeQuotes = [
        'My purpose is to track all the reports in this server.',
        'I try my best to serve the president of RCW',
        'Might as well call ourselves Report Commend Warriors',
        'I try to track reports perfectly. Who cares about the commends?'
    ]
    response = random.choice(purposeQuotes)
    await ctx.send(response)


#random report implementation
@client.command(name='randreport', help='Reports a random RCW member for the luls', usage='!randreport',aliases=['rr', 'randrep'])
async def randreport(ctx):
    for guild in client.guilds:
        toReport = random.choice(guild.members)
        await ctx.send('{0} has been reported randomly!'.format(toReport.mention))
    
# @client.command(name='printall')
# async def printall(ctx):
#     for guild in client.guilds:
#         for member in guild.members:
#             print(member.name, ' ')

    
    


# reporting another guild member
@client.command(name='report', help='Personally report someone', usage='!report @member_1 @member_2 .. @member_n',aliases=['rep', 'rpt', 'rp', 'sk'])
async def report(ctx, arg):
    conn = sqlite3.connect("RCWdatabase.db")
    cursor = conn.cursor()
    cursor.execute('SELECT Currency FROM RCWDB WHERE Name=?', [ctx.author.name])
    currencyReturnResult = cursor.fetchone()
    currencyReturnResult = int(''.join(map(str, currencyReturnResult)))
    numberOfMentions = len(ctx.message.mentions)
    if currencyReturnResult >= numberOfMentions:
        for mention in ctx.message.mentions:
            cursor.execute('UPDATE RCWDB SET Currency = (Currency - 1) WHERE Name = ?', [ctx.author.name])
            cursor.execute('UPDATE RCWDB SET Reports = (Reports + 1) WHERE Name = ?', [mention.name])
            await ctx.send('{0} has been reported by {1.author.mention}!'.format(mention.mention, ctx))
        conn.commit()
        conn.close()

    else:
        await ctx.send('Sorry {0.author.mention}, you do not have enough duddu for the report/s'.format(ctx))


# commending another guild member
@client.command(name='commend', help='Commend them,show them some love', usage='!commend @member_1 @member_2 .. @member_n', aliases=['cmnd'])
async def commend(ctx, arg):
    conn = sqlite3.connect("RCWdatabase.db")
    cursor = conn.cursor()
    cursor.execute('SELECT Currency FROM RCWDB WHERE Name=?', [ctx.author.name])
    currencyReturnResult = cursor.fetchone()
    currencyReturnResult = int(''.join(map(str, currencyReturnResult)))
    numberOfMentions = len(ctx.message.mentions)
    if currencyReturnResult >= numberOfMentions:
        for mention in ctx.message.mentions:
            cursor.execute('UPDATE RCWDB SET Currency = (Currency - 1) WHERE Name = ?', [ctx.author.name])
            cursor.execute('UPDATE RCWDB SET Commends = (Commends + 1) WHERE Name = ?', [mention.name])
            await ctx.send('{0} has been commended by {1.author.mention}!'.format(mention.mention, ctx))
        conn.commit()
        conn.close()
    else:
        await ctx.send('Sorry {0.author.mention}, you do not have enough duddu for the commend/s.'.format(ctx))


# checking your current currency balance
@client.command(name='currencybal', help='Shows the amount of 💰 left', usage='!currencybal', aliases=['duddu', 'currbal', 'bankbal', "currency"])
async def currencybal(ctx):
    conn = sqlite3.connect("RCWdatabase.db")
    cursor = conn.cursor()
    cursor.execute('SELECT Currency FROM RCWDB WHERE Name=?', [ctx.author.name])
    currencyReturnResult = cursor.fetchone()
    currencyReturnResult = int(''.join(map(str, currencyReturnResult)))
    conn.close()
    await ctx.send('{1.author.mention}} currently has {0} 💰 left'.format(currencyReturnResult,ctx))


# shows the users reports
@client.command(name='myreports', help='Shows the amount of reports🔪 you got', usage='!myreports', aliases=['repbal', 'repcnt'])
async def myreports(ctx):
    conn = sqlite3.connect("RCWdatabase.db")
    cursor = conn.cursor()
    cursor.execute('SELECT Reports FROM RCWDB WHERE Name=?', [ctx.author.name])
    reportReturnResult = cursor.fetchone()
    reportReturnResult = int(''.join(map(str, reportReturnResult)))
    conn.close()
    await ctx.send('{1.author.mention}} currently has {0} reports🔪'.format(reportReturnResult,ctx))


#shows the users Commends
@client.command(name='mycommends', help='Shows the amount of commends🎉 you got', usage='!mycommends', aliases=['cmndbal', 'cmndcnt'])
async def mycommends(ctx):
    conn = sqlite3.connect("RCWdatabase.db")
    cursor = conn.cursor()
    cursor.execute('SELECT Commends FROM RCWDB WHERE Name=?', [ctx.author.name])
    commendReturnResult = cursor.fetchone()
    commendReturnResult = int(''.join(map(str, commendReturnResult)))
    conn.close()
    await ctx.send('{1.author.mention} currently has {0} commends🎉'.format(commendReturnResult,ctx))

@client.command(name='reportlb')
async def reportlb(ctx):
    conn = sqlite3.connect("RCWdatabase.db")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM RCWDB ORDER BY Reports')
    result = cursor.fetchall()
    conn.close()
    topReportString = result[0][0]
    for guild in client.guilds:
        topReportMember = guild.get_member_named(topReportString)
        await ctx.send('Top Report Holder is {0}!!'.format(topReportMember.mention))

        



# 'admin' only resets the table data.
@client.command(name='resetTableData')
@commands.is_owner()
async def resetTableData(ctx):
    conn = sqlite3.connect("RCWdatabase.db")
    cursor = conn.cursor()
    for member in ctx.guild.members:
        # memberList.append((member.name, 0, 0, 10))
        cursor.execute('UPDATE RCWDB SET Commends = ?, Reports = ?, Currency = ? WHERE Name = ?', (0, 0, 10, member.name))
    conn.commit()
    conn.close()
client.run(TOKEN)

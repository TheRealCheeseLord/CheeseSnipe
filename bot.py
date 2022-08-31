import discord
from discord import Client, Embed, Intents, default_permissions, guild_only
from discord.abc import GuildChannel, PrivateChannel, Snowflake
from discord.ext import commands
from dotenv import load_dotenv

import os
import asyncio
import json
import shutil

def db_refreshDcName(ctx: discord.ApplicationContext):
    db_input = open('db.json')
    db_json = json.load(db_input)

    db_json[str(ctx.author.id)]["username"] = str(ctx.author)

load_dotenv(".env")
TOKEN = os.getenv("TOKEN")
intents = discord.Intents().all()
bot = commands.Bot(command_prefix=';', help_command=None, intents=intents, debug_guilds=[870024105934614609])

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_message_delete(message: discord.Message):

    db_input = open('db.json')
    db_json = json.load(db_input)

    if message.author.bot == True:
        return

    if not str(message.author.id) in db_json:
        if not message.attachments:

            os.mkdir('Messages/' + str(message.author.id))
            os.mkdir('Messages/' + str(message.author.id) + "/" + str(message.id))

            with open('Messages/' + str(message.author.id) + "/" + str(message.id) + "/content.txt", 'w') as text:
                text.write(message.content)

            created_at = str(message.created_at).split('.')[0]

            db_json[str(message.author.id)] = { "username": str(message.author), "cache": [{ "text": "Messages/" + str(message.author.id) + "/" + str(message.id) + "/content.txt", "message_id": str(message.id), "created_at": str(created_at), "created_by": str(message.author) }] }

            with open("db.json", "w") as jsonFile:
                json.dump(db_json, jsonFile, sort_keys=True, indent=4)
        else:
            os.mkdir('Messages/' + str(message.author.id))
            os.mkdir('Messages/' + str(message.author.id) + "/" + str(message.id))
            os.mkdir('Messages/' + str(message.author.id) + "/" + str(message.id) + "/attachements")

            with open('Messages/' + str(message.author.id) + "/" + str(message.id), 'w') as text:
                text.write(message.content)

            x_int = 0
            for x in message.attachments:
                await x.save(f'Messages/{str(message.author.id)}/{str(message.id)}/attachements/{str(x_int)}.png')
                x_int += 1

            created_at = str(message.created_at).split('.')[0]

            db_json[str(message.author.id)] = { "username": str(message.author), "cache": [{ "text": "Messages/" + str(message.author.id) + "/" + str(message.id) + "/content.txt", "attachements": "Messages/" + message.author.id + "/" + message.id + "/attachements", "message_id": str(message.id), "created_at": str(created_at), "created_by": str(message.author) }] }

            with open("db.json", "w") as jsonFile:
                json.dump(db_json, jsonFile, sort_keys=True, indent=4)
    else:
        if not message.attachments:

            os.mkdir('Messages/' + str(message.author.id) + "/" + str(message.id))

            if len(db_json[str(message.author.id)]["cache"]) == 10:

                oldest_message_id = db_json[str(message.author.id)]["cache"][0]["message_id"]

                shutil.rmtree(f'Messages/{str(message.author.id)}/{oldest_message_id}')

                db_json[str(message.author.id)]["cache"].pop(0)

            with open('Messages/' + str(message.author.id) + "/" + str(message.id) + "/content.txt", 'w') as text:
                text.write(message.content)

            created_at = str(message.created_at).split('.')[0]

            db_json[str(message.author.id)]["cache"].append({ "text": "Messages/" + str(message.author.id) + "/" + str(message.id) + "/content.txt", "message_id": str(message.id), "created_at": str(created_at), "created_by": str(message.author) })

            with open("db.json", "w") as jsonFile:
                json.dump(db_json, jsonFile, sort_keys=True, indent=4)
        else:

            os.mkdir('Messages/' + str(message.author.id) + "/" + str(message.id))
            os.mkdir('Messages/' + str(message.author.id) + "/" + str(message.id) + "/attachements")

            if len(db_json[str(message.author.id)]["cache"]) == 10:

                oldest_message_id = db_json[str(message.author.id)]["cache"][0]["message_id"]

                shutil.rmtree(f'Messages/{str(message.author.id)}/{oldest_message_id}')

                db_json[str(message.author.id)]["cache"].pop(0)

            with open('Messages/' + str(message.author.id) + "/" + str(message.id) + "/content.txt", 'w') as text:
                text.write(message.content)

            x_int = 0
            for x in message.attachments:
                await x.save(f'Messages/{str(message.author.id)}/{str(message.id)}/attachements/{str(x_int)}.png')
                x_int += 1

            created_at = str(message.created_at).split('.')[0]

            db_json[str(message.author.id)]["cache"].append({ "text": "Messages/" + str(message.author.id) + "/" + str(message.id) + "/content.txt", "attachements": "Messages/" + str(message.author.id) + "/" + str(message.id) + "/attachements", "message_id": str(message.id), "created_at": str(created_at), "created_by": str(message.author) })

            with open("db.json", "w") as jsonFile:
                json.dump(db_json, jsonFile, sort_keys=True, indent=4)

@bot.slash_command(name='list')
async def listMessages(ctx: discord.ApplicationContext, user: discord.Option(discord.Member, "User")):

    db_input = open('db.json')
    db_json = json.load(db_input)

    if str(user.id) in db_json:
        s = ""
        for x in db_json[str(user.id)]["cache"]:
            text_content_location = x["text"]
            text_content = open(text_content_location)
            text_content = text_content.read()
            if len(text_content) > 10:
                text_content = text_content[0:10]
                text_content += "..."

            index = db_json[str(user.id)]["cache"].index(x)
            created_at = x["created_at"]

            s += "**[" + str(index) + "]** " + str(created_at) + " - " + text_content + "\n"
        
        embed = discord.Embed(title="**" + str(user) + "**:", description=s, color=0xebca26)
        await ctx.respond(embed = embed)
    else:
        embed = discord.Embed(title='User not found', color=0xebca26)
        await ctx.respond(embed = embed)

@bot.slash_command(name='view')
async def view(ctx: discord.ApplicationContext, user: discord.Option(discord.Member, "User"), index: discord.Option(int, "Index")):

    db_input = open('db.json')
    db_json = json.load(db_input)

    if str(user.id) in db_json:

        message_json = db_json[str(user.id)]["cache"][index]
        created_at = message_json["created_at"]
        message_id = message_json["message_id"]

        file_list = []
        if os.path.exists(f'Messages/{str(user.id)}/{str(message_id)}/attachements'):
            for file in os.listdir(f'Messages/{str(user.id)}/{str(message_id)}/attachements'):
                file_object = open(f'Messages/{str(user.id)}/{str(message_id)}/attachements/' + file, 'rb')
                file_list.append(discord.File(file_object))

        s = "**Created At:** " + created_at + " UTC" +"\n**Content:**\n\n"

        message_content_location = message_json["text"]
        message_content = open(message_content_location)
        message_content = message_content.read()
        
        s += message_content

        if os.path.exists(f'Messages/{str(user.id)}/{str(message_id)}/attachements'):
            embed = discord.Embed(title='**' + str(user) + '**:', description=s, color=0xebca26)
            await ctx.respond(embed = embed, files = file_list)
        else:
            embed = discord.Embed(title='**' + str(user) + '**:', description=s, color=0xebca26)
            await ctx.respond(embed = embed)
    else:
        embed = discord.Embed(title='User not found', color=0xebca26)
        await ctx.respond(embed = embed)

bot.run(TOKEN)
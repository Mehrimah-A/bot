import os
from dotenv import load_dotenv
load_dotenv(override=True)

import random

from yolo_recognizer import recognize_image_objects
TOKEN=os.environ.get("DISCORD_TOKEN")

import discord
from discord.ext import commands, tasks

izinler=discord.Intents.all()
izinler.message_content=True

tega=commands.Bot(command_prefix="!",intents=izinler)

@tega.event
async def on_ready():
    print("bot is ready")

fikralar=[]
with open("./fikralar.txt",encoding="utf8") as doc:
    fikralar=doc.read()
    fikralar=fikralar.split("***")

@tega.command("fikra")
async def fikra(ctx):
    fikra=random.choice(fikralar)
    await ctx.send(fikra)


@tega.command("tani")
async def tani(ctx):
    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            if attachment .filename.endswitch((".jpg",".jpeg",".png")):
                temp_image_path=f"temp_{attachment.filename}"
                await attachment.save(temp_image_path)

                recognition=recognize_image_objects(temp_image_path)
                output_image_path,detections=recognition
                await ctx.channel.send(file=discord.File(output_image_path))
                detections_text = "\n".join([f"{obj['name']}: {obj['percentage_probability']:.2f}%" for obj in detections])
                await ctx.channel.send(f"Detections:\n{detections_text}")
                os.remove(temp_image_path)
            else:
                await ctx.send("No attachments found in the message.")




tega.run(TOKEN)
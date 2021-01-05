import discord
import os
from keep_alive import keep_alive
from PIL import Image
import requests

client = discord.Client()

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user or str(message.author).endswith("5494") or str(message.author).endswith("#0929"):
    return 
  if len(message.attachments) > 0:
    for file in message.attachments:
      string = str(file)
      url = string[string.index("https"):-2]
      if url.endswith((".jpeg",".jpg",".png",".JPEG",".JPG",".PNG")):
        filename = url.split('/')[-1]
        r = requests.get(url, allow_redirects=True)
        open(filename, 'wb').write(r.content)
        my_image = Image.open(filename)
        (width, height) = (my_image.width * 5, my_image.height // 5) 
        my_image = my_image.resize((width, height))
        await message.delete()
        if url.endswith((".jpeg",".jpg",".JPEG",".JPG")):
          my_image.save("result.jpg")
          await message.channel.send(file=discord.File('result.jpg'))
        else:
          my_image.save("result.png")
          await message.channel.send(file=discord.File('result.png'))
        my_image.close()
        
keep_alive()
client.run(os.getenv('TOKEN'))

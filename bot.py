import discord
import requests
import os
import asyncio

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
CHANNEL_NAME = "📢➤Discount〡تخفيضات"
DEALS_API = "https://www.cheapshark.com/api/1.0/deals?storeID=1&upperPrice=60&pageSize=5"

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

client = discord.Client(intents=intents)

def get_deals():
    try:
        response = requests.get(DEALS_API)
        data = response.json()
        messages = []
        for deal in data:
            title = deal["title"]
            normal_price = deal["normalPrice"]
            sale_price = deal["salePrice"]
            savings = round(float(deal["savings"]))
            store = "Steam"
            link = f"https://www.cheapshark.com/redirect?dealID={deal['dealID']}"
            msg = f"**{title}** ➡️ ~~{normal_price}~~ ➡️ **{sale_price}** (**وفر {savings}**)"

🛒: متجر {store}
🔗 {link}"
            messages.append(msg)
        return messages
    except Exception as e:
        return [f"❌ فشل في جلب التخفيضات: {e}"]

@client.event
async def on_ready():
    print(f"✅ تم تسجيل الدخول كـ {client.user}")
    for guild in client.guilds:
        for channel in guild.text_channels:
            if channel.name == CHANNEL_NAME and channel.permissions_for(guild.me).send_messages:
                for msg in get_deals():
                    asyncio.create_task(channel.send(msg))
                return

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.lower() == "تخفيضات":
        for msg in get_deals():
            await message.channel.send(msg)

client.run(TOKEN)

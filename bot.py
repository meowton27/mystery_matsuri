import discord
from discord.ext import commands
from discord.commands import Option
from datetime import timedelta
from typing import List 
import random
import json
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
bot = discord.Bot(intents = intents)

# ---------------------------------------------------------------- EVENT COMMANDS ----------------------------------------------------------------

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")

@bot.event
async def on_application_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
         await ctx.respond(f"The command is on cooldown, please try again in `{round(error.retry_after,2)}` seconds")
    else:
         raise error



# ---------------------------------------------------------------- SLASH COMMANDS ----------------------------------------------------------------

# ---------------------------------------------------------------- CURRENCIES     ----------------------------------------------------------------

try:
    with open('./Python_lang/discord_bot/user_data.json', 'r') as f:
        user_data = json.load(f)
except FileNotFoundError:
    print("File 'user_data.json' not found.")
    user_data = {}  # Initialize with an empty dictionary
except json.JSONDecodeError:
    print("Invalid JSON data in 'user_data.json'.")
    user_data = {}  # Initialize with an empty dictionary

def save_user_data():
    with open('./Python_lang/discord_bot/user_data.json', 'w') as f:
        json.dump(user_data, f, indent=4)

@bot.slash_command(name="work", description="doing something")
async def daily(ctx):
    user_id = str(ctx.author.id)

    # Check if the user has a balance entry, create one if not
    if user_id not in user_data:
        user_data[user_id] = {'balance': 0}

    # Check if the user can work (based on cooldown or other criteria)
    earnings = random.randint(10, 50)
    user_data[user_id]['balance'] += earnings
    save_user_data()

    await ctx.respond(f'You earned {earnings} coins! <:dancing:1158790727149568073>')

@bot.slash_command(name="balance", description="your balance")
async def balance(ctx) :
    user_id = str(ctx.author.id)

    # Check if the user has a balance entry, create one if not
    if user_id not in user_data:
        await ctx.respond(f'You have no balance entry')
    else :
        bal = user_data[user_id]['balance']
        await ctx.respond(f'Your balance is {bal} coins')
    

# ---------------------------------------------------------------- FOOD DELIVERY AND ORDER -------------------------------------------------------

@bot.slash_command(name="order", description="ordering food")
async def order(ctx:commands.Context, 
                menu: discord.Option(str, choices=['quack', 'meow', 'woof']), 
                option: str = None):
    
    embed = discord.Embed(title=f"Hello there <a:kitsuneflower:1156299096559202384>",
                          description=f"Name\t: {ctx.author.mention}\nyour order\t: {menu}\ndetails\t: {option}", 
                          color=discord.Color.blurple())
    
    embed_kitchen = discord.Embed(title=f"Order Received <a:kitsuneflower:1156299096559202384>",
                          description="To be edited, the order details", 
                          color=discord.Color.red())
    
    # sending the order to the kitchen
    thread_id = ctx.guild.get_channel_or_thread(1159011194951176212)
    await thread_id.send("Order Received, make it asap", embed = embed_kitchen)

    # giving the receipt to the user
    await ctx.respond(f'Your order is delivered {ctx.author.mention}, thank you for ordering us', embed = embed)
    
@bot.slash_command(name="deliver",description="Delivering the order to the customer")
async def deliver(ctx:commands.Context,
                  user: discord.Option(discord.SlashCommandOptionType.user, required=True),
                  message: str = None) :
     
    
    embed_user = discord.Embed(title=f"Food Delivery <a:kitsuneflower:1156299096559202384>",
                          description=f"Your Food is here {user}, enjoy!\nmessage\t:{message}", 
                          color=discord.Color.green())
    
    # sending the food to the user
    thread_id = ctx.guild.get_channel_or_thread(1159014759459475466)
    await thread_id.send("Your order is here <@732966109916954677>", embed = embed_user)

    # notifying the cook that the order is delivered
    await ctx.respond("order delivered")

# ---------------------------------------------------------------- MISCELANNOUS ------------------------------------------------------------------

@bot.slash_command(name = "boo", description = "Making you scared I bet")
@commands.cooldown(1, 5 * 60)
async def say_boo(ctx):
        await ctx.respond("Boo!")   

@bot.slash_command(name = "dmme", description = "Giving ya a DM")
@commands.cooldown(1, 5 * 60)
async def dm_me(ctx: commands.Context):
    emoji_custom_id = "<:KitsuneMasks02:1158093475322011680>"
    emoji2 = "<a:kitsuneflower:1156299096559202384>" 
    await ctx.respond(f"Don't wanna {emoji_custom_id}")

    user = ctx.author

    # Create an embed for the DM
    embed = discord.Embed(title=f"Hello there {emoji2}",description="let me know if this dm reach you", color=discord.Color.green())
    image_url = 'https://cdn.discordapp.com/attachments/1154695654501785620/1154804232407482449/FINAL-mystery-matsuri-banner.jpg?ex=651b8d00&is=651a3b80&hm=29f9d96ee759c01cc979be80e5c435c8275d3d012b7b2bab6c4668601541661f&'
    embed.set_image(url=image_url)

    try:
        await user.send(embed=embed)
        await ctx.respond(f"JK, I Sent you a DM with a custom hello message! {emoji2}", ephemeral=True)
    except discord.Forbidden:
        await ctx.respond(f"Too bad your dm is closed {emoji_custom_id}", ephemeral=True)





bot.run(TOKEN)
import discord
from discord.ext import commands
from discord.commands import Option
from datetime import timedelta
from typing import List 
import random
import json
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
bot = discord.Bot(intents = intents)

fish_cmds = ['info', 'help', 'list', 'collection']

fish_data = [
    {"number": "01", "emote_id": "<:1f:1156919377308954654>", "name": "common"},
    {"number": "02", "emote_id": "<:2f:1156919381973028864>", "name": "comet"},
    {"number": "03", "emote_id": "<:3f:1156919386385428500>", "name": "wakin"},
    {"number": "04", "emote_id": "<:4f:1156919390692978698>", "name": "watonai"},
    {"number": "05", "emote_id": "<:5f:1156919394337832961>", "name": "london shubunkin"},
    {"number": "06", "emote_id": "<:6f:1156919396283977778>", "name": "american shubunkin"},
    {"number": "07", "emote_id": "<:7f:1156919400432156694>", "name": "bristol shubunkin"},
    {"number": "08", "emote_id": "<:8f:1156919403993112646>", "name": "jikin"},
    {"number": "09", "emote_id": "<:9f:1156919407893819504>", "name": "fantail"},
    {"number": "10", "emote_id": "<:10f:1156919412763410473>", "name": "sarasa"},
    {"number": "11", "emote_id": "<:11f:1156919416425037834>", "name": "calico"},
    {"number": "12", "emote_id": "<:12f:1156919418866114680>", "name": "veil tail"},
    {"number": "13", "emote_id": "<:13f:1156919422146060319>", "name": "oranda"},
    {"number": "14", "emote_id": "<:14f:1156919425849639003>", "name": "red cap oranda"},
    {"number": "15", "emote_id": "<:15f:1156919427875479552>", "name": "lion head"},
    {"number": "16", "emote_id": "<:16f:1156919431583248514>", "name": "ranchu"},
    {"number": "17", "emote_id": "<:17f:1156919433709768724>", "name": "black moor"},
    {"number": "18", "emote_id": "<:18f:1156919437388156999>", "name": "panda moor"},
    {"number": "19", "emote_id": "<:19f:1156919441184014386>", "name": "pearlscale"},
    {"number": "20", "emote_id": "<:20f:1156919444757545101>", "name": "crown pearlscale"},
    {"number": "21", "emote_id": "<:21f:1156919447475462215>", "name": "butterfly telescope"},
    {"number": "22", "emote_id": "<:22f:1156919451179036742>", "name": "egg"},
    {"number": "23", "emote_id": "<:23f:1156919454731616257>", "name": "blue phoenix"},
    {"number": "24", "emote_id": "<:24f:1156919456853934130>", "name": "tosakin"},
    {"number": "25", "emote_id": "<:25f:1156919460582670347>", "name": "tamasaba"},
    {"number": "26", "emote_id": "<:26f:1156919464093290516>", "name": "sukiyu"},
    {"number": "27", "emote_id": "<:27f:1156919466496638996>", "name": "bubble eye"},
    {"number": "28", "emote_id": "<:28f:1156919470024040518>", "name": "star gazer"}
]

fish_catchphrases = {
    "1": "{user.mention} successfully captured a **{fish_number}** goldfish! {emote_id}",
    "2": "Great job, {user.mention}! You reeled in a glimmering **{fish_number}** goldfish! {emote_id}",
    "3": "Woah~ Nice catch, {user.mention}! A **{fish_number}** goldfish in the net! {emote_id}",
    "4": "{user.mention}, you’ve got yourself a stunning **{fish_number}** goldfish! {emote_id}",
    "5": "Well done, {user.mention}. You’ve scooped a **{fish_number}** goldfish! {emote_id}",
    "6": "A shiny **{fish_number}** goldfish for {user.mention}! {emote_id}",
    "7": "Nice scoop, {user.mention}! You captured a **{fish_number}** goldfish~ {emote_id}",
    "8": "{user.mention} captured a **{fish_number}** goldfish! Keep scooping to complete your collection~ {emote_id}",
    "9": "{user.mention} is on fire! A dazzling **{fish_number}** goldfish in your scoop! {emote_id}",
    "10": "{user.mention} captured a **{fish_number}** goldfish. Keep scooping, you’re doing great! {emote_id}",
    "11": "Hey! {user.mention} snagged a beautiful **{fish_number}** goldfish~ {emote_id}",
    "12": "Lucky, {user.mention}! You’ve scooped a **{fish_number}** goldfish~ {emote_id}",
    "13": "Your skills are unmatched, {user.mention}! You successfully grabbed an **{fish_number}** goldfish. {emote_id}",
    "14": "You're making quite a splash, {user.mention}! You’ve scooped a **{fish_number}** goldfish. {emote_id}",
    "15": "Extraordinary {user.mention}! You've added a **{fish_number}** to your collection. {emote_id}",
    "16": "{user.mention} reeled in a sparkling **{fish_number}** goldfish! {emote_id}",
    "17": "{user.mention} mastered the art of the scoop and caught a **{fish_number}** goldfish! {emote_id}",
    "18": "You’re a pro at this, {user.mention}! You captured a **{fish_number}** goldfish. {emote_id}",
    "19": "Scoop-tastic! {user.mention} captured a gleaming **{fish_number}** goldfish! {emote_id}",
    "20": "Great job, {user.mention}! A **{fish_number}** goldfish joins your collection. {emote_id}",
    "21": "Fishy fortune favors you, {user.mention}! You captured a **{fish_number}** goldfish~ {emote_id}",
    "22": "What is it, {user.mention}? *gasp* It’s a **{fish_number}** goldfish! {emote_id}",
    "23": "Phew! That was a tough fight, {user.mention}. You captured a pretty **{fish_number}** goldfish! {emote_id}",
    "24": "Oh, look at that {user.mention}! You scooped a **{fish_number}** goldfish~ {emote_id}",
    "25": "You made it look easy, {user.mention}! You caught a **{fish_number}** goldfish! {emote_id}",
    "26": "Yay! {user.mention} successfully scooped a **{fish_number}** goldfish! {emote_id}",
    "27": "Nice catch, {user.mention}! You got a **{fish_number}** goldfish! {emote_id}",
    "28": "Fish-scooping master {user.mention}! You successfully scooped up a shiny **{fish_number}** goldfish! {emote_id}",
    "29": random.choice([
        "Oh no! Your scooper came up empty. Try again!",
        "Oops! You failed to catch one. :(",
        "Your scooping skills need refinement. You couldn’t even catch a common goldfish. :(",
        "\*Your scooper broke.\* Don’t give up! You’ll get the hang of it~",
        "Aw, so close! You nearly got it…"
    ])
}

try:
    with open('./user_data.json', 'r') as f:
        user_data = json.load(f)
except FileNotFoundError:
    print("File 'user_data.json' not found.")
    user_data = {}  # Initialize with an empty dictionary
except json.JSONDecodeError:
    print("Invalid JSON data in 'user_data.json'.")
    user_data = {}  # Initialize with an empty dictionary

def save_user_data():
    with open('./user_data.json', 'w') as f:
        json.dump(user_data, f, indent=4)

# ---------------------------------------------------------------- EVENT COMMANDS ----------------------------------------------------------------

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")

@bot.event
async def on_application_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        retry_after = error.retry_after
        if retry_after >= 86400:  # More than a day
            days = int(retry_after // 86400)
            await ctx.respond(f"The command is on cooldown, please try again in {days} day{'s' if days > 1 else ''}.")
        elif retry_after >= 3600:  # More than an hour
            hours = int(retry_after // 3600)
            await ctx.respond(f"The command is on cooldown, please try again in {hours} hour{'s' if hours > 1 else ''}.")
        elif retry_after >= 60:  # More than a minute
            minutes = int(retry_after // 60)
            await ctx.respond(f"The command is on cooldown, please try again in {minutes} minute{'s' if minutes > 1 else ''}.")
        else:
            await ctx.respond(f"The command is on cooldown, please try again in {round(retry_after, 2)} seconds.")
    else:
        raise error



# ---------------------------------------------------------------- SLASH COMMANDS ----------------------------------------------------------------

# ---------------------------------------------------------------- CURRENCIES     ----------------------------------------------------------------

@bot.slash_command(name="daily", description="doing something")
@commands.cooldown(1, 24 * 60 * 60)
async def daily(ctx):
    user_id = str(ctx.author.id)

    # Check if the user has a balance entry, create one if not
    if user_id not in user_data:
        user_data[user_id] = {'balance': 0}
    elif 'balance' not in user_data[user_id]:
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

# ---------------------------------------------------------------- FISH SCOOPING -----------------------------------------------------------------

@bot.slash_command(name="fish", description="Fish Scooping ayy")
async def fish(ctx: commands.Context, option: discord.Option(str, choices=fish_cmds)):
    if option == 'info':
        await fish_info(ctx)
    elif option == 'help':
        await fish_help(ctx)
    elif option == 'list':
        await fish_list(ctx)
    elif option == 'collection':
        await fish_collection(ctx)
    else:
        await ctx.respond("Invalid option. Please choose from: info, help, list, collection")

async def fish_info(ctx: commands.Context):
    # information about fish scooping
    embed = discord.Embed(
    title="Scoop n' Solve",
    description="Experience the joy of catching fish and solving riddles! Inspired by the classic Japanese festival game “Kingyu Sukui” where players use a paper scooper to catch goldfish from a pond.",
    color=discord.Color.blurple()
    )

    embed.add_field(
        name="**Gameplay:**",
        value=(
            "- Use the slash command `/scoop` to play fish scooping.\n"
            "- There are 28 unique goldfish species available to catch. Collect them all for a special prize!\n"
            "- Keep an eye out for random *fishy* riddles. Successfully solving these riddles will earn you valuable clues for the mystery game. Use command `/ans` to send your answer to a riddle~\n"
            "- Enjoy scooping up goldfish, solving riddles, and working toward the prizes!"
        )
    )

    embed.add_field(
        name="**Prizes:**",
        value=(
            "- You get 5 fest points for every goldfish you catch.\n"
            "- A complete set (28 species of goldfish) can be exchanged for a 10k <:dccoin:722844861148955021> coupon.\n"
            "- The first player to complete a set will receive a special award. Don't forget to ping any staff member of <@&1151925948074184755>"
        ),
        inline = False
    )

    image_url = 'https://i.pinimg.com/originals/60/1f/68/601f68d55572d5ea2e42b2e85bc8b333.gif'
    embed.set_image(url=image_url)
    embed.set_footer(text="Mystery Matsuri | Scoop n' Solve")

    # giving the receipt to the user
    await ctx.respond(embed = embed)

async def fish_help(ctx: commands.Context):
    embed = discord.Embed(title="Scoop n' Solve Fish Commands",
                          description="`/fish info` : to view the gameplay and prizes\n"
                                      "`/fish list` : to view the goldfish collection\n"
                                      "`/scoop` : to play fish scooping and catch a goldfish!",
                          color=discord.Color.gold()
                          )

    # Set the image URL
    embed.set_image(url="https://i.pinimg.com/originals/60/1f/68/601f68d55572d5ea2e42b2e85bc8b333.gif")

    # Set the footer
    embed.set_footer(text="Mystery Matsuri | Scoop n' Solve")

    # You can send this embed in a message like this
    await ctx.respond(embed=embed)

async def fish_list(ctx: commands.Context):
    embed = discord.Embed(color=discord.Color.orange())
    embed.set_image(url="https://cdn.discordapp.com/attachments/1154695654501785620/1156912343138185226/Fish_List.png?ex=6516b214&is=65156094&hm=3291ea33884896639f7e753f2acbe10e8acd3d115d8cb4ff12614149e264d663&")

    # You can send this embed in a message like this
    await ctx.respond(embed=embed)

async def fish_collection(ctx: commands.Context):
    # Implement the logic for the 'collection' option here
    user_id = str(ctx.author.id)

    # Check if the user data exists and has a "fish_catches" key
    if user_id not in user_data or "fish_catches" not in user_data[user_id]:
        await ctx.respond("You haven't caught any fish yet.")
        return

    fish_catches = user_data[user_id]["fish_catches"]

    # Create two lists for column 1 and column 2
    column1 = []
    column2 = []

    for fish_number, count in fish_catches.items():
        fish_entry = fish_data[int(fish_number) - 1]  # Adjust index since fish numbers start from 1
        fish_name = fish_entry["name"]
        emote_id = fish_entry["emote_id"]
        formatted_fish = f"`#{fish_number}` {fish_name} {emote_id} \t× {count}"

        # Add to the appropriate column list
        if len(column1) < 14:
            column1.append(formatted_fish)
        else:
            column2.append(formatted_fish)

    # Create an embed with two fields (left and right) with inline format
    embed = discord.Embed(title="**Fish Collection**",description=f"Goldfishes owned by {ctx.author.mention} <a:goldfishfish:1156278359446265926>", color=discord.Color.red())

    embed.add_field(name="", value="\n".join(column1), inline=True)
    embed.add_field(name="", value="\n".join(column2), inline=True)

    await ctx.respond(embed = embed)

@bot.slash_command(name = "scoop", description = "Scooping a fish")
# @commands.cooldown(1, 5 * 60)
async def scoop(ctx):
    rng = random.randint(0, len(fish_data) - 1)  # Pick a random fish index
    fish = fish_data[rng]

    fish_name = f"{fish['name']}"
    fish_number = fish['number']
    emote_id = fish['emote_id']

    # Pick a random catchphrase
    rng2 = random.randint(1, len(fish_catchphrases))
    catchphrase_template = fish_catchphrases[f"{rng2}"]
    if rng2 == 29 :
        await ctx.respond(catchphrase_template)
    else :
        catchphrase = catchphrase_template.format(user=ctx.author, fish_number=fish_name, emote_id=emote_id)

        # Update user's data (you may need to adapt this to your user data structure)
        user_id = str(ctx.author.id)
        if user_id not in user_data:
            user_data[user_id] = {'fish_catches': {}}
        if 'fish_catches' not in user_data[user_id]:
            user_data[user_id] = {'fish_catches': {}}
            for fish in fish_data:
                user_data[user_id]['fish_catches'][fish['number']] = 0

        user_data[user_id]['fish_catches'][fish_number] += 1


        save_user_data()


        await ctx.respond(catchphrase)



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
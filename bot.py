import discord
from discord.ext import commands
from discord.commands import Option
from discord.ui.button import Button
from discord.ui import View
from typing import List 
import random
import json
import os
from dotenv import load_dotenv
import asyncio

from data import fish_data, fish_catchphrases


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
bot = discord.Bot(intents = intents)

fish_cmds = ['info', 'help', 'list', 'collection']


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

# checking if the user is registered in json or not
def check_data(user_id) :
    if user_id not in user_data:
        user_data[user_id] = {}
        user_data[user_id]['fish_catches'] = {}
        for fish in fish_data:
            user_data[user_id]['fish_catches'][fish['number']] = 0
        user_data[user_id]['balance'] = 0

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
            await ctx.respond(f"The command is on cooldown, please try again in `{days} day{'s' if days > 1 else ''}.`")
        elif retry_after >= 3600:  # More than an hour
            hours = int(retry_after // 3600)
            await ctx.respond(f"The command is on cooldown, please try again in `{hours} hour{'s' if hours > 1 else ''}.`")
        elif retry_after >= 60:  # More than a minute
            minutes = int(retry_after // 60)
            await ctx.respond(f"The command is on cooldown, please try again in `{minutes} minute{'s' if minutes > 1 else ''}.`")
        else:
            await ctx.respond(f"The command is on cooldown, please try again in `{round(retry_after, 2)} seconds.`")
    else:
        raise error


# ---------------------------------------------------------------- SLASH COMMANDS ----------------------------------------------------------------

# ---------------------------------------------------------------- CURRENCIES     ----------------------------------------------------------------

@bot.slash_command(name="fortune", description="doing something")
@commands.cooldown(1, 24 * 60 * 60, commands.BucketType.user)
async def fortune(ctx):
    await ctx.respond("Opening the fortune slip...")

    await asyncio.sleep(1)  # Add a bit more delay before showing the result

    fortune_result = random.choice(["Great Fortune", "Good Fortune", "Modest Fortune", "Rising Fortune","Misfortune","Great Misfortune"])

    user_id = str(ctx.author.id)

    # Check if the user has a balance entry, create one if not
    check_data(user_id)

    # Check if the user can work (based on cooldown or other criteria)
    earnings = random.randint(10, 30)
    user_data[user_id]['balance'] += earnings
    save_user_data()
    
    embed = discord.Embed(
        title="Fortune Slip Result",
        description=f"You got: **{fortune_result}**, and You earned `{earnings}` <:sakura:1159350038959505468>",
        color=discord.Color.gold()
    )
    embed.set_image(url='https://cdn.discordapp.com/attachments/1161323437717995530/1161324191291809832/ai_lucky.jpeg?ex=6537e26f&is=65256d6f&hm=26d6b5686672dcd5de8901a93dd9b5b440a8fe65a41bbc3e9ecc659ea7eb9cc7&')

    # Send a new interaction response with the embed
    await ctx.send(embed=embed)


@bot.slash_command(name="balance", description="your balance")
async def balance(ctx) :
    user_id = str(ctx.author.id)

    # Check if the user has a balance entry, create one if not
    check_data(user_id)

    bal = user_data[user_id]['balance']
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Updating it to be embed
    await ctx.respond(f'Your balance is `{bal}` <:sakura:1159350038959505468>')
    

# ---------------------------------------------------------------- FOOD DELIVERY AND ORDER -------------------------------------------------------

@bot.slash_command(name="menu", description="Our stall's menu")
async def menu(ctx: commands.Context):
    embed = discord.Embed(color=discord.Color.orange())
    embed.set_image(url="https://cdn.discordapp.com/attachments/1154695654501785620/1159916352933482606/menu-01.png?ex=6532c348&is=65204e48&hm=6e62e4c3f65df22063f0d28825f0c7fb650c2d3d3fed29533b63656c2e6daa84&")

    await ctx.respond(embed=embed)

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
# @commands.cooldown(1, 5 * 60, commands.BucketType.user)
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
        check_data(user_id)

        user_data[user_id]['fish_catches'][fish_number] += 1


        save_user_data()

        await gacha_riddle(ctx.author)
        await ctx.respond(catchphrase)

# ---------------------------------------------------------------- Darting Game ----------------------------------------------------------------

class DartGameButton(Button["DartGame"]):
    def __init__(self, number):
        if number < 6 or (19 < number < 26) or ((number-1)%5 == 0 ) or (number%5 == 0 )  :
            super().__init__(style=discord.ButtonStyle.primary, label="\u200b", row=int((number-1)/5))
        elif number == 13 :
            super().__init__(style=discord.ButtonStyle.gray, label="\u200b", row=int((number-1)/5))
        else :
            super().__init__(style=discord.ButtonStyle.danger, label="\u200b", row=int((number-1)/5))
        self.number = number

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: DartGame = self.view
        if view.finished:
            return

        random_number = random.randint(1, 25)
        if self.number == random_number:
            self.style = discord.ButtonStyle.success
            self.label = "🎯"
            content = "You won bro"
            await gacha_riddle(interaction.user)
        else:
            correct_button = view.children[random_number - 1]
            correct_button.style = discord.ButtonStyle.success
            correct_button.label = "😏"
            self.label = "✖️"
            content = f"You suck, the lucky number was {random_number}"

        # Disable all buttons in the view
        for button in view.children:
            button.disabled = True

        view.finished = True
        # Edit the embed description to display the result
        embed = interaction.message.embeds[0]
        embed.description = content
        await interaction.response.edit_message(embed=embed, view=view)

class DartGame(View):
    children: List[DartGameButton]

    def __init__(self):
        super().__init__()
        self.finished = False

        for number in range(1, 26):
            self.add_item(DartGameButton(number))

@bot.slash_command(name="shoot", description="Dart n' Decode")
async def shoot(ctx: commands.Context):
    """Play the Dart Game."""
    embed = discord.Embed(title="Dart Game", description="Click a button to throw a dart.", color=discord.Color.blue())
    await ctx.respond(embed=embed, view=DartGame())

# ---------------------------------------------------------------- MISCELANNOUS ------------------------------------------------------------------

@bot.slash_command(name = "mystery", description = "Mystery Matsuri Commands")
async def mystery(ctx):
    embed = discord.Embed(title="Mystery Matsuri Commands", color=discord.Color.gold())

    # Add commands for Scoop n' Solve
    scoop_commands = [
        "`/fish info` : to view gameplay and prizes",
        "`/fish help` : to view all commands",
        "`/fish list` : to view 28 types of goldfish",
        "`/fish collection` : to view your goldfish collection",
        "`/scoop` : to play fish scooping!"
    ]
    embed.add_field(name="Scoop n' Solve Commands", value='\n'.join(scoop_commands), inline=False)

    # Add commands for Dart n' Dash
    dart_commands = [
        "`/dart info` : to view the gameplay and prizes",
        "`/dart help` : to view all commands",
        "`/shoot` : to play target shooting~"
    ]
    embed.add_field(name="Dart n' Dash Commands", value='\n'.join(dart_commands), inline=False)

    # Add commands for Dine n' Decode
    dine_commands = [
        "`/dine info` : to view how to order and dine",
        "`/dine menu` : to view the menu",
        "`/order` : to place an order",
        "`/deliver` : to fulfill an order (command for Class 1-D students only)"
    ]
    embed.add_field(name="Dine n' Decode Commands", value='\n'.join(dine_commands), inline=False)

    # Add commands for Riddles
    riddle_command = ["/ans : to send an answer to a riddle"]
    embed.add_field(name="Riddles", value='\n'.join(riddle_command), inline=False)
    await ctx.respond(embed= embed)   

@bot.slash_command(name = "dmme", description = "Giving ya a DM")
@commands.cooldown(1, 5 * 60, commands.BucketType.user)
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

@bot.slash_command(name="boo")
async def boo(ctx) :
    await ctx.respond("boo hoo hoo hoo")
    await gacha_riddle(ctx.author)

# randomizer (for riddle)
async def gacha_riddle(user) :
    rng = 1
    if rng == 1 :
        embed = discord.Embed(title="Pss, You got a secret message",
                              description = "please use `/solve` to solve the riddle",
                              color=discord.Color.orange())
        embed.set_image(url="https://cdn.discordapp.com/attachments/1160145573039583232/1160146204194263111/RIDDLE_1.png?ex=65339959&is=65212459&hm=e6a1df44b9590b142f24d2be8f471afc2cfa10a54a486b0af629b28c2c7d9b5d&")
        await user.send(embed=embed)

    




bot.run(TOKEN)
import asyncio
import json
import os
import random
from typing import List
from datetime import datetime

import discord
from discord.ext import commands
from discord.ui import View
from discord.ui.button import Button

# importing data from data.py
from data import fish_catchphrases, fish_data, riddle, prize, food_menu, food_gifs, broke_message, shoot_message, shoot_success, scoop_fail, food_prepare

TOKEN = 'MTE1ODQwMTU3ODIzMTkzMDk1NA.G23a-m.ft60RZenPUbf2jmm3HiKPZkf4rJLPR2yt2SBhY'

intents = discord.Intents.all()
bot = discord.Bot(intents=intents)

fish_cmds = ['info', 'list', 'collection']
dart_cmds = ['info']
dine_cmds = ['info', 'menu']

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


def check_data(user_id):
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
      await ctx.respond(
          f"The command is on cooldown, please try again in `{days} day{'s' if days > 1 else ''}.`"
      )
    elif retry_after >= 3600:  # More than an hour
      hours = int(retry_after // 3600)
      await ctx.respond(
          f"The command is on cooldown, please try again in `{hours} hour{'s' if hours > 1 else ''}.`"
      )
    elif retry_after >= 60:  # More than a minute
      minutes = int(retry_after // 60)
      await ctx.respond(
          f"The command is on cooldown, please try again in `{minutes} minute{'s' if minutes > 1 else ''}.`"
      )
    else:
      await ctx.respond(
          f"The command is on cooldown, please try again in `{round(retry_after, 2)} seconds.`"
      )
  else:
    raise error


# ---------------------------------------------------------------- SLASH COMMANDS ----------------------------------------------------------------

# ---------------------------------------------------------------- FORTUNE  ----------------------------------------------------------------


@bot.slash_command(name="fortune", description="to check your daily fortune")
@commands.cooldown(1, 24 * 60 * 60, commands.BucketType.user)
async def fortune(ctx):
  await ctx.respond("Opening the fortune slip...")

  fortune_result = random.choice([
      "**A Great Fortune!**\n\nCongratulations! Great Fortune smiles upon you. May your path be filled with joy, success, and all the splendid surprises life has to offer!",
      "**A Good Fortune!**\n\nGood Fortune smiles upon you! May this auspicious blessing illuminate your path with abundance joy and prosperity.",
      "**A Modest Fortune!**\n\nA modest fortune beckons you. May this humble blessing accompany you, bringing steady joys and quiet contentment on your journey through life.",
      "**A Modest fortune!**\n\nWith a modest fortune, you have the chance to be a beacon of kindness and gratitude, sharing your inner wealth with others. Your actions, no matter how small, can ripple out and create a more compassionate world. So, embrace your modest fortune with an open heart, and let it illuminate the path of contentment and joy.",
      "**A Rising Fortune!**\n\nA rising fortune graces your path. May each step lead to new heights of joy, prosperity, and unexpected blessings.",
      "**A Rising Fortune!**\n\nAs your fortune continues to ascend, keep your heart open to the abundance of experiences and connections that await you. May your rising fortune lead you to a brighter future filled with joy, success, and the fulfillment of your dreams.",
      "**A Misfortune!**\n\nIn the realm of misfortune, may you find the fortitude to endure the challenges that unfold. Remember, resilience often emerges from the echoes of adversity.",
      "**A Misfortune!**\n\nEmbrace this moment as an opportunity to sharpen your wits and intuition. Within the depths of the mysteries, there lies the potential for personal growth and resilience. Trust your instincts, seek the truth, and navigate this uncertain journey with courage and discernment.",
      "**A Great Misfortune!**\n\nGreat Misfortune befalls you. In the shadows of adversity, tread cautiously, for the road ahead may be laden with challenges. May you find strength in the face of an uncertain journey."
  ])

  user_id = str(ctx.author.id)

  # Ran's misfortune
  if user_id == "654832174566080522":
    fortune_result = "**A Great Misfortune!**\n\nIn the shadow of great misfortune, your path takes on an ominous hue and the journey ahead appears mysterious. In the face of uncertainty, it's important to tread in caution, there may be elements of deceit that seek to challenge you, for the allure of the unknown can sometimes conceal the most ominous secrets."

  # Check if the user has a balance entry, create one if not
  check_data(user_id)

  # Check if the user can work (based on cooldown or other criteria)
  earnings = random.randint(10, 30)
  user_data[user_id]['balance'] += earnings
  save_user_data()

  fortune = discord.Embed(
      title="FORTUNE SLIP <:fortuneslip:1161301922117066833>",
      description=f"{fortune_result}\n\n"
      f"You earned **{earnings}** <:sakura:1159350038959505468>",
      color=discord.Color.gold())
  fortune.set_image(
      url=
      'https://cdn.discordapp.com/attachments/1152924238429294632/1161605995026456596/IMG_0767.jpg?ex=6538e8e2&is=652673e2&hm=fa598b926f86ded0647ba6a5320bb4ae89d4006a46f3c3a76eb8b26899700b91&'
  )
  fortune.set_thumbnail(url=ctx.author.avatar.url)
  fortune.set_footer(text="Mystery Matsuri | Daily Fortune")

  # Send a new interaction response with the embed
  await ctx.send(embed=fortune)


@bot.slash_command(name="balance", description="to check your balance")
async def balance(ctx):
  user_id = str(ctx.author.id)

  # Check if the user has a balance entry, create one if not
  check_data(user_id)

  bal = user_data[user_id]['balance']
  # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Updating it to be embed
  await ctx.respond(f'Your balance is `{bal}` <:sakura:1159350038959505468>')


# ---------------------------------------------------------------- DINE N' DECODE -----------------------------------------------------------------


@bot.slash_command(name="dine", description="Dine n' Decode")
async def dine(ctx: commands.Context,
               option: discord.Option(str, choices=dine_cmds)):
  if option == 'info':
    await dine_info(ctx)
  if option == 'menu':
    await dine_menu(ctx)


# DINE N' DECODE INFO


async def dine_info(ctx: commands.Context):
  embed = discord.Embed(
      title="DINE N' DECODE",
      description=
      "Experience the fusion of Japanese flavors and brain-teasing riddles here at **Dine n' Decode**! Get ready to savor Japanese street foods and sweets while unlocking clues to unravel our enigmatic dining experience~\n",
      color=discord.Color.green())

  embed.add_field(
      name="**How to order and dine:**",
      value=
      ("- Use slash command `/dine` `menu` to check what food we offer~\n"
       "- Use slash command `/order` to place your order. You can only order one food at a time in every **15 minutes**.\n"
       "- Once your order has been placed, kindly wait for our staff to deliver your food. You will be notified when it's done.\n"
       "- Depending on the food, you'll probably get a **random riddle** to answer. Use slash command `/ans` to send your answer.\n"
       "- Enjoy the dining experience and the festivities~"))

  embed.set_image(
      url=
      "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/618395ed-3302-4408-bcd8-4ce51cc8b364/deoioou-d38e35ff-bf55-4160-835a-dec07338a5fe.gif?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcLzYxODM5NWVkLTMzMDItNDQwOC1iY2Q4LTRjZTUxY2M4YjM2NFwvZGVvaW9vdS1kMzhlMzVmZi1iZjU1LTQxNjAtODM1YS1kZWMwNzMzOGE1ZmUuZ2lmIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.F_NkKnBOQ-CENyMP9r3dr8qODWfa3tTW6ggHHiT40jQ"
  )
  embed.set_footer(text="Mystery Matsuri | Dine n' Decode")

  await ctx.respond(embed=embed)


# DINE N' DECODE MENU
async def dine_menu(ctx: commands.Context):
  embed = discord.Embed(color=discord.Color.green())
  embed.set_image(
      url=
      "https://cdn.discordapp.com/attachments/1154695654501785620/1159916352933482606/menu-01.png?ex=6532c348&is=65204e48&hm=6e62e4c3f65df22063f0d28825f0c7fb650c2d3d3fed29533b63656c2e6daa84&"
  )
  embed.set_footer(text="Mystery Matsuri | Dine n' Decode")

  await ctx.respond(embed=embed)


# ---------------------------------------------------------------- ORDER COMMAND -------------------------------------------------------

food = [
    'Nikuman', 'Gyoza', 'Yaki tomorokoshi', 'Yakitori', 'Ikayaki',
    'Okonomiyaki', 'Yakisoba', 'Takoyaki', 'McConan', 'Taiyaki', 'Kibi dango',
    'Ringo ame', 'Kakigori', 'Anmitsu', 'Watame', 'Crepes', 'Ice cream',
    'Parfait', 'Water bottle', 'Soda', 'Juice', 'Boba milk tea'
]


# ORDER COMMAND - TO PLACE AN ORDER
@bot.slash_command(name="order", description="to place an order")
@commands.cooldown(1, 10 * 60, commands.BucketType.user)
async def order(ctx: commands.Context,
                food: discord.Option(str, choices=food, required=True),
                request: str = None):
  price = food_menu[food]

  user_id = str(ctx.author.id)
  check_data(user_id)
  bal = user_data[user_id]['balance']

  # checkin whether user has the money to buy food or not
  if bal < price:
    await ctx.respond(
        f"Hey {ctx.author.mention}, {random.choice(broke_message)}")
    return

  user_data[user_id]['balance'] -= price
  save_user_data()

  await gacha_riddle(ctx.author, "order")

  food_gifs = food_prepare.get(food, [])

  if isinstance(food_gifs, list):
    # If there are multiple GIFs associated with the food, select one randomly
    selected_gif_url = random.choice(food_gifs)
  elif isinstance(food_gifs, str):
    # If there's a single GIF URL associated with the food, use it
    selected_gif_url = food_gifs

  # order confirmation embed in dine n' decode channel
  embed = discord.Embed(
      title="🧾 Order Confirmation 🧾",
      description=
      f"Hi {ctx.author.mention}! <a:goubawave:1155587291062997012>\n\n"
      f"Your order has been received and is currently being prepared with care. Our chefs are working their magic~ <a:dsparkles:1155585454603780196>\n\n"
      f"Here's a summary of your request:\n"
      f"- `ORDER   :`\t {food} \n"
      f"-----------------------------\n"
      f"- `COST    :`\t {price} \n\n"
      f"We'll notify you once it's ready. In the meantime, feel free to chat and enjoy the festivities! <a:dctakagidance:1035648909193785464>\n\n"
      f"Thank you for choosing **Dine n' Decode**~",
      color=discord.Color.green())
  embed.set_thumbnail(url=ctx.author.avatar.url)
  embed.set_image(url=selected_gif_url)
  embed.set_footer(text="Mystery Matsuri | Dine n' Decode")

  # order request embed to send in kitchen channel
  embed_kitchen = discord.Embed(
      title="🗒️ Order Request 🗒️",
      description="A new order has been placed. Please make it ASAP!\n\n"
      f"**ORDER DETAILS**:\n"
      f"- `CUSTOMER:`\t {ctx.author.mention} \n"
      f"- `ORDER   :`\t {food} \n"
      f"- `COST    :`\t {price} \n"
      f"- `REQUEST :`\t {request} \n\n"
      "Use slash command `/deliver` to prompt delivery of this order and provide an excellent service. The customer will be notified once their order is delivered. Please react :white_check_mark: once it's done.",
      color=discord.Color.green())
  embed_kitchen.set_image(
      url="https://media.giphy.com/media/mNQxKBlgG3mqHS7W2a/giphy.gif")
  embed_kitchen.set_thumbnail(url=ctx.author.avatar.url)
  embed_kitchen.set_footer(text="Mystery Matsuri | Dine n' Decode")

  # sending the order to the kitchen
  thread_id = ctx.guild.get_channel_or_thread(
    1156982446156419233)  # TBC kitchen channel
  await thread_id.send(embed=embed_kitchen)

  # giving the receipt to the user
  await ctx.respond(
      f"Got it, {ctx.author.mention}! Your order has been placed. 🧾\n\n",
      embed=embed)


# ---------------------------------------------------------------- DELIVER COMMAND -------------------------------------------------------


# DELIVER COMMAND - TO FULFILL AN ORDER
@bot.slash_command(
    name="deliver",
    description=
    "to deliver an order to the customer *command for class D students only*")
async def deliver(ctx: commands.Context,
                  customer: discord.Option(discord.SlashCommandOptionType.user,
                                           required=True),
                  food: discord.Option(discord.SlashCommandOptionType.string,
                                       choices=food,
                                       required=True),
                  message: str = None):

  user = ctx.author
  if message == None :
    message = "Enjoy your meal! 😋"

  allowed_role = discord.utils.get(user.roles, id=1076229438213206047)  # TBC

  if allowed_role is None:
    await ctx.respond(
        "<a:purple_exclamation:1159577549186277426> Unauthorized access. This command is reserved for <@1076229438213206047> students and chefs only. <a:purple_exclamation:1159577549186277426>"
    )
    return

  food_gif_urls = food_gifs.get(food)

  if isinstance(food_gif_urls, list):
    food_gif = random.choice(food_gif_urls)
  else:
    food_gif = food_gif_urls
  embed_user = discord.Embed(
      title=
      "<a:foodtakeout:1155780015082979338> FOOD DELIVERY <a:foodtakeout:1155780015082979338>",
      description=f"Hi {customer.mention}! <a:goubawave:1155587291062997012>\n\n"
      f"Here is your **{food}**~ <a:yyum:1155585450224930836>\n\n"
      f"\"*{message}*\"\n\n"
      f"Served by: {user.mention} <a:chefshat:1155774533266051102>",
      color=discord.Color.green(),
      timestamp=datetime.now())

  embed_user.set_thumbnail(url=customer.avatar.url)
  embed_user.set_footer(text="Mystery Matsuri | Dine n' Decode")
  embed_user.set_image(url=food_gif)

  # sending the food to the customer
  thread_id = ctx.guild.get_channel_or_thread(1161734275134144522)  # TBC to dine n' decode channel
  await thread_id.send(
      f"Your order is here {customer.mention}~ <a:fooddelivery:1155777956749250636>",
      embed=embed_user)

  # notifying the cook that the order is delivered
  await ctx.respond(
      # TBC mention the dine n' decode
      f"{customer.mention}'s order of **{food}** has been delivered in <#1161734275134144522>. <a:fooddelivery:1155777956749250636>"
  )


# ---------------------------------------------------------------- FISH SCOOPING -----------------------------------------------------------------


@bot.slash_command(name="fish", description="Scoop n' Solve")
async def fish(ctx: commands.Context,
               option: discord.Option(str, choices=fish_cmds)):
  if option == 'info':
    await fish_info(ctx)
  elif option == 'list':
    await fish_list(ctx)
  elif option == 'collection':
    await fish_collection(ctx)
  else:
    await ctx.respond(
        "Invalid option. Please choose from: info, help, list, collection")


# FISH INFO
async def fish_info(ctx: commands.Context):
  embed = discord.Embed(
      title="SCOOP N' SOLVE",
      description=
      "Experience the joy of catching fish and solving riddles! Inspired by the classic Japanese festival game “Kingyu Sukui” where players use a paper scooper to catch goldfish from a pond.",
      color=discord.Color.orange())

  embed.add_field(
      name="**Gameplay:**",
      value=
      ("- Use the slash command `/scoop` to play fish scooping.\n"
       "- There are 28 unique goldfish species available to catch. Collect them all for a special prize!\n"
       "- Keep an eye out for random *fishy* riddles. Successfully solving these riddles will earn you valuable clues for the mystery game. Use command `/ans` to send your answer to a riddle~\n"
       "- Enjoy scooping up goldfish, solving riddles, and working toward the prizes!"
       ))

  embed.add_field(
      name="**Prizes:**",
      value=
      ("- You get 1 <:sakura:1159350038959505468> for every goldfish you catch.\n"
       "- The first player to complete a set (28 species of goldfish) can receive a 10k <:dccoin:722844861148955021> coupon.\n"
       ),
      inline=False)

  image_url = 'https://i.pinimg.com/originals/60/1f/68/601f68d55572d5ea2e42b2e85bc8b333.gif'
  embed.set_image(url=image_url)
  embed.set_footer(text="Mystery Matsuri | Scoop n' Solve")

  await ctx.respond(embed=embed)


# FISH LIST
async def fish_list(ctx: commands.Context):
  embed = discord.Embed(color=discord.Color.orange())
  embed.set_image(
      url=
      "https://cdn.discordapp.com/attachments/1154695654501785620/1156912343138185226/Fish_List.png?ex=6516b214&is=65156094&hm=3291ea33884896639f7e753f2acbe10e8acd3d115d8cb4ff12614149e264d663&"
  )

  embed.set_footer(text="Mystery Matsuri | Scoop n' Solve")

  await ctx.respond(embed=embed)


# FISH COLLECTION
async def fish_collection(ctx: commands.Context):
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
    # Adjust index since fish numbers start from 1
    fish_entry = fish_data[int(fish_number) - 1]
    fish_name = fish_entry["name"]
    emote_id = fish_entry["emote_id"]
    formatted_fish = f"`#{fish_number}` {fish_name} {emote_id} \t× {count}"

    # Add to the appropriate column list
    if len(column1) < 14:
      column1.append(formatted_fish)
    else:
      column2.append(formatted_fish)

  # Create an embed with two fields (left and right) with inline format
  embed = discord.Embed(
      title="**Fish Collection**",
      description=
      f"Goldfishes owned by {ctx.author.mention} <a:goldfishfish:1156278359446265926>",
      color=discord.Color.orange())

  embed.add_field(name="", value="\n".join(column1), inline=True)
  embed.add_field(name="", value="\n".join(column2), inline=True)
  embed.set_footer(text="Mystery Matsuri | Scoop n' Solve")

  await ctx.respond(embed=embed)


# SCOOP COMMAND
@bot.slash_command(name="scoop", description="Scooping a fish")
@commands.cooldown(1, 1 * 60, commands.BucketType.user)
async def scoop(ctx):
  rng = random.randint(0, len(fish_data) - 1)  # Pick a random fish index
  fish = fish_data[rng]

  fish_name = f"{fish['name']}"
  fish_number = fish['number']
  emote_id = fish['emote_id']

  # Pick a random catchphrase
  rng2 = random.randint(1, 70)

  if rng2 >= 29:
    await ctx.respond(random.choice(scoop_fail))
  else:
    catchphrase_template = fish_catchphrases[f"{rng2}"]
    catchphrase = catchphrase_template.format(user=ctx.author,
                                              fish_number=fish_name,
                                              emote_id=emote_id)

    user_id = str(ctx.author.id)
    check_data(user_id)
    user_data[user_id]['balance'] += 1
    user_data[user_id]['fish_catches'][fish_number] += 1

    save_user_data()

    await gacha_riddle(ctx.author, "scoop")
    await ctx.respond(catchphrase)


# ---------------------------------------------------------------- DART N' DASH ----------------------------------------------------------------


@bot.slash_command(name="dart", description="Dart n' Dash")
async def dart(ctx: commands.Context,
               option: discord.Option(str, choices=dart_cmds)):
  if option == 'info':  # DART N' DASH INFO
    embed = discord.Embed(
        title="DART N' DASH",
        description=
        "Get your aim ready and dash to victory at the **Dart n' Dash** shooting game! Test your ~~luck in~~ sharpshooting skills and win exciting prizes.  Hit the lucky target, unlock prizes or clues, and experience the mystery action-adventure event for fun~\n\n",
        color=discord.Color.blue())

    embed.add_field(
        name="**How to play:**",
        value=
        ("- Use slash command `/shoot` to start play\n"
         "- Select a target. Note that \\*lucky\\* target is random and you have a 30% chance to hit it.\n"
         "- Once you hit the \\*lucky\\* target, you should get your prize or clue in DMs. Make sure your DMs in this server are open.\n"
         "- Enjoy our mystery action-adventure shooting game~"))
    embed.set_image(
        url=
        "https://cdn.discordapp.com/attachments/1154695654501785620/1159466920140095498/dart-n-dash-2.gif?ex=653120b7&is=651eabb7&hm=87502483b676dc1e2a8b7624&"
    )
    embed.set_footer(text="Mystery Matsuri | Dart n' Dash")
    await ctx.respond(embed=embed)


# ---------------------------------------------------------------- SHOOTING GAME ----------------------------------------------------------------


class DartGameButton(Button["DartGame"]):

  def __init__(self, number):
    if number < 6 or (19 < number < 26) or ((number - 1) % 5
                                            == 0) or (number % 5 == 0):
      super().__init__(style=discord.ButtonStyle.primary,
                       label="\u200b",
                       row=int((number - 1) / 5))
    elif number == 13:
      super().__init__(style=discord.ButtonStyle.gray,
                       label="\u200b",
                       row=int((number - 1) / 5))
    else:
      super().__init__(style=discord.ButtonStyle.danger,
                       label="\u200b",
                       row=int((number - 1) / 5))
    self.number = number

  async def callback(self, interaction: discord.Interaction):
    assert self.view is not None
    view: DartGame = self.view
    if view.finished:
      return

    random_number = random.randint(0, 4)
    if random_number == 1:
      self.style = discord.ButtonStyle.success
      self.label = "🎯"
      content = f"{random.choice(shoot_success)}"
      # RIP
      await gacha_prize(interaction.user, interaction.message.channel)

    else:
      rng = random.choice([n for n in range(1, 26) if n != self.number])
      correct_button = view.children[rng - 1]
      correct_button.style = discord.ButtonStyle.success
      correct_button.label = "🤪"
      self.label = "✖️"
      content = random.choice(shoot_message)

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


@bot.slash_command(name="shoot", description="to play dart shooting game")
@commands.cooldown(1, 5 * 60, commands.BucketType.user)
async def shoot(ctx: commands.Context):
  """Play the Dart Game."""
  embed = discord.Embed(
      title=
      "<a:lineblue:1155793338197356545><a:lineblue:1155793338197356545> <:aim:1155585587424804974> DART N' DASH <:aim:1155585587424804974> <a:lineblue:1155793338197356545><a:lineblue:1155793338197356545>",
      description="Click a button to throw a dart. <:dart:1155585583805108225>",
      color=discord.Color.blue())
  embed.set_footer(text="Mystery Matsuri | Dart n' Decode")
  await ctx.respond(embed=embed, view=DartGame())


# ---------------------------------------------------------------- RIDDLES ------------------------------------------------------------------

# randomizer (for riddle)


async def gacha_prize(user, channel):
  rng = random.randint(1, 100)
  if 1 <= rng <= 45:  # dummy prize
    gift = random.choice(prize)
    embed = discord.Embed(title=gift['title'],
                          description=gift['description'],
                          color=discord.Color.blue())
    embed.set_image(url=gift['image'])
    await channel.send(
        f"<a:purple_arrow:1159577384756969504> Congratulations {user.mention}! You won a prize~",
        embed=embed)

  elif 46 <= rng <= 65:  # sakura
    user_id = str(user.id)
    check_data(user_id)
    user_data[user_id]['balance'] += 10
    save_user_data()
    await channel.send(
        f"<a:purple_arrow:1159577384756969504> Congratulations {user.mention}! Your precision in the **Dart n' Dash** game is unmatched! Here's 10 <:sakura:1159350038959505468> added to your balance~"
    )

  elif 66 <= rng <= 80:  # sakura
    user_id = str(user.id)
    check_data(user_id)
    user_data[user_id]['balance'] += 45
    save_user_data()
    await channel.send(
        f"<a:purple_arrow:1159577384756969504> Well done, sharpshooter {user.mention}! With pinpoint accuracy in **Dart n' Dash** game, you won 45 <:sakura:1159350038959505468>! Spend them wisely~"
    )

  elif 81 <= rng <= 90:  # voucher
    embed = discord.Embed(
        title="A 10k <:dccoin:722844861148955021> Voucher!",
        description=
        f"<a:purple_arrow:1159577384756969504> Congratulations, {user.mention}! You earned yourself a 10k <:dccoin:722844861148955021> voucher."
        f"\n\nSend a screenshot of this in <#1161734128593539072> and tag <@685776874265509911> or <@732966109916954677> to claim~",  # TBC TBD
        color=0xa700f5,
        timestamp=datetime.now())
    embed.set_image(
        url=
        "https://cdn.discordapp.com/attachments/1160198592695377920/1160859498899046460/10K-dc-coins-voucher-03.png?ex=653631a8&is=6523bca8&hm=41eea2651ca18ceaa4d2436ea36ed595f9b8f2f3b3b5259a3d115a9e5fee0ea4&"
    )
    embed.set_footer(text="Mystery Matsuri | Dart n' Decode")
    await channel.send(embed=embed)

  elif 91 <= rng <= 100:  # riddle
    await gacha_riddle(user, "shoot")


async def gacha_riddle(user, str):
  rng = random.randint(0, 8)  # TBC
  if rng == 1 or str == "shoot":  # bypass shooting
    if str == "scoop":
      rng2 = random.randint(1, 5)
      embed = discord.Embed(
          title=f"RIDDLE #{rng2}",
          # TBC
          description=
          f"Hey {user.mention}, you've successfully hooked a riddle! \n\nUse the slash command `/ans` in <#1161722366167109653> to send your answer to the riddle.",
          colour=0xa700f5,
          timestamp=datetime.now())
      embed.set_image(url=riddle[f"{rng2}"])
      embed.set_footer(text="Mystery Matsuri | Scoop n' Solve")
    elif str == "shoot":
      rng2 = random.randint(6, 10)
      embed = discord.Embed(
          title=f"RIDDLE #{rng2}",
          # TBC
          description=
          f"Impressive shooting skills, {user.mention}! Now to keep your mind sharp, take a shot to decode this riddle. 🎯\n\nUse the slash command `/ans` in <#1161722366167109653> to send your answer to the riddle.",
          colour=0xa700f5,
          timestamp=datetime.now())
      embed.set_image(url=riddle[f"{rng2}"])
      embed.set_footer(text="Mystery Matsuri | Dart n' Dash")
    else:
      rng2 = random.randint(11, 15)
      embed = discord.Embed(
          title=f"RIDDLE #{rng2}",
          description=
          f"Thanks for your order, {user.mention}! As you wait for your delicious meal, here's a random \\*food for thought\\* for you~ <a:foodtakeout:1155780015082979338>\n\nUse the slash command `/ans` in <#1161722366167109653> to send your answer to the riddle.",  # TBC
          colour=0xa700f5,
          timestamp=datetime.now())
      embed.set_image(url=riddle[f"{rng2}"])
      embed.set_footer(text="Mystery Matsuri | Dine n' Decode")
    await user.send(embed=embed)


# ---------------------------------------------------------------- CLUES ------------------------------------------------------------------


# CLUES EMBEDS
@bot.slash_command(name="ans", description="to send your answer to a riddle")
@commands.cooldown(1, 5 * 60, commands.BucketType.user)
async def ans(
    ctx, answer: str):  # to be implemented : limit how many ans user can send
  user = ctx.author  # Get the user who sent the command
  reply = ""
  num = -1

  if answer == "deck of cards":  # CLUE 1
    embed = discord.Embed(
        title="CLUE #1",
        description=
        "*Continuing your fish scooping adventure, you spot a calendar submerged beneath the surface. Could there be any significant events marked on these dates?*",
        color=discord.Color.purple())
    embed.set_image(
        url=
        "https://cdn.discordapp.com/attachments/1154474063750766694/1160975540933636136/1CLUE.png?ex=65369dba&is=652428ba&hm=f4eaa216ab74d366d95205a8ce69b5d40e4d3e76ca102f02c077b2eb402e1f24&"
    )
    num = 1
    await user.send(embed=embed)

  elif answer in ("an echo", "echo"):  # CLUE 2
    embed = discord.Embed(
        title="CLUE #2",
        description=
        "*While playing scoop, you found a piece of photo on the ground and picked it up. This surely is a clue to the mystery case!*",
        color=discord.Color.purple())
    embed.set_image(
        url=
        "https://cdn.discordapp.com/attachments/1154474063750766694/1160975634634387799/2CLUE.png?ex=65369dd1&is=652428d1&hm=a4897e4204db2fc3c77f7e1a0524c4f23f9c5435fe5020fcd8f0643dc91a2867&"
    )
    num = 2
    await user.send(embed=embed)

  elif answer in ("fishhook", "fish hook", "bait"):  # CLUE 3
    embed = discord.Embed(
        title="CLUE #3",
        description=
        "*While scooping, you found a piece of paper lying on the ground. A clue that will lead you in solving the case!*",
        color=discord.Color.purple())
    embed.set_image(
        url=
        "https://cdn.discordapp.com/attachments/1154474063750766694/1160975691177791568/3CLUE.png?ex=65369dde&is=652428de&hm=811c3306ac26d6850173004d82c38ac46ade6913fd65ef00b260fe7ae139965a&"
    )
    num = 3
    await user.send(embed=embed)

  elif answer == "something catchy":  # CLUE 4
    embed = discord.Embed(
        title="CLUE #4",
        description=
        "*While scooping up a goldfish, a photo suddenly slapped onto your face, almost making you drop your net. Luckily, you still caught the goldfish. But when you took a closer look at the photo now in your other hand, you couldn't help but notice that there's something wrong...*",
        color=discord.Color.purple())
    embed.set_image(
        url=
        "https://cdn.discordapp.com/attachments/1154474063750766694/1160977136539156490/4CLUE.png?ex=65369f37&is=65242a37&hm=4d000f7742646942a7252520e2e3fff743515ae37172dc8348fe0c7fccae3cd9&"
    )
    num = 4
    await user.send(embed=embed)

  elif answer in ("they are all married", "they were all married",
                  "couples"):  # Riddle 5
    embed = discord.Embed(
        title="CLUE #5",
        description=
        "*In the midst of your fish scooping adventure, you stumble upon a torn note with the word 'murderer' written in red, with series of cryptic numbers. The ominous message sends shivers down your spine, raising more questions about the mystery...*",
        color=discord.Color.purple())
    embed.set_image(
        url=
        "https://cdn.discordapp.com/attachments/1154474063750766694/1160977560629432510/5CLUE.png?ex=65369f9c&is=65242a9c&hm=8f10606e25710c62fca055a9bdbe207d201bb66d3ab4a8c838e46c9884fdde8b&"
    )
    num = 5
    await user.send(embed=embed)

  elif answer in ("aeiou", "vowels"):  # CLUE 6
    embed = discord.Embed(
        title="CLUE #6",
        description=
        "*As you take aim and fire another dart, you notice something peculiar—a ripped piece of paper with a series of mysterious numbers etched onto it. It's an intriguing find, to say the least.*",
        color=discord.Color.purple())
    embed.set_image(
        url=
        "https://cdn.discordapp.com/attachments/1154474063750766694/1161005417846022304/6CLUE.png?ex=6536b98e&is=6524448e&hm=ce0133494692336becc83d14c11e47ae11ae7a89f558aa2fe83813d941846554&"
    )
    num = 6
    await user.send(embed=embed)

  elif answer == "queue":  # CLUE 7
    embed = discord.Embed(
        title="CLUE #7",
        description=
        "*In the midst of your dart-throwing adventure, you discover something unexpected— You found a piece of photo attached on the dart board. Seems to be a clue to the mystery murder case of Ran!*",
        color=discord.Color.purple())
    embed.set_image(
        url=
        "https://cdn.discordapp.com/attachments/1154474063750766694/1161005673291726878/7CLUE.png?ex=6536b9ca&is=652444ca&hm=023ee34dd7e1dba076283d1479954d8dba47ea67aae843ca4f83532dd54abf66&"
    )
    num = 7
    await user.send(embed=embed)

  elif answer == "empty":  # CLUE 8
    embed = discord.Embed(
        title="CLUE #8",
        description=
        "*A well-aimed shot reveals more than just points. You found something sticking out from beneath the dartboard. It's a mysterious clue that might hold the key in solving the case!*",
        color=discord.Color.purple())
    embed.set_image(
        url=
        "https://cdn.discordapp.com/attachments/1154474063750766694/1161005810575478824/8CLUE.png?ex=6536b9eb&is=652444eb&hm=ce7771807c9206a8e0885012e28236925be1d2617c3cb1566afe4e1f50223750&"
    )
    num = 8
    await user.send(embed=embed)

  elif answer in ("m", "M", "letter M"):  # CLUE 9
    embed = discord.Embed(
        title="CLUE #9",
        description=
        "*Your throw is particularly accurate, you hit a calendar on the wall. Dislodging it and revealing a significant date marked in red. It seems this date holds a clue of its own.*",
        color=discord.Color.purple())
    num = 9
    embed.set_image(
        url=
        "https://cdn.discordapp.com/attachments/1154474063750766694/1161005941492285610/9CLUE.png?ex=6536ba0a&is=6524450a&hm=7bed97d77c7b921c5cffa0d68a3abdd14fd3fe97dbe29d7fd70204dc6f74a2ad&"
    )
    await user.send(embed=embed)

  elif answer in ("ENT", "E N T", "ent"):  # CLUE 10
    embed = discord.Embed(
        title="CLUE #10",
        description=
        "*As you take your final shot, your dart lands precisely on a photo tucked away in the corner. As you pick it up, you realize there's something peculiar about it. Could this be a significant clue in the unfolding mystery?*",
        color=discord.Color.purple())
    embed.set_image(
        url=
        "https://cdn.discordapp.com/attachments/1154474063750766694/1161006193116979290/10CLUE.png?ex=6536ba46&is=65244546&hm=89421c26f7caf73c44c33a9d11f0d5b24adffac7f55ad3cc4c022c9ad8b92cd3&"
    )
    num = 10
    await user.send(embed=embed)

  elif answer == "hand in hand":  # CLUE 11
    embed = discord.Embed(
        title="CLUE #11",
        description=
        "*As you savor your delicious special order, you notice something odd under your plate —it's a piece of torn paper! Perhaps it's a clue to the murder mystery?*",
        color=discord.Color.purple())
    embed.set_image(
        url=
        "https://cdn.discordapp.com/attachments/1154474063750766694/1161006321861152768/11CLUE.png?ex=6536ba65&is=65244565&hm=49beea91051c99ea4abf61bbfad39e55fe4f0071835da77695f0428960947620&"
    )
    num = 11
    await user.send(embed=embed)

  elif answer == "for once in a while":  # CLUE 12
    embed = discord.Embed(
        title="CLUE #12",
        description=
        "*As you enjoy your delicious Japanese feast at Dine n' Decode, you reach for your chopsticks and notice something unusual—a piece of torn paper hidden among the utensils. On closer inspection, you see it contains a cryptic message that begs for your attention.*",
        color=discord.Color.purple())
    embed.set_image(
        url=
        "https://cdn.discordapp.com/attachments/1154474063750766694/1161006430430707803/12CLUE.png?ex=6536ba7f&is=6524457f&hm=b6dc150d350ff18ef04c737dae42fdeca4a5c617549e30b2c84a522776f5fc30&"
    )
    num = 12
    await user.send(embed=embed)

  elif answer == "reverse psychology":  # CLUE 13
    embed = discord.Embed(
        title="CLUE #13",
        description=
        "*As you sip your drink, you can't help but glance at the calendar on the wall and noticed that dates were marked with events, but it appears there's something more important to notice.*",
        color=discord.Color.purple())
    embed.set_image(
        url=
        "https://cdn.discordapp.com/attachments/1154474063750766694/1161006505756201112/13CLUE.png?ex=6536ba91&is=65244591&hm=62bb06b7b0ddf2bf537a2bbfefb3304e615f3d030d47e956c7e29155146cc319&"
    )
    num = 13
    await user.send(embed=embed)

  elif answer == "candy":  # CLUE 14
    embed = discord.Embed(
        title="CLUE #14",
        description=
        "*While you're waiting for your food to arrive, you notice a torn photo lying on the countertop near the stall. The image is torn and incomplete, leaving you to wonder what this scene might reveal about the mystery...*",
        color=discord.Color.purple())
    embed.set_image(
        url=
        "https://cdn.discordapp.com/attachments/1154474063750766694/1161006582306439168/14CLUE.png?ex=6536baa3&is=652445a3&hm=1782957ef8b6c0ebc5bee300ae02ce5b6719296fefdc4b93519624dd0a18b8af&"
    )
    num = 14
    await user.send(embed=embed)

  elif answer == "upside down":  # CLUE 15
    embed = discord.Embed(
        title="CLUE #15",
        description=
        "*As you enjoy your meal, you find a ripped photo tucked under your napkin on the dining table. Perhaps this could be the missing piece in solving the mystery...?*",
        color=discord.Color.purple())
    embed.set_image(
        url=
        "https://cdn.discordapp.com/attachments/1154474063750766694/1161006718571008001/15CLUE.png?ex=6536bac4&is=652445c4&hm=d9b6784e2cccbd560e4e6748adfec9fe4dee61cbb9d9c21708c0abe56cecc877&"
    )
    num = 15
    await user.send(embed=embed)

  if num != -1:
    reply = "Your answer is correct. Please check your DM for a clue for the mystery game."
    thread_id = ctx.guild.get_channel_or_thread(
        1148136805116411975)  # TBC to the mystery event
    await thread_id.send(
        f"{user.mention} got the riddle correct and obtained the clue #{num}.")
  else:
    reply = "Your answer is incorrect. Take your time and give the riddle some careful thought."

  await ctx.respond(reply, ephemeral=True)


# solve the mystery


@bot.slash_command(name="solve", description="Solve the ongoing mystery")
@commands.cooldown(1, 30 * 60, commands.BucketType.user)
# @commands.cooldown(1, 24 * 60 * 60, commands.BucketType.user)
async def solve(ctx: commands.Context,
                culprit: discord.Option(discord.SlashCommandOptionType.string,
                                        required=True),
                crime: discord.Option(discord.SlashCommandOptionType.string,
                                      required=True),
                evidence: discord.Option(discord.SlashCommandOptionType.string,
                                         required=True),
                motive: discord.Option(discord.SlashCommandOptionType.string,
                                       required=True),
                conclusion: discord.Option(
                    discord.SlashCommandOptionType.string, required=True)):
  thread_id = ctx.guild.get_channel_or_thread(
      1148136805116411975)  # TBC to the kitchen channel
  embed = discord.Embed(
      title="Someone is trying to solve the mystery",
      description=f"{ctx.author.mention} is trying to solve the mystery\n\n"
      f"`Culprit`        : {culprit}\n\n"
      f"`Crime`          : {crime}\n\n"
      f"`Evidence`       : {evidence}\n\n"
      f"`Motive`         : {motive}\n\n"
      f"`Conclusion`     : {conclusion}",
      color=discord.Color.blue(),
      timestamp=datetime.now())

  await thread_id.send(embed=embed)
  await ctx.respond(
      "Thank you for giving us your thoughts, you answer has been sent to the detective to be reviewed",
      ephemeral=True)


# ---------------------------------------------------------------- ALL MYSTERY COMMANDS ------------------------------------------------------------------


@bot.slash_command(name="mystery", description="Mystery Matsuri Commands")
async def mystery(ctx):
  embed = discord.Embed(
      title="MYSTERY MATSURI COMMANDS",
      description=
      "Discover your way to an unforgettable festival where you scoop, shoot, dine, and unravel the secrets of <@&1076229438213206047> students have prepared for an immersive mystery festival experience! <a:kitsunebow:1156299105488871444>\n",
      color=discord.Color.purple())

  # Add commands for Scoop n' Solve
  scoop_commands = [
      "`/fish` `info` :\t to view gameplay and prizes",
      "`/fish` `list` :\t to view 28 types of goldfish",
      "`/fish` `collection` :\t to view your goldfish collection",
      "`/scoop` :\t to play fish scooping!\n"
  ]
  embed.add_field(name="<a:goldfishfish:1156278359446265926> Scoop n' Solve",
                  value='\n'.join(scoop_commands),
                  inline=False)

  # Add commands for Dart n' Dash
  dart_commands = [
      "`/dart` `info` :\t to view the gameplay and prizes",
      "`/shoot` :\t to play target shooting~\n"
  ]
  embed.add_field(name="<:target1:1155585593187762257> Dart n' Dash",
                  value='\n'.join(dart_commands),
                  inline=False)

  # Add commands for Dine n' Decode
  dine_commands = [
      "`/dine` `info` :\t to view how to order and dine",
      "`/dine` `menu` :\t to view the menu", "`/order` :\t to place an order",
      "`/deliver` :\t to fulfill an order (command for Class 1-D students only)\n"
  ]
  embed.add_field(name="<a:foodtakeout:1155780015082979338> Dine n' Decode",
                  value='\n'.join(dine_commands),
                  inline=False)

  # Add commands for Riddles
  riddle_command = [
      "`/ans` :\t to send an answer to a riddle",
      "`/solve` :\t to solve the mystery case",
      "`/fortune` :\t to check your daily fortune",
      "`/balance` :\t to check your balance"
  ]
  embed.add_field(name="<:kitsune:1156299235990450206> General Commands",
                  value='\n'.join(riddle_command),
                  inline=False)
  embed.set_image(
      url=
      "https://cdn.discordapp.com/attachments/1154695654501785620/1161282421505916989/class-1d-mystery-matsuri.png?ex=6537bb88&is=65254688&hm=029eda0d2a7f565c0e66ebaa1b4356ccb1a42c93e4a1916487fbf9591be17c42&"
  )
  embed.set_footer(text="Mystery Matsuri | Class 1-D")
  await ctx.respond(embed=embed)


# ----------------------------------------------------------------------------------------------------------

bot.run(TOKEN)

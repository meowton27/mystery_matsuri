import random
import discord

fish_data = [{
    "number": "01",
    "emote_id": "<:1f:1156919377308954654>",
    "name": "common"
}, {
    "number": "02",
    "emote_id": "<:2f:1156919381973028864>",
    "name": "comet"
}, {
    "number": "03",
    "emote_id": "<:3f:1156919386385428500>",
    "name": "wakin"
}, {
    "number": "04",
    "emote_id": "<:4f:1156919390692978698>",
    "name": "watonai"
}, {
    "number": "05",
    "emote_id": "<:5f:1156919394337832961>",
    "name": "london shubunkin"
}, {
    "number": "06",
    "emote_id": "<:6f:1156919396283977778>",
    "name": "american shubunkin"
}, {
    "number": "07",
    "emote_id": "<:7f:1156919400432156694>",
    "name": "bristol shubunkin"
}, {
    "number": "08",
    "emote_id": "<:8f:1156919403993112646>",
    "name": "jikin"
}, {
    "number": "09",
    "emote_id": "<:9f:1156919407893819504>",
    "name": "fantail"
}, {
    "number": "10",
    "emote_id": "<:10f:1156919412763410473>",
    "name": "sarasa"
}, {
    "number": "11",
    "emote_id": "<:11f:1156919416425037834>",
    "name": "calico"
}, {
    "number": "12",
    "emote_id": "<:12f:1156919418866114680>",
    "name": "veil tail"
}, {
    "number": "13",
    "emote_id": "<:13f:1156919422146060319>",
    "name": "oranda"
}, {
    "number": "14",
    "emote_id": "<:14f:1156919425849639003>",
    "name": "red cap oranda"
}, {
    "number": "15",
    "emote_id": "<:15f:1156919427875479552>",
    "name": "lion head"
}, {
    "number": "16",
    "emote_id": "<:16f:1156919431583248514>",
    "name": "ranchu"
}, {
    "number": "17",
    "emote_id": "<:17f:1156919433709768724>",
    "name": "black moor"
}, {
    "number": "18",
    "emote_id": "<:18f:1156919437388156999>",
    "name": "panda moor"
}, {
    "number": "19",
    "emote_id": "<:19f:1156919441184014386>",
    "name": "pearlscale"
}, {
    "number": "20",
    "emote_id": "<:20f:1156919444757545101>",
    "name": "crown pearlscale"
}, {
    "number": "21",
    "emote_id": "<:21f:1156919447475462215>",
    "name": "butterfly telescope"
}, {
    "number": "22",
    "emote_id": "<:22f:1156919451179036742>",
    "name": "egg"
}, {
    "number": "23",
    "emote_id": "<:23f:1156919454731616257>",
    "name": "blue phoenix"
}, {
    "number": "24",
    "emote_id": "<:24f:1156919456853934130>",
    "name": "tosakin"
}, {
    "number": "25",
    "emote_id": "<:25f:1156919460582670347>",
    "name": "tamasaba"
}, {
    "number": "26",
    "emote_id": "<:26f:1156919464093290516>",
    "name": "sukiyu"
}, {
    "number": "27",
    "emote_id": "<:27f:1156919466496638996>",
    "name": "bubble eye"
}, {
    "number": "28",
    "emote_id": "<:28f:1156919470024040518>",
    "name": "star gazer"
}]

fish_catchphrases = {
    "1":
    "{user.mention} successfully captured a **{fish_number}** goldfish! {emote_id}",
    "2":
    "Great job, {user.mention}! You reeled in a glimmering **{fish_number}** goldfish! {emote_id}",
    "3":
    "Woah~ Nice catch, {user.mention}! A **{fish_number}** goldfish in the net! {emote_id}",
    "4":
    "{user.mention}, you’ve got yourself a stunning **{fish_number}** goldfish! {emote_id}",
    "5":
    "Well done, {user.mention}. You’ve scooped a **{fish_number}** goldfish! {emote_id}",
    "6":
    "A shiny **{fish_number}** goldfish for {user.mention}! {emote_id}",
    "7":
    "Nice scoop, {user.mention}! You captured a **{fish_number}** goldfish~ {emote_id}",
    "8":
    "{user.mention} captured a **{fish_number}** goldfish! Keep scooping to complete your collection~ {emote_id}",
    "9":
    "{user.mention} is on fire! A dazzling **{fish_number}** goldfish in your scoop! {emote_id}",
    "10":
    "{user.mention} captured a **{fish_number}** goldfish. Keep scooping, you’re doing great! {emote_id}",
    "11":
    "Hey! {user.mention} snagged a beautiful **{fish_number}** goldfish~ {emote_id}",
    "12":
    "Lucky, {user.mention}! You’ve scooped a **{fish_number}** goldfish~ {emote_id}",
    "13":
    "Your skills are unmatched, {user.mention}! You successfully grabbed an **{fish_number}** goldfish. {emote_id}",
    "14":
    "You're making quite a splash, {user.mention}! You’ve scooped a **{fish_number}** goldfish. {emote_id}",
    "15":
    "Extraordinary {user.mention}! You've added a **{fish_number}** to your collection. {emote_id}",
    "16":
    "{user.mention} reeled in a sparkling **{fish_number}** goldfish! {emote_id}",
    "17":
    "{user.mention} mastered the art of the scoop and caught a **{fish_number}** goldfish! {emote_id}",
    "18":
    "You’re a pro at this, {user.mention}! You captured a **{fish_number}** goldfish. {emote_id}",
    "19":
    "Scoop-tastic! {user.mention} captured a gleaming **{fish_number}** goldfish! {emote_id}",
    "20":
    "Great job, {user.mention}! A **{fish_number}** goldfish joins your collection. {emote_id}",
    "21":
    "Fishy fortune favors you, {user.mention}! You captured a **{fish_number}** goldfish~ {emote_id}",
    "22":
    "What is it, {user.mention}? *gasp* It’s a **{fish_number}** goldfish! {emote_id}",
    "23":
    "Phew! That was a tough fight, {user.mention}. You captured a pretty **{fish_number}** goldfish! {emote_id}",
    "24":
    "Oh, look at that {user.mention}! You scooped a **{fish_number}** goldfish~ {emote_id}",
    "25":
    "You made it look easy, {user.mention}! You caught a **{fish_number}** goldfish! {emote_id}",
    "26":
    "Yay! {user.mention} successfully scooped a **{fish_number}** goldfish! {emote_id}",
    "27":
    "Nice catch, {user.mention}! You got a **{fish_number}** goldfish! {emote_id}",
    "28":
    "Fish-scooping master {user.mention}! You successfully scooped up a shiny **{fish_number}** goldfish! {emote_id}"
}

scoop_fail = [
    "Oh no! Your scooper came up empty. Try again!",
    "Talk about a fishy escape artist! No worries~ you can try again!",
    "Oops! You failed to catch one. :(", "\*Sigh\* What a shame… Try again!",
    "Fish got moves, huh? Better Luck next time!",
    "You almost caught a Star Gazer goldfish! But it escaped… :(",
    "Your scooping skills need refinement. You couldn’t even catch a common goldfish. :(",
    "\*Your scooper broke.\* Don’t give up! You’ll get the hang of it~",
    "Aw, so close! You nearly got it…",
    "Oh no! The pearlscale goldfish broke free! :("
]

riddle = {
    "1":
    "https://cdn.discordapp.com/attachments/1160145573039583232/1160146204194263111/RIDDLE_1.png?ex=65339959&is=65212459&hm=e6a1df44b9590b142f24d2be8f471afc2cfa10a54a486b0af629b28c2c7d9b5d&",
    "2":
    "https://cdn.discordapp.com/attachments/1160145573039583232/1160146338248392794/RIDDLE_2.png?ex=65339979&is=65212479&hm=34bc151e54bfaf92e15ebef26f3cc8d8b543b2856877d05afb8a1c848dc06d1a&",
    "3":
    "https://cdn.discordapp.com/attachments/1160145573039583232/1160146457563758662/RIDDLE_3.png?ex=65339995&is=65212495&hm=3e9f80d3c1f715d4a0ce4c2e93bfa542767efc0ccf4fc7f724eaa9298ccd83d6&",
    "4":
    "https://cdn.discordapp.com/attachments/1160145573039583232/1160146563260235786/RIDDLE_4.png?ex=653399af&is=652124af&hm=fbe23622b32cd2d6a218f1bc22ed1dd6439ef8cf43b151a18e651d75e353436c&",
    "5":
    "https://cdn.discordapp.com/attachments/1160145573039583232/1160146738980597760/RIDDLE_5.png?ex=653399d9&is=652124d9&hm=6ee8c5659daa1897129edb527364bd4dbe840fe9cc4627a6d641c47f6ea3efa3&",
    "6":
    "https://cdn.discordapp.com/attachments/1160145573039583232/1160146919373426688/RIDDLE_6.png?ex=65339a04&is=65212504&hm=2a33fda577a95190864fa319c35dbb1ff284ae40cf153f90df2c976de15ab15b&",
    "7":
    "https://cdn.discordapp.com/attachments/1160145573039583232/1160146999136493598/RIDDLE_7.png?ex=65339a17&is=65212517&hm=a5118c092cafb816b3297b5a3de0aa559460de79babe085222bd1f08b170b522&",
    "8":
    "https://cdn.discordapp.com/attachments/1160145573039583232/1160147065205166181/RIDDLE_8.png?ex=65339a26&is=65212526&hm=d1cf12c47f14e896a8c4cd50a81d697579ee7bfa8959237cf67bdbc66ece3771&",
    "9":
    "https://cdn.discordapp.com/attachments/1160145573039583232/1160147188597399682/RIDDLE_9.png?ex=65339a44&is=65212544&hm=510874e946c555773cb4f990c0468d476581e31a52f838545ba2354aedbc1776&",
    "10":
    "https://cdn.discordapp.com/attachments/1160145573039583232/1160147372832194630/RIDDLE_10.png?ex=65339a70&is=65212570&hm=9cd381769c91d48f516e4ab358bcd971160ce2380c908ad1e985cb1ff3bb5b15&",
    "11":
    "https://cdn.discordapp.com/attachments/1160145573039583232/1160147522594017360/RIDDLE_11.png?ex=65339a93&is=65212593&hm=c6103db232abb75ddc6753de3b35710799bd3f1be9b066267023b5cfdd46c8f3&",
    "12":
    "https://cdn.discordapp.com/attachments/1160145573039583232/1160147603653140610/RIDDLE_12.png?ex=65339aa7&is=652125a7&hm=ef37b544b64e8d95c638b742969167fa599307b7cece2b7e8b4d9789225a61c6&",
    "13":
    "https://cdn.discordapp.com/attachments/1160145573039583232/1160147669759574046/RIDDLE_13.png?ex=65339ab6&is=652125b6&hm=e1791a678cb8f9bb4eb1143352fbc0809a761d162dde9fc1467f47d65e31b76b&",
    "14":
    "https://cdn.discordapp.com/attachments/1160145573039583232/1160147726307168336/RIDDLE_14.png?ex=65339ac4&is=652125c4&hm=e2d31f6e3266ffa56f27ea10863237f182260cac7ca8fdc782462b088c4902e2&",
    "15":
    "https://cdn.discordapp.com/attachments/1160145573039583232/1160147789485973554/RIDDLE_15.png?ex=65339ad3&is=652125d3&hm=6da8657846d50d86342c7e36ef7f8ef6e6f7207e4388d2c3af8edf57c369f8de&",
}

food_menu = {
    "Yaki tomorokoshi": 15,
    "Yakitori": 15,
    "Ikayaki": 15,
    "Nikuman": 15,
    "Gyoza": 15,
    "Okonomiyaki": 20,
    "Yakisoba": 20,
    "Takoyaki": 20,
    "McConan": 25,
    "Taiyaki": 5,
    "Kibi dango": 5,
    "Ringo ame": 5,
    "Kakigori": 10,
    "Anmitsu": 15,
    "Crepes": 15,
    "Watame": 15,
    "Ice cream": 15,
    "Parfait": 20,
    "Water bottle": 5,
    "Soda": 10,
    "Juice": 10,
    "Boba milk tea": 15,
}

prize = [{
    "type":
    "embed",
    "title":
    "Chocolate Box",
    "description":
    "Congratulations on your win! You've earned a delectable **Chocolate Box**. May each sweet indulgence bring moments of delight and joy to your festival experience!",
    "image":
    "https://cdn.discordapp.com/attachments/1160198592695377920/1161615255009501227/images_8.jpg?ex=6538f182&is=65267c82&hm=c1135295ad5b7d71b6de89d7a3c9d07b09c1dbcbd402db366884267a7e5bae97&"
}, {
    "type":
    "embed",
    "title":
    "Naruto Headband",
    "description":
    "Congratulations! You've earned a **Naruto Headband** – a symbol of strength and determination. Wear it proudly and may it inspire you on your own ninja journey through the festival of life. Dattebayo!",
    "image":
    "https://cdn.discordapp.com/attachments/1160198592695377920/1161615540025053205/images_2.jpg?ex=6538f1c6&is=65267cc6&hm=ebd19defae52c6ac21bc35c5a9111ce98b201a34b8dbcbfde5478af8033dce1f&"
}, {
    "type":
    "embed",
    "title":
    "Pikachu Stuffed Toy",
    "description":
    "Omedetou! You've won a **Pikachu Stuffed Toy**. May this adorable little companion bring a spark of joy and electrifying happiness to your festivities!",
    "image":
    "https://cdn.discordapp.com/attachments/1160198592695377920/1161616549308796989/a-small-pikachu-stuffed-toy-being-given-to-someone-preview.jpg?ex=6538f2b7&is=65267db7&hm=191f59497a624a1c07c2f4e35a2315a0c3b8dfa9b26f857d75dfadb2d42d9f23&"
}, {
    "type":
    "embed",
    "title":
    "Death Note Notebook",
    "description":
    "You've won a **Death Note Notebook**! May it be a canvas for your creativity and a tribute to the intriguing world of anime. Enjoy jotting down your festival memories ~~(and the name of people you hate winks)~~ in this!",
    "image":
    "https://cdn.discordapp.com/attachments/1160198592695377920/1161618335272796170/images_3.jpg?ex=6538f460&is=65267f60&hm=874092200ff21ba8328d749771b5b1c2409671eb443df0c4d3b98f548d570089&"
}, {
    "type":
    "embed",
    "title":
    "Kaitou KID Key Ring",
    "description":
    "Bravo! You've won a **Kaito KID Key Ring**. May the elusive charm of Kaito KID accompany you, bringing a touch of magic and mystery in this festive adventure. Enjoy!",
    "image":
    "https://cdn.discordapp.com/attachments/1160198592695377920/1161619393567006761/images_4.jpg?ex=6538f55d&is=6526805d&hm=2e6c328829571ab4ec88b635e4e1148c9cf286f1989875632a3d8c9f6c6a7901&"
}, {
    "type":
    "embed",
    "title":
    "Tom And Jerry Frame",
    "description":
    "Congratulations on winning a **Tom and Jerry Frame**! May the timeless antics of these classic characters add laughter and joy to your festivities!\n**FUN FACT**: There chase has been going on for **83 years** now! ",
    "image":
    "https://cdn.discordapp.com/attachments/1160198592695377920/1161620293857579079/OIG_10.jpg?ex=6538f633&is=65268133&hm=a7aa75e605030f1d28d487734104a489996733be40039c19a195a824613c1861&"
}, {
    "type":
    "embed",
    "title":
    "Strawhat's Jolly Roger",
    "description":
    "Ahoy! You've won Strawhat's **Jolly Roger Flag** from One Piece. May it unfurl tales of adventure and camaraderie, adding a swashbuckling touch to your festival festivities. Enjoy your pirate-worthy prize!",
    "image":
    "https://cdn.discordapp.com/attachments/1160198592695377920/1161622354200363108/images_12.jpg?ex=6538f81f&is=6526831f&hm=88921da49dcbb538ff90c72c392765f7e0580288d5703a2cfce4f6a93285f195&"
}, {
    "type":
    "embed",
    "title":
    "Mouri Ran Figurine",
    "description":
    "Congratulations on winning **Mouri Ran's Figurine**! May this iconic character stand as a reminder of mystery, deduction, and festival fun! Enjoy~",
    "image":
    "https://cdn.discordapp.com/attachments/1160198592695377920/1161623526021812264/images_5.jpg?ex=6538f936&is=65268436&hm=f5fa2cf7daaeabc42e7f1186fbd88620bee891f2c62c0a270fde36cd6e202417&"
}, {
    "type":
    "embed",
    "title":
    "Raiden Ei Bookmark",
    "description":
    "Fantastic choice! You've won a **Raiden Ei Bookmark**. May the electro-archon herself infuse your reading adventures with electrifying energy and excitement. Enjoy your festival prize!",
    "image":
    "https://cdn.discordapp.com/attachments/1160198592695377920/1161625730631860274/images_6.jpg?ex=6538fb44&is=65268644&hm=5a65ea1cd8372e4e7c6b66b5a807efe9ade39fb724f52c21e7f2b6aa167b4a70&"
}, {
    "type":
    "embed",
    "title":
    "Conan Plushie",
    "description":
    "Brilliant win! You've earned a Conan Plushie! May the world of mystery and deduction snuggle into your heart with this adorable prize. Enjoy your plush companion!",
    "image":
    "https://cdn.discordapp.com/attachments/1160198592695377920/1161626623011999784/OIG_7.jpg?ex=6538fc18&is=65268718&hm=3b1264222530ca592a4423b2e0d68e0ac4ae7c0ebc21e57b78ec754c7edefa69&"
}]

food_prepare = {
    "Yaki tomorokoshi": [
        "https://media.giphy.com/media/EzmIfIX3MvPfTqnrQN/giphy.gif",
        "https://media.giphy.com/media/GfiH05aedRTEgyQ0wt/giphy.gif",
        "https://media.giphy.com/media/zdQG6Wz3Thprsx69MQ/giphy.gif"
    ],
    "Yakitori": [
        "https://media.giphy.com/media/EzmIfIX3MvPfTqnrQN/giphy.gif",
        "https://media.giphy.com/media/GfiH05aedRTEgyQ0wt/giphy.gif",
        "https://media.giphy.com/media/zdQG6Wz3Thprsx69MQ/giphy.gif"
    ],
    "Ikayaki": [
        "https://media.giphy.com/media/EzmIfIX3MvPfTqnrQN/giphy.gif",
        "https://media.giphy.com/media/GfiH05aedRTEgyQ0wt/giphy.gif",
        "https://media.giphy.com/media/zdQG6Wz3Thprsx69MQ/giphy.gif"
    ],
    "Nikuman": [
        "https://media.giphy.com/media/QXLbYGpK4AbahDmunj/giphy.gif",
        "https://media.giphy.com/media/YBEVES6knBTmk0QxjJ/giphy.gif"
    ],
    "Gyoza": [
        "https://media.giphy.com/media/QXLbYGpK4AbahDmunj/giphy.gif",
        "https://media.giphy.com/media/YBEVES6knBTmk0QxjJ/giphy.gif"
    ],
    "Okonomiyaki":
    "https://media.giphy.com/media/yrvrc3XdldASPLSyov/giphy.gif",
    "Yakisoba":
    "https://media.giphy.com/media/WOPJnASH5lagPfPgbD/giphy.gif",
    "Takoyaki":
    "https://media.giphy.com/media/SpBtkW83em19YDJTRy/giphy.gif",
    "McConan":
    "https://media.giphy.com/media/5sGm9lJoHhmNNV59eq/giphy.gif",
    "Taiyaki":
    "https://media.giphy.com/media/honvMhxliFmFD0z27q/giphy.gif",
    "Kibi dango":
    "https://media.giphy.com/media/9ATKNBXOZb9ghy3AWb/giphy.gif",
    "Ringo ame": [
        "https://media.giphy.com/media/hvzS7Lieqzv3q9E5b6/giphy.gif",
        "https://media.giphy.com/media/ZwNS0ajF3RISDjGR6M/giphy.gif",
    ],
    "Kakigori": [
        "https://media.giphy.com/media/oa49ZdbT5QQ3X0nbkM/giphy.gif",
        "https://media.giphy.com/media/VmDZDXDIGh6prvJzEH/giphy.gif",
    ],
    "Anmitsu": [
        "https://media.giphy.com/media/2HLxlVv7SNmbz0b12a/giphy.gif",
        "https://media.giphy.com/media/cZ6wY7wVp9ZwAHLrIy/giphy.gif",
        "https://media.giphy.com/media/vIDwdIm3MkxntHs7sH/giphy.gif",
    ],
    "Crepes":
    "https://media.giphy.com/media/cZ6wY7wVp9ZwAHLrIy/giphy.gif",
    "Watame":
    "https://media.giphy.com/media/8XM7hVMvOK1J08UWRh/giphy.gif",
    "Ice cream":
    "https://media.giphy.com/media/NxvWWAjWUqlnuvrk8P/giphy.gif",
    "Parfait": [
        "https://media.giphy.com/media/v8tqeruxgteqlVoWvg/giphy.gif",
        "https://media.giphy.com/media/cZ6wY7wVp9ZwAHLrIy/giphy.gif",
    ],
    "Water bottle":
    "https://media.giphy.com/media/Qkf7uJlajrvoGFh4gq/giphy.gif",
    "Soda": [
        "https://media.giphy.com/media/CVyXSL2WDoidaL80Jq/giphy.gif",
        "https://media.giphy.com/media/bPvU0ua5cCgYzBhkkS/giphy.gif",
    ],
    "Juice": [
        "https://media.giphy.com/media/1j4XvpXgQ4p3kHi47I/giphy.gif",
        "https://media.giphy.com/media/CVyXSL2WDoidaL80Jq/giphy.gif",
    ],
    "Boba milk tea": [
        "https://media.giphy.com/media/oG5WlLyg4B7rrN4huV/giphy.gif",
        "https://media.giphy.com/media/oknIDtfyLSDaTPw7aO/giphy.gif",
        "https://media.giphy.com/media/CVyXSL2WDoidaL80Jq/giphy.gif",
    ],
}

food_gifs = {
    "Nikuman":
    ["https://i.gifer.com/3ObxW.gif", "https://i.gifer.com/3ObxX.gif"],
    "Gyoza":
    ["https://i.gifer.com/3ObxY.gif", "https://i.gifer.com/3Obxa.gif"],
    "Yaki tomorokoshi":
    ["https://i.gifer.com/3ObxU.gif", "https://i.gifer.com/3ObxV.gif"],
    "Yakitori": [
        "https://i.gifer.com/3ObxR.gif", "https://i.gifer.com/3ObxS.gif",
        "https://i.gifer.com/3ObxT.gif"
    ],
    "Ikayaki":
    "https://i.gifer.com/3ObxQ.gif",
    "Okonomiyaki":
    ["https://i.gifer.com/3ObxL.gif", "https://i.gifer.com/3ObxM.gif"],
    "Yakisoba":
    ["https://i.gifer.com/3ObxJ.gif", "https://i.gifer.com/3ObxK.gif"],
    "Takoyaki": [
        "https://i.gifer.com/3ObxN.gif", "https://i.gifer.com/3ObxP.gif",
        "https://i.gifer.com/3ObxO.gif"
    ],
    "McConan": [
        "https://i.gifer.com/3Obxb.gif", "https://i.gifer.com/3Obxc.gif",
        "https://i.gifer.com/3Obxd.gif"
    ],
    "Taiyaki": [
        "https://i.gifer.com/3Obxe.gif", "https://i.gifer.com/3Oc0e.gif",
        "https://i.gifer.com/3Obzt.gif"
    ],
    "Kibi dango":
    ["https://i.gifer.com/3Obxf.gif", "https://i.gifer.com/3Obxg.gif"],
    "Ringo ame": [
        "https://i.gifer.com/3Obxh.gif", "https://i.gifer.com/3Obzq.gif",
        "https://i.gifer.com/3Obzs.gif"
    ],
    "Kakigori": [
        "https://i.gifer.com/3Obxl.gif", "https://i.gifer.com/3Obxm.gif",
        "https://i.gifer.com/3Obxn.gif", "https://i.gifer.com/3Obxp.gif"
    ],
    "Anmitsu":
    ["https://i.gifer.com/3Obxv.gif", "https://i.gifer.com/3Obxx.gif"],
    "Crepes": ["https://i.gifer.com/3Obxq.gif", "https/i.gifer.com/3Obxr.gif"],
    "Ice cream":
    ["https://i.gifer.com/50ff.gif", "https://i.gifer.com/3Obxu.gif"],
    "Parfait": [
        "https://i.gifer.com/3Obxz.gif", "https://i.gifer.com/3Oby0.gif",
        "https://i.gifer.com/3Oby1.gif", "https://i.gifer.com/3Oby2.gif"
    ],
    "Water bottle":
    ["https://i.gifer.com/3Oby6.gif", "https://i.gifer.com/3ObyB.gif"],
    "Soda": [
        "https://i.gifer.com/3Oby3.gif", "https://i.gifer.com/3Oby4.gif",
        "https://i.gifer.com/3Oc0c.gif"
    ],
    "Juice": [
        "https://i.gifer.com/3Oby5.gif", "https://i.gifer.com/3Oby7.gif",
        "https://i.gifer.com/3Oby8.gif"
    ],
    "Boba milk tea":
    "https://i.gifer.com/3ObyA.gif",
}

broke_message = [
    "Your balance is empty! Time to roll up your sleeves and earn some <:sakura:1159350038959505468> before you can place that order.",
    "Your pouch seems a little empty. It's time to hustle for some <:sakura:1159350038959505468> before you can order.",
    "Before you feast, let's pocket some <:sakura:1159350038959505468>. Work hard, play harder!"
]

shoot_message = [
    "Oof! Better luck next time~ <:dckidshrug:717035532634554368>",
    "So close! Try again~ <:dchanzawacry:743454350336196659>",
    "Almost there, keep trying! <:dcamurov:743454311551336460>",
    "Don't give up, you're getting close! <a:dcconanfunny:780643980681019452>",
    "You missed your target. RIP <:dcayumicry:743454339716087879>"
]

shoot_success = [
    "Great shot, user! It's a bullseye! <:target1:1155585593187762257>",
    "You've hit the mark, user. Amazing~ <:dcrumiowo:743454346691215360>",
    "Congratulations user! You nailed it~ <a:dcconanyay:728996021618868307>",
    "Well done, user! You're right on target. <:dcheijistrong:1026405346257944576>",
    "Excellent sharpshooter user! Impressive~ <a:dcaiclaps:723730589425074200>"
]

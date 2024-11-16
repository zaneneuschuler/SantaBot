import discord
import aiohttp
import io
import os
import db
import random
import shutil

from dotenv import load_dotenv

load_dotenv()


def testing_function(first, second):
    for i in range(len(first)):
        if first[i][0] == second[i][0]:
            return True
        else:
            pass
    return False


def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)


devs = (
    os.getenv("ADMIN_IDS").strip("][").split(", ")
)  # take devs from ADMIN_IDS in .env and convert to a list of dev ids

bot = discord.Bot()
# Guilds go into .env as a string split by spaces
bot_guild_ids = os.getenv("GUILD_IDS").split(" ")

#get db from .env
bot_db = os.getenv("DB")


# create Slash Command group with bot.create_group
# greetings = bot.create_group("greetings", "Greet people")


# @greetings.command(description="Hi there!")
# async def hello(ctx):
#     await ctx.respond(f"Hello, {ctx.author}!")


# @greetings.command(description="Bye there!")
# async def bye(ctx):
#     await ctx.respond(f"Bye, {ctx.author.id}!")


santa = bot.create_group("santa", "Secret santa things!")


@santa.command(description="Upload your skeleton!")
async def upload(
    ctx, file: discord.Attachment, stepartist: discord.SlashCommandOptionType.string
):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            file.url
        ) as resp:  # async grab file from discord's servers
            if resp.status != 200:
                return await ctx.send("Could not download file...")
            data = io.BytesIO(await resp.read())
            upload_ext = file.url.split(".")[-1].split("?")[0]  # grab extension
            print(upload_ext)

            f = open(f"uploads/{ctx.author.id}.{upload_ext}", "wb")
            f.write(data.getbuffer())  # write datastream to file and close
            f.close()
            await ctx.respond(
                "Your file has been submitted! Please await distribution time to see what presents you get! If you want to make changes to your file, feel free to reupload your file! :3",
                ephemeral=True,
            )
            db.put(ctx.author.id, stepartist, bot_db)
            # DB expects author ID and then stepartist name

@santa.command(description="Upload your finished file! (for future events)")
async def submitfinal(
    ctx, file: discord.Attachment
):
    if str(ctx.author.id) in os.getenv("ADMIN_IDS"):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                file.url
            ) as resp:  # async grab file from discord's servers
                if resp.status != 200:
                    return await ctx.send("Could not download file...")
                data = io.BytesIO(await resp.read())
                upload_ext = file.url.split(".")[-1].split("?")[0]  # grab extension

                f = open(f"finalpack/{ctx.author.id}.{upload_ext}", "wb")
                f.write(data.getbuffer())  # write datastream to file and close
                f.close()
                await ctx.respond(
                    "Your finished file has been submitted! Please wait for Christmas Day for the full pack release! If you want to make changes to your file, feel free to reupload your file before then! :3",
                    ephemeral=True,
                )
    else:
        ctx.respond("Sorry! For 2023, all files must be submitted directly to ATB. Maybe next year!", ephemeral=True)
# ideally i'd want some sort of system that checks if a santa event is ongoing so that upload and submitfinal can't be used outside of certain time periods, but that's probably for later

@santa.command(description="LET'S HECKING GOOOOOOOOOOOOOOOOOO")
async def hohoho(ctx):
    if str(ctx.author.id) in os.getenv("ADMIN_IDS"):  # TODO: also put this in .env
        await ctx.respond("Ho ho ho! Be prepared to get your files...", ephemeral=True)
        stepartists = db.get(bot_db)
        stepartists_randomized = random.sample(stepartists, len(stepartists))
        shuffled = testing_function(stepartists, stepartists_randomized)
        while shuffled:
            print("Need to reshuffle!")  # cursed. will literally not scale well at all.
            random.shuffle(stepartists_randomized)
            shuffled = testing_function(stepartists, stepartists_randomized)
        message_to_send = ""
        for i in range(len(stepartists)):
            santa = stepartists[i][0]    
            lucky_boy_or_girl = stepartists_randomized[i][0]
            message_to_send += f"Stepartist {stepartists[i][1]} will get {stepartists_randomized[i][1]}'s file!\n"
            new_file = shutil.copyfile(
                f"uploads/{lucky_boy_or_girl}.zip",
                f"uploads/{stepartists[i][1]}present.zip",
            )  # shouldn't hardcode in/out extensions, but fixable.
            user = await bot.fetch_user(santa)
            try:
                await user.send(
                    f"Here is your file! If you have any questions/concerns, feel free to message <@{devs[0]}>, and make sure to submit your file when you're done to him as well!  Ho ho ho!",
                    file=discord.File(new_file),
                )#In memory of devs[2]. Good job Zane.
                os.remove(new_file)
            except Exception as error:
               print("Oh no! That's not good! Here's the error:", error)
               await ctx.respond(
                    f"Could not send file to {stepartists[i][1]}! File has been saved, please manually DM them!",
                    ephemeral=True,
                )

        print(message_to_send)
    else:
        await ctx.respond(
            "Oops! You're not allowed to use this command!", ephemeral=True
        )


@santa.command(description="For internal testing purposes")
async def testing(ctx):
    if str(ctx.author.id) in os.getenv("ADMIN_IDS"):
        stepartists = db.get(bot_db)
        message = "Stepartists currently signed up: \n"
        for i in range(len(stepartists)):
            current = stepartists[i][0]
            message = message + f'<@{current}> \n'
        await ctx.respond(message, ephemeral=True)
    else:
        await ctx.respond("https://cdn.cloudflare.steamstatic.com/steamcommunity/public/images/apps/1421490/5a9ac5aa850e5638527ab0fae7c4983f63f9c3e6.jpg", ephemeral=True)

@santa.command(description="For internal testing purposes")
async def wipe(ctx):
    if str(ctx.author.id) in os.getenv("ADMIN_IDS"):
        db.wipe(bot_db)
        await ctx.respond(f"Database has been wiped! Make sure to doublecheck {bot_db} to make sure though!", ephemeral=True)
    else:
        await ctx.respond("https://cdn.cloudflare.steamstatic.com/steamcommunity/public/images/apps/1421490/5a9ac5aa850e5638527ab0fae7c4983f63f9c3e6.jpg", ephemeral=True)


@santa.command(description="For internal testing purposes")
async def manualadd(ctx, stepartist: discord.SlashCommandOptionType.string, discord_id: discord.SlashCommandOptionType.string):
    if str(ctx.author.id) in os.getenv("ADMIN_IDS"):
        db.put(discord_id, stepartist, bot_db) #Hey, this is really unsafe since the command accepts a string for the discord ID, meaning that theoretically a sql injection could happen.
        #But I mean, hopefully none of the devs want to do something like that, right?
        await ctx.respond("did thing", ephemeral=True)
    else:
        await ctx.respond("https://cdn.cloudflare.steamstatic.com/steamcommunity/public/images/apps/1421490/5a9ac5aa850e5638527ab0fae7c4983f63f9c3e6.jpg", ephemeral=True)


@santa.command(description="How does this bot work?")
async def help(ctx):
    if str(ctx.author.id) in os.getenv("ADMIN_IDS"): 
        embed = discord.Embed(
            title="Read me!",
            description="Hi there! Starting Secret Stepfile Santa 2023, we are proud to introduce to you ***SantaBot***! **SantaBot** has been made in order to make the entire Secret Santa Process generally be a lot more streamlined than in the past, and hopefully can be used for many years in the future!",
            colour=0xF50000,
        )

        embed.set_author(
            name="SantaBot", icon_url="https://zaneis.moe/ss/2023-10-03_14-27_16638.png"
        )

        embed.add_field(
            name="So what does this mean?",
            value="Starting 2023, **SantaBot** will be the main way to submit and receive files! This might seem a little scary, but we have a handy guide for you to help you through the new Secret Santa experience!",
            inline=False,
        )
        embed.add_field(
            name="Step 0: Preparation",
            value="Once <@262440960040894474> announces that submissions are open, make sure to have your file in a *.zip* folder! This will make it much easier for us to handle. Along with this, ***please*** have DMs from server members open! If you do not do this, we will be unable to automatically send you your gifts!",
            inline=True,
        )
        embed.add_field(
            name="Step 1: Submission",
            value="Once you have your file(s) prepared, type in `/santa upload` in your discord messaging bar! This will open a prompt for you to upload your file, and your stepartist name! Then all you have to do is submit it, and that's it! It will be recieved by SantaBot immediately (as soon as it uploads). See the below image for a handy guide!",
            inline=True,
        )
        embed.add_field(
            name="Step 2: Receiving your file",
            value="Once the distribution day comes, <@262440960040894474> or <@84108714671345664> will pull the magic lever (okay it's another command), and the bot will automatically choose your partner, and give you their files! The *entire* distribution process has been automated!",
            inline=True,
        )
        embed.add_field(
            name="Step 3: Submitting your final files",
            value="Unfortunately, at this time **SantaBot** ~~is not able to accept your final submissions~~ won't be used for recieving final files, so that will still be handled by sending your file to <@262440960040894474>, however in the future we can try to automate that and the pack creation process as well!",
            inline=True,
        )
        embed.add_field(
            name="Still have questions?",
            value="Please mention <@84108714671345664>, and he will try to answer your questions to the best of his ability!",
            inline=False,
        )

        embed.set_image(
            url="https://zaneis.moe/ss/2023-10-30_15-30_16844.png"
        )

        embed.set_footer(
            text="Built by zaniel & Sorae for Secret Stepfile Santa!",
            icon_url="https://zaneis.moe/ss/2023-10-03_14-27_16638.png",
        )

        await ctx.send(embed=embed)
        await ctx.respond("Info message sent!", ephemeral=True)
    else:
        await ctx.respond(
            "Oops! You're not allowed to use this command!", ephemeral=True
        )


bot.run(os.getenv("CLIENT_TOKEN"))

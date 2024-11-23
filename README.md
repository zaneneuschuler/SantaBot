# SantaBot: A single purpose Secret Santa discord bot.
## TODO: Documentation for project

Quick and dirty How To Run:

> [!CAUTION]
> Having venv set up is probably recommended, considering that this project uses py-cord and not discord.py. Also use this code at your own risk.

1. Download the repository to your computer locally.
2. Create a venv for the project.
3. Do `pip install -r requirements.txt` to install all of the requirements neccessary.
4. Create a `.env` file and fill it with the following information:
```
CLIENT_TOKEN=YOURTOKENHERE
GUILD_IDS="[YOUR,GUILD,IDS,HERE]"
ADMIN_IDS="[YOUR,ADMIN,IDS,HERE]"
DB="yourdb.db"
DBX_TOKEN="YOUR_DBX_APP_TOKEN"
```
5. Run `python bot.py`.
6. ????
7. You have SantaBot up and running! Hopefully.

If you intend to use or work on Dropbox link downloading, you need to create a new app to get your access token.
1. Go to [this page](https://www.dropbox.com/developers/apps/create?_tk=pilot_lp&_ad=ctabtn1&_camp=create) to set up a new app on Dropbox.
2. Select Scoped access -> Full Dropbox and give your app a name, then click `Create app`.
3. On the app's dashboard, under the Settings tab, generate an access token under `Generated access token` and put that in the .env.
4. Go to the Permissions tab and set the `sharing.read` permission to on.
Sorry lol

> [!WARNING]
> This code is provided as-is. If you need help running the bot, please open an issue as that will be the fastest way for me to see it.
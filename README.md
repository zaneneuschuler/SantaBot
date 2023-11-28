# SantaBot: A single purpose Secret Santa discord bot.
## TODO: Documentation for project

## Development

This project uses [Poetry](https://python-poetry.org) for dependency management.
The project is known to work with Python 3.11.5 and Poetry 1.6.1.
Using older versions of Poetry and Python may lead to command failures with unintuitive error messages.

To run it locally:
1. Follow [Discord's instructions](https://discord.com/developers/docs/getting-started) for setting up an app to use for testing. Write a `.env` file into your project's root with the following format:
  ```
  CLIENT_TOKEN="client token here"
  GUILD_IDS="[guild, ids, here]"
  ADMIN_IDS="[admin, ids, here]"
  ```
1. Install project dependencies. (You may need to [install Poetry](https://python-poetry.org/docs/#installing-with-the-official-installer) first.)
  ```
  $ poetry install
  ```
1. Run the project.
  ```
  $ poetry run python ./bot.py
  ```

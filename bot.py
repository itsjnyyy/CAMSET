import os
import string
import difflib
import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup

# --- Config ---
DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
LIQUIPEDIA_URL = "https://liquipedia.net/rocketleague/List_of_player_camera_settings"
HEADERS = {
    "User-Agent": "CAMSET-Bot/2.0 (Discord bot for Rocket League camera settings lookup)"
}

# --- Bot setup ---
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# --- Scraper ---
def fetch_camera_settings():
    """Scrape all player camera settings from Liquipedia."""
    response = requests.get(LIQUIPEDIA_URL, headers=HEADERS, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")

    players = {}

    # The page may have multiple tables (one per region/tier)
    tables = soup.find_all("table", class_="wikitable")
    if not tables:
        tables = soup.find_all("table", class_="sortable")

    for table in tables:
        rows = table.find_all("tr")[1:]  # skip header
        for row in rows:
            cols = row.find_all("td")
            if len(cols) < 8:
                continue
            try:
                name_raw = cols[0].get_text(strip=True)
                name_key = name_raw.translate(str.maketrans("", "", string.punctuation)).lower()

                players[name_key] = {
                    "name": name_raw,
                    "org": cols[1].get_text(strip=True) if len(cols) > 1 else "N/A",
                    "fov": cols[3].get_text(strip=True) if len(cols) > 3 else "N/A",
                    "distance": cols[4].get_text(strip=True) if len(cols) > 4 else "N/A",
                    "height": cols[5].get_text(strip=True) if len(cols) > 5 else "N/A",
                    "angle": cols[6].get_text(strip=True) if len(cols) > 6 else "N/A",
                    "stiffness": cols[7].get_text(strip=True) if len(cols) > 7 else "N/A",
                    "swivel": cols[8].get_text(strip=True) if len(cols) > 8 else "N/A",
                    "transition": cols[9].get_text(strip=True) if len(cols) > 9 else "N/A",
                }
            except (IndexError, AttributeError):
                continue

    return players


def build_embed(player: dict, is_closest: bool = False) -> discord.Embed:
    """Build a Discord embed for a player's camera settings."""
    title = f"📷 {player['name']}"
    if is_closest:
        title = f"📷 Closest match: {player['name']}"

    embed = discord.Embed(title=title, color=0x00bfff)
    if player["org"]:
        embed.set_author(name=player["org"])

    embed.add_field(name="Field of View", value=player["fov"], inline=True)
    embed.add_field(name="Distance", value=player["distance"], inline=True)
    embed.add_field(name="Height", value=player["height"], inline=True)
    embed.add_field(name="Angle", value=player["angle"], inline=True)
    embed.add_field(name="Stiffness", value=player["stiffness"], inline=True)
    embed.add_field(name="Swivel Speed", value=player["swivel"], inline=True)
    embed.add_field(name="Transition Speed", value=player["transition"], inline=True)
    embed.set_footer(text="Source: Liquipedia • /camset <player>")

    return embed


# --- Slash command ---
@bot.tree.command(name="camset", description="Look up a Rocket League pro player's camera settings")
@discord.app_commands.describe(player="The player's name (e.g. jstn, Jstn, JSTN)")
async def camset(interaction: discord.Interaction, player: str):
    await interaction.response.defer()

    try:
        players = fetch_camera_settings()
    except Exception as e:
        await interaction.followup.send(f"❌ Failed to fetch data from Liquipedia: `{e}`")
        return

    if not players:
        await interaction.followup.send("❌ No player data found. Liquipedia's table format may have changed.")
        return

    # Normalize input
    query = player.translate(str.maketrans("", "", string.punctuation)).lower()

    # Exact match
    if query in players:
        embed = build_embed(players[query])
        await interaction.followup.send(embed=embed)
        return

    # Fuzzy match
    closest = difflib.get_close_matches(query, players.keys(), n=1, cutoff=0.6)
    if closest:
        embed = build_embed(players[closest[0]], is_closest=True)
        await interaction.followup.send(embed=embed)
    else:
        await interaction.followup.send(
            f"❌ Player **{player}** not found and no close match either.\n"
            f"Check the full list: <{LIQUIPEDIA_URL}>"
        )


STARTUP_CHANNEL_ID = 1276988782872367217
STARTUP_MESSAGE_SENT = False

# --- On ready ---
@bot.event
async def on_ready():
    global STARTUP_MESSAGE_SENT
    await bot.tree.sync()
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="Rocket League pro cam settings | /camset"
        )
    )
    if not STARTUP_MESSAGE_SENT:
        channel = await bot.fetch_channel(STARTUP_CHANNEL_ID)
        if channel:
            await channel.send(
                "👋 **Hey! I'm CAMSET** — your Rocket League pro camera settings lookup bot.\n\n"
                "📷 **What I do:**\n"
                "I pull real-time camera settings for any Rocket League pro player directly from Liquipedia, "
                "so you can instantly copy the exact setup your favourite player uses.\n\n"
                "**Settings I return:** FOV · Distance · Height · Angle · Stiffness · Swivel Speed · Transition Speed\n\n"
                "**How to use me:**\n"
                "```/camset <player name>```\n"
                "**Examples:**\n"
                "```/camset jstn\n/camset Yukeo\n/camset Garrett G```\n"
                "> 💡 Don't worry about exact spelling — fuzzy search handles typos and partial names!"
            )
        STARTUP_MESSAGE_SENT = True
    print(f"✅ Logged in as {bot.user} | /camset command ready")


bot.run(DISCORD_TOKEN)

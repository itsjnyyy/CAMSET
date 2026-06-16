# CAMSET Bot 🎮

> ✅ **Status: Live and deployed on Railway**

A Discord bot that looks up **Rocket League pro player camera settings** in real time from [Liquipedia](https://liquipedia.net/rocketleague/List_of_player_camera_settings).

## Features

- 📷 Live camera settings fetched from Liquipedia on every request — always up to date
- 🔍 Fuzzy name matching handles typos and partial names
- 📊 Returns FOV, Distance, Height, Angle, Stiffness, Swivel Speed, and Transition Speed
- 💬 Rich embed responses with player org info
- 🟢 Rich presence status: **Watching Rocket League pro cam settings | /camset**
- 📣 Posts a welcome/instructions message to a designated channel on startup
- No database required — fully stateless and lightweight

## Usage

```
/camset jstn
/camset Yukeo
/camset garrett g
```

Returns a formatted embed with the player's full camera config. If the name isn't an exact match, the bot suggests the closest player found.

---

## Deployment

This bot is hosted on [Railway](https://railway.app) and deploys automatically.

### Environment Variables

| Variable | Description |
|---|---|
| `DISCORD_TOKEN` | Your Discord bot token from the Developer Portal |

### Running Locally

```bash
pip install -r requirements.txt
DISCORD_TOKEN=your_token_here python bot.py
```

### Deploying to Railway

1. Push this repo to GitHub
2. Go to [railway.app](https://railway.app) → **New Project → Deploy from GitHub**
3. Select this repo
4. Add the `DISCORD_TOKEN` variable under **Variables**
5. Railway will build and deploy automatically

---

## Bot Setup (Discord Developer Portal)

1. Go to [discord.com/developers/applications](https://discord.com/developers/applications) → **New Application**
2. Go to **Bot** → **Add Bot** → copy the token
3. Under **OAuth2 → URL Generator**: check `bot` + `applications.commands`, then `Send Messages` + `Use Slash Commands`
4. Open the generated URL to invite the bot to your server

---

## Configuration

To change which channel the bot posts its startup message to, update `STARTUP_CHANNEL_ID` in `bot.py`:

```python
STARTUP_CHANNEL_ID = your_channel_id_here
```

---

## Requirements

- Python 3.10+
- `discord.py >= 2.3.0`
- `requests >= 2.31.0`
- `beautifulsoup4 >= 4.12.0`

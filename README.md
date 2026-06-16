# CAMSET Bot 🎮

> ✅ **Status: Live and working**

A Discord bot that looks up **Rocket League pro player camera settings** in real time from [Liquipedia](https://liquipedia.net/rocketleague/List_of_player_camera_settings).

## Usage

```
/camset jstn
/camset Yukeo
/camset garrett g
```

Returns an embed with the player's full camera config — FOV, Distance, Height, Angle, Stiffness, Swivel Speed, and Transition Speed. If the name isn't an exact match, it suggests the closest player found.

---

## Deployment (Railway)

### 1. Create the bot

1. Go to [discord.com/developers/applications](https://discord.com/developers/applications) → **New Application**
2. Go to **Bot** → **Add Bot** → copy the token
3. Under **OAuth2 → URL Generator**: check `bot` + `applications.commands`, then `Send Messages` + `Use Slash Commands`
4. Open the generated URL to invite the bot to your server

### 2. Deploy to Railway

1. Push this repo to GitHub
2. Go to [railway.app](https://railway.app) → **New Project → Deploy from GitHub**
3. Select this repo
4. Go to **Variables** and add:

| Variable | Value |
|---|---|
| `DISCORD_TOKEN` | Your bot token from the Developer Portal |

5. Railway will deploy automatically. Check logs for `✅ Logged in as ...`

---

## Requirements

- Python 3.10+
- `discord.py`, `requests`, `beautifulsoup4` (see `requirements.txt`)

---

## Notes

- Camera settings are fetched live from Liquipedia on every `/camset` command
- Fuzzy name matching handles typos and partial names
- No database needed — stateless and lightweight

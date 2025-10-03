# Discord Instagram Bot

A feature-rich Discord bot that automatically posts Instagram reels and posts to a designated channel with beautiful embeds and random promotional messages.

## Features

✨ **Multiple Input Methods**
- 📱 Clean UI with button interface
- 💬 Command-based posting (`!reel <link>`)
- 🤖 Auto-detection in DMs (just paste the link!)

🎨 **Beautiful Embeds**
- Instagram thumbnails automatically fetched
- Random promotional messages (50+ variations)
- Color-coded Instagram branding
- Auto-detects if it's a Reel, Post, or Video

🛡️ **Smart Features**
- Duplicate link prevention
- Persistent link history tracking
- Admin commands for management
- Error handling and user feedback

## Installation

### 1. Prerequisites
- Python 3.8 or higher
- A Discord bot token ([Create one here](https://discord.com/developers/applications))

### 2. Install Dependencies

```bash
pip install discord.py requests
```

### 3. Configure the Bot

Open `bot.py` and edit these lines at the top:

```python
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # Replace with your Discord bot token
TARGET_CHANNEL_ID = 1234567890  # Replace with your target channel ID
```

#### How to get your Bot Token:
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application or select an existing one
3. Go to the "Bot" section
4. Click "Reset Token" and copy your token
5. **Important:** Enable "Message Content Intent" in the Bot settings!

#### How to get Channel ID:
1. Enable Developer Mode in Discord (User Settings > Advanced > Developer Mode)
2. Right-click on the channel where you want posts to appear
3. Click "Copy ID"

### 4. Invite the Bot to Your Server

Use this URL (replace `YOUR_CLIENT_ID` with your application's client ID):
```
https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=274878024768&scope=bot
```

Required Permissions:
- Read Messages/View Channels
- Send Messages
- Embed Links
- Attach Files
- Read Message History

## Usage

### Method 1: UI Panel (Recommended)
1. In any channel, type: `!panel`
2. Click the "📸 Post Instagram Content" button
3. Paste your Instagram URL in the modal
4. Click Submit!

### Method 2: Command
```
!reel https://www.instagram.com/reel/xxxxxx/
```

### Method 3: DM (Auto-detect)
Simply send an Instagram link directly to the bot via DM, and it will automatically process it!

## Commands

| Command | Description | Permission |
|---------|-------------|------------|
| `!panel` | Shows the UI posting panel | Everyone |
| `!reel <url>` | Posts an Instagram link | Everyone |
| `!clearhistory` | Clears posted links history | Admin Only |

## Running the Bot

```bash
python bot.py
```

You should see:
```
✅ Bot is ready! Logged in as YourBot#1234
📡 Bot ID: 123456789
🎯 Target Channel ID: 987654321
📝 Loaded 0 previously posted links
==================================================
```

## Example Output

When you post an Instagram link, the bot will create an embed like this:

```
🎥 Watch my new reel!

[Instagram Reel Embed]
┌─────────────────────────────┐
│  Instagram Reel             │
│  🚀 Just dropped something  │
│     fresh!                  │
│                             │
│  [Thumbnail Image]          │
│                             │
│  🔗 instagram.com/reel/xxx  │
└─────────────────────────────┘
Posted via Instagram Bot
```

Each post includes:
- A randomly selected promotional message from 50+ options
- The Instagram thumbnail image
- The post type (Reel, Post, or Video)
- A clickable link to the Instagram content

## File Structure

```
discord bot/
├── bot.py                    # Main bot file
├── posted_links.json         # Auto-generated: tracks posted links
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Troubleshooting

### Bot doesn't respond to commands
- Make sure "Message Content Intent" is enabled in Discord Developer Portal
- Check that the bot has proper permissions in your server

### "Target channel not found" error
- Verify the `TARGET_CHANNEL_ID` is correct
- Make sure the bot has access to that channel

### Thumbnail not loading
- Instagram may block scraping attempts
- The bot will fall back to the Instagram logo icon
- For better thumbnail fetching, consider using Instagram's official API

### Bot goes offline
- Check your token is valid
- Ensure your internet connection is stable
- Check the console for error messages

## Advanced Configuration

### Customizing Promotional Messages

Edit the `PROMO_MESSAGES` list in `bot.py`:

```python
PROMO_MESSAGES = [
    "🎥 Your custom message here!",
    "✨ Another cool message!",
    # Add as many as you want!
]
```

### Changing Embed Colors

Find this line in `bot.py`:
```python
color=discord.Color.from_rgb(225, 48, 108),  # Instagram pink
```

Change to any RGB color you prefer!

## Security Notes

⚠️ **Never share your bot token publicly!**
- Don't commit it to GitHub
- Don't share screenshots containing it
- If leaked, reset it immediately in the Developer Portal

## Support

If you encounter issues:
1. Check that all dependencies are installed
2. Verify your bot token and channel ID are correct
3. Make sure Message Content Intent is enabled
4. Check the console for error messages

## License

This bot is provided as-is for personal use. Feel free to modify and customize it to your needs!

## Credits

Built with:
- [discord.py](https://github.com/Rapptz/discord.py) - Discord API wrapper
- Python 3

---

**Enjoy your Instagram posting bot! 🎉**

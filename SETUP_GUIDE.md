# Configuration Guide for Discord Instagram Bot

## Quick Setup Checklist

- [ ] Install Python 3.8+
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Create Discord bot and get token
- [ ] Enable Message Content Intent
- [ ] Get your target channel ID
- [ ] Edit bot.py with your token and channel ID
- [ ] Invite bot to your server
- [ ] Run the bot!

## Step-by-Step Configuration

### 1. Create a Discord Bot

1. Go to https://discord.com/developers/applications
2. Click "New Application"
3. Give it a name (e.g., "Instagram Poster")
4. Go to the "Bot" tab on the left
5. Click "Add Bot"
6. Under "Privileged Gateway Intents", enable:
   - ✅ **MESSAGE CONTENT INTENT** (Required!)
   - ✅ Presence Intent (Optional)
   - ✅ Server Members Intent (Optional)

### 2. Get Your Bot Token

1. In the Bot tab, click "Reset Token"
2. Copy the token (you'll only see it once!)
3. Open `bot.py` and replace this line:
   ```python
   BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
   ```
   with:
   ```python
   BOT_TOKEN = "your_actual_token_here"
   ```

### 3. Get Your Channel ID

1. Open Discord
2. Go to User Settings > Advanced
3. Enable "Developer Mode"
4. Right-click the channel where you want posts to appear
5. Click "Copy ID"
6. In `bot.py`, replace:
   ```python
   TARGET_CHANNEL_ID = 1234567890
   ```
   with:
   ```python
   TARGET_CHANNEL_ID = your_channel_id_here
   ```

### 4. Invite Bot to Your Server

1. Go back to Discord Developer Portal
2. Click on "OAuth2" > "URL Generator"
3. Select scopes:
   - ✅ bot
4. Select bot permissions:
   - ✅ Read Messages/View Channels
   - ✅ Send Messages
   - ✅ Embed Links
   - ✅ Attach Files
   - ✅ Read Message History
5. Copy the generated URL
6. Open it in your browser
7. Select your server and authorize

**OR** use this quick URL (replace YOUR_CLIENT_ID):
```
https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=274878024768&scope=bot
```

Your Client ID is found in the "General Information" tab of your application.

### 5. Install Dependencies

Open terminal in the bot directory and run:

```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install discord.py requests
```

### 6. Run the Bot

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

## Testing Your Bot

### Test 1: UI Panel
1. In any channel, type: `!panel`
2. You should see a nice embed with a button
3. Click "📸 Post Instagram Content"
4. A modal should pop up
5. Paste an Instagram link and submit

### Test 2: Command
1. Type: `!reel https://www.instagram.com/reel/C_example/`
2. The bot should process and post to your target channel

### Test 3: DM Auto-detect
1. Send a DM to your bot
2. Just paste an Instagram link (no command needed)
3. The bot should automatically process it

## Common Issues

### "Message Content Intent is not enabled"
- Go to Discord Developer Portal > Your Bot > Bot tab
- Scroll down to "Privileged Gateway Intents"
- Enable "Message Content Intent"
- Restart your bot

### "Target channel not found"
- Double-check your channel ID is correct
- Make sure the bot has access to that channel
- Verify the bot is in the same server as the channel

### "Invalid Token"
- Your token may have expired or been regenerated
- Get a new token from the Developer Portal
- Update bot.py with the new token

### Bot doesn't respond to commands
- Check that the bot is online (green status)
- Verify Message Content Intent is enabled
- Make sure the bot has "Send Messages" permission

### Thumbnail doesn't load
- Instagram may block automated requests
- The bot falls back to Instagram's logo
- This is normal behavior - the embed will still work!

## Security Best Practices

1. **Never share your bot token**
   - Don't commit it to Git
   - Don't share screenshots with it
   - Use environment variables in production

2. **Use environment variables (Advanced)**
   ```python
   import os
   BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
   TARGET_CHANNEL_ID = int(os.getenv('TARGET_CHANNEL_ID'))
   ```

3. **Keep your bot updated**
   ```bash
   pip install --upgrade discord.py requests
   ```

## Optional Enhancements

### Using Environment Variables

Create a `.env` file:
```
DISCORD_BOT_TOKEN=your_token_here
TARGET_CHANNEL_ID=your_channel_id_here
```

Install python-dotenv:
```bash
pip install python-dotenv
```

Update bot.py:
```python
from dotenv import load_dotenv
import os

load_dotenv()
BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
TARGET_CHANNEL_ID = int(os.getenv('TARGET_CHANNEL_ID'))
```

### Running as a Background Service (Windows)

Create `start_bot.bat`:
```batch
@echo off
python bot.py
pause
```

Double-click to run!

### Running as a Background Service (Linux)

Create a systemd service file: `/etc/systemd/system/instagram-bot.service`
```ini
[Unit]
Description=Instagram Discord Bot
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/discord bot
ExecStart=/usr/bin/python3 bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable instagram-bot
sudo systemctl start instagram-bot
```

## Need Help?

Check the README.md for more information and troubleshooting tips!

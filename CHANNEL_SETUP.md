# 📺 Channel Setup Guide

## 🎯 How the Bot Works with Channels

Your bot now supports **TWO separate channels**:

### 1. **Control Channel** 🎮
- Where YOU send commands and Instagram links
- Where the UI panel appears
- Can be a private channel just for admins
- **OR** you can use DMs with the bot

### 2. **Target Channel** 📸
- Where the bot POSTS the Instagram content
- Public channel where your community sees the posts
- Beautiful embeds with thumbnails appear here

---

## ⚙️ Configuration Options

### **Option A: Use Any Channel (Default)**
If you DON'T set `CONTROL_CHANNEL_ID`, you can use commands from:
- ✅ Any channel in your server
- ✅ DMs with the bot

Posts will still go to the TARGET_CHANNEL_ID

### **Option B: Use a Specific Control Channel (Recommended)**
Set `CONTROL_CHANNEL_ID` to restrict commands to one channel:
- ✅ Only that channel can use bot commands
- ✅ DMs with the bot still work
- ✅ Keeps your server clean - commands in one place, posts in another

---

## 📋 How to Set Up Two Separate Channels

### Step 1: Get Channel IDs

1. **Enable Developer Mode** in Discord:
   - Settings → Advanced → Developer Mode ON

2. **Get Control Channel ID** (where you'll use commands):
   - Right-click on your control channel (e.g., `#instagram-control`)
   - Click "Copy ID"
   - Example: `1234567890123456789`

3. **Get Target Channel ID** (where posts appear):
   - Right-click on your target channel (e.g., `#instagram-feed`)
   - Click "Copy ID"
   - Example: `1334165445271617546`

### Step 2: Set Environment Variables

#### **In Railway.app:**

1. Go to your project
2. Click **"Variables"** tab
3. Update/Add these variables:

   **Variable 1: Target Channel** (required)
   ```
   TARGET_CHANNEL_ID = 1334165445271617546
   ```
   *(Where Instagram posts will appear)*

   **Variable 2: Control Channel** (optional)
   ```
   CONTROL_CHANNEL_ID = 1234567890123456789
   ```
   *(Where you can use commands - leave empty to allow any channel)*

4. Click **"Save"** or **"Deploy"**

#### **Running Locally:**

In PowerShell:
```powershell
$env:BOT_TOKEN="your_token_here"
$env:TARGET_CHANNEL_ID="1334165445271617546"
$env:CONTROL_CHANNEL_ID="1234567890123456789"
python bot.py
```

---

## 🎬 Example Setup

### **Scenario 1: Private Control, Public Posts**

```
#instagram-control (Private - Admin only)
└── You type: !panel
└── You click button and paste Instagram link
└── ✅ Bot confirms: "Successfully posted!"

#instagram-feed (Public - Everyone can see)
└── 🎥 Watch my new reel!
└── [Beautiful Instagram embed appears]
└── Your community sees and engages!
```

**Environment Variables:**
```
TARGET_CHANNEL_ID = 9999999999999  # #instagram-feed
CONTROL_CHANNEL_ID = 8888888888888  # #instagram-control
```

### **Scenario 2: Use DMs, Post Publicly**

```
DM with Bot
└── You paste: https://www.instagram.com/reel/xxxxx/
└── ✅ Bot confirms: "Successfully posted!"

#social-media (Public)
└── 🚀 Just dropped something fresh!
└── [Beautiful Instagram embed appears]
```

**Environment Variables:**
```
TARGET_CHANNEL_ID = 9999999999999  # #social-media
CONTROL_CHANNEL_ID = 0  # Allow any channel/DM
```

---

## 🧪 Testing Your Setup

### Test 1: Control Channel
1. Go to your control channel
2. Type: `!panel`
3. ✅ Should see the UI panel

### Test 2: Wrong Channel (if CONTROL_CHANNEL_ID is set)
1. Go to a different channel
2. Type: `!panel`
3. ✅ Should see: "Please use this command in #instagram-control or DM me!"

### Test 3: Post to Target Channel
1. Use `!reel <instagram_link>` in control channel
2. ✅ Post should appear in TARGET_CHANNEL_ID
3. ✅ Confirmation appears in control channel

### Test 4: DM Always Works
1. DM the bot with an Instagram link
2. ✅ Should work regardless of CONTROL_CHANNEL_ID setting
3. ✅ Post appears in TARGET_CHANNEL_ID

---

## 🎯 Recommended Channel Setup

### For Clean Server Organization:

1. **#instagram-control** (Private)
   - Permissions: Admin/Moderator only
   - Purpose: Send commands, use UI panel
   - Set as: `CONTROL_CHANNEL_ID`

2. **#instagram-feed** (Public)
   - Permissions: Everyone can view
   - Purpose: Display Instagram posts
   - Set as: `TARGET_CHANNEL_ID`

This keeps your server organized:
- Commands and admin work in private channel
- Clean, beautiful posts in public feed
- No command spam in public channels

---

## ⚙️ Current Configuration

After deploying, check your Railway logs to see:
```
✅ Bot is ready! Logged in as YourBot#1234
📡 Bot ID: 123456789...
🎯 Target Channel ID: 1334165445271617546
🎮 Control Channel ID: 1234567890123456789
📝 Loaded 0 previously posted links
==================================================
```

If you see `Control Channel: Any channel/DM allowed`, it means CONTROL_CHANNEL_ID is not set (or set to 0).

---

## 🆘 Troubleshooting

### Bot won't respond to commands
- ✅ Check you're in the CONTROL_CHANNEL or DM
- ✅ Try using DM - it always works

### Posts don't appear in target channel
- ✅ Verify TARGET_CHANNEL_ID is correct
- ✅ Make sure bot has permissions in that channel

### Want to change channels?
1. Update environment variables in Railway
2. Bot will auto-redeploy
3. Test with `!panel` command

---

**Need help setting up your channels? Let me know!** 🚀

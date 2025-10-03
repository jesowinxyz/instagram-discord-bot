# Instagram Discord Bot - Hosting Guide

## 🚀 Deploy to Railway.app (RECOMMENDED with GitHub Student Pack)

Railway gives you $5/month in free credits with the Student Developer Pack - perfect for keeping your bot online 24/7!

### Step 1: Push to GitHub

1. Initialize git repository:
```bash
git init
git add .
git commit -m "Initial commit - Instagram Discord Bot"
```

2. Create a new repository on GitHub
3. Push your code:
```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

⚠️ **IMPORTANT:** Make sure your bot token is NOT in the code before pushing!

### Step 2: Deploy to Railway

1. Go to [Railway.app](https://railway.app)
2. Sign in with GitHub
3. Click **"New Project"**
4. Select **"Deploy from GitHub repo"**
5. Choose your bot repository
6. Railway will auto-detect it's a Python app

### Step 3: Set Environment Variables

In Railway dashboard:
1. Go to your project
2. Click **"Variables"** tab
3. Add these variables:
   - `BOT_TOKEN` = `your_discord_bot_token_here`
   - `TARGET_CHANNEL_ID` = `1334165445271617546`

### Step 4: Deploy!

Railway will automatically deploy your bot. You'll see logs showing:
```
✅ Bot is ready! Logged in as YourBot#1234
```

---

## 🎨 Alternative: Deploy to Render.com

### Step 1: Push to GitHub (same as above)

### Step 2: Deploy to Render

1. Go to [Render.com](https://render.com)
2. Sign in with GitHub
3. Click **"New +"** → **"Web Service"**
4. Connect your GitHub repository
5. Configure:
   - **Name:** instagram-discord-bot
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python bot.py`
   - **Plan:** Free

### Step 3: Set Environment Variables

In Render dashboard:
1. Go to **"Environment"** tab
2. Add:
   - `BOT_TOKEN` = `your_discord_bot_token_here`
   - `TARGET_CHANNEL_ID` = `1334165445271617546`

⚠️ **Note:** Render free tier sleeps after 15 mins of inactivity. Your bot will go offline!

---

## 🔧 Alternative: Heroku (with Student Pack)

### Step 1: Install Heroku CLI
```bash
# Download from: https://devcenter.heroku.com/articles/heroku-cli
```

### Step 2: Login and Create App
```bash
heroku login
heroku create your-instagram-bot
```

### Step 3: Set Environment Variables
```bash
heroku config:set BOT_TOKEN="your_bot_token_here"
heroku config:set TARGET_CHANNEL_ID="1334165445271617546"
```

### Step 4: Deploy
```bash
git push heroku main
```

### Step 5: Scale Worker
```bash
heroku ps:scale web=1
```

---

## 📋 Quick Comparison

| Platform | Cost | Always On? | Setup Difficulty | Student Pack Benefit |
|----------|------|------------|------------------|---------------------|
| **Railway** | $5/mo credit FREE | ✅ Yes | ⭐ Easy | ✅ Free credits |
| **Render** | Free tier | ❌ Sleeps | ⭐⭐ Easy | ❌ No |
| **Heroku** | Free credits | ✅ Yes | ⭐⭐⭐ Medium | ✅ Free credits |

**Recommendation:** Use **Railway.app** - it's the easiest and stays online 24/7 with your Student Pack!

---

## 🔒 Security Checklist Before Deploying

- [ ] Bot token is NOT hardcoded in bot.py
- [ ] Added `.gitignore` to exclude `.env` files
- [ ] Using environment variables for sensitive data
- [ ] `.env` file is NOT committed to git
- [ ] Posted links database is gitignored

---

## 🧪 Test Locally First

Before deploying, test locally with environment variables:

### Windows (PowerShell):
```powershell
$env:BOT_TOKEN="your_token_here"
$env:TARGET_CHANNEL_ID="1334165445271617546"
python bot.py
```

### Linux/Mac:
```bash
export BOT_TOKEN="your_token_here"
export TARGET_CHANNEL_ID="1334165445271617546"
python bot.py
```

---

## 🎉 After Deployment

Your bot will be online 24/7! You can:
- Send Instagram links via DM
- Use `!reel <link>` command
- Use `!panel` for the UI

Monitor your bot:
- Railway: View logs in dashboard
- Render: View logs in dashboard
- Heroku: `heroku logs --tail`

---

## 🆘 Troubleshooting

### Bot goes offline on Render
- This is normal on free tier - it sleeps after inactivity
- Upgrade to paid plan or use Railway/Heroku instead

### "BOT_TOKEN not found"
- Make sure you set environment variables in the platform dashboard
- Check spelling: `BOT_TOKEN` (exact case)

### Bot can't post to channel
- Verify `TARGET_CHANNEL_ID` is correct
- Ensure bot has permissions in that channel

---

**Need help? Let me know which platform you choose and I'll guide you through it!** 🚀

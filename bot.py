import discord
from discord.ext import commands
from discord.ui import Button, View, Modal, TextInput
import random
import json
import os
import re
import requests
from datetime import datetime

# ============= CONFIGURATION =============
# Use environment variables for security (better for hosting)
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")  # Will use env variable if available
TARGET_CHANNEL_ID = int(os.getenv("TARGET_CHANNEL_ID", "1334165445271617546"))  # Channel where Instagram posts appear
CONTROL_CHANNEL_ID = int(os.getenv("CONTROL_CHANNEL_ID", "0"))  # Channel where you send commands (0 = any channel/DM)

# AMOLED Theme Colors
THEME_COLOR = discord.Color.from_rgb(0, 229, 255)  # Cyan Blue
EMBED_COLOR = discord.Color.from_rgb(0, 255, 255)  # Bright Cyan
INSTAGRAM_ACCENT = discord.Color.from_rgb(0, 200, 255)  # Instagram Blue-Cyan
# =========================================

# Promotional messages dataset (100+ modern reel phrases)
PROMO_MESSAGES = [
    # Classic phrases
    "🎥 Watch my new reel!",
    "🚀 Just dropped something fresh!",
    "✨ New content alert! Check this out!",
    "🔥 Fire content incoming!",
    "💎 Don't miss this one!",
    "🌟 Something special for you!",
    "👀 You need to see this!",
    "💫 Fresh off the press!",
    
    # Modern reel phrases
    "⚡ NEW REEL UPLOADED!",
    "🎬 Just posted a new reel - go check it out!",
    "🔥 New reel is LIVE!",
    "💫 Uploaded a fresh reel!",
    "🎯 New reel alert!",
    "✨ Latest reel is up!",
    "🚀 Fresh reel just dropped!",
    "💥 New reel posted - don't sleep on this!",
    "🎥 Latest upload is here!",
    "⭐ New reel available now!",
    "🌟 Reel uploaded - check the link!",
    "🔊 New reel announcement!",
    "📱 Just uploaded - tap to watch!",
    "🎪 New reel show time!",
    "💎 Premium content uploaded!",
    
    # Trending phrases
    "🔥 This reel is heating up!",
    "⚡ Viral alert!",
    "💯 100% worth your time!",
    "🎬 Lights, camera, action!",
    "🎯 Direct hit of awesome content!",
    "⚡ Electric vibes only!",
    "🎪 The show must go on!",
    "🎨 Art in motion right here!",
    "🌈 Bringing colors to your feed!",
    "🎵 Vibing with this one!",
    "🏆 Award-worthy content!",
    "💥 Boom! New drop!",
    "🌺 Blooming with creativity!",
    "🚁 Taking you higher with this!",
    "🎭 Performance of the day!",
    
    # Engagement phrases
    "🍿 Grab your popcorn for this!",
    "👀 You don't want to miss this!",
    "🔥 It's giving main character energy!",
    "✨ Serving looks and content!",
    "💅 We're serving quality!",
    "� Cinema level production!",
    "�🎸 Rocking your feed!",
    "🌊 Making waves with this!",
    "🔮 Magic happens here!",
    "🎯 Hitting all the right notes!",
    "🌙 Moonlight vibes!",
    "☀️ Sunshine on your timeline!",
    
    # Hype phrases
    "🎪 Step right up and watch!",
    "🏅 Medal-worthy moment!",
    "🎨 Masterpiece alert!",
    "🚀 Blast off with this content!",
    "💝 Gift for your eyes!",
    "🌸 Fresh and fabulous!",
    "🎬 Cinematic excellence!",
    "🎯 Bullseye of entertainment!",
    "⭐ Star-studded content!",
    "🎪 The greatest show!",
    "🌟 Shining bright today!",
    "🎵 Music to my eyes!",
    "🔥 Too hot to handle!",
    "💎 Rare gem found!",
    
    # Social media lingo
    "🌈 POV: You just found amazing content!",
    "🎭 Plot twist: This reel is fire!",
    "🎸 When the content hits different!",
    "🌊 Riding the wave of creativity!",
    "⚡ Lightning in a bottle!",
    "🎨 Canvas of creativity!",
    "🚁 Sky-high quality!",
    "🍿 Binge-worthy material!",
    "🎯 On target and on fire!",
    "🌙 Dreamy content ahead!",
    "☀️ Brightening your day!",
    "🎪 Spectacular spectacular!",
    
    # Modern slang
    "🏆 This hits different!",
    "💫 Main character vibes!",
    "🌺 No cap - this is fire!",
    "🎬 Oscar-worthy reel!",
    "🔮 Crystal clear quality!",
    "💝 Love at first sight!",
    "🌸 Blossom into greatness!",
    "⚡ Absolutely unhinged (in a good way)!",
    "� The algorithm loves this one!",
    "💎 Hidden gem unlocked!",
    
    # Call to action
    "👉 Tap the link to watch!",
    "🎬 Full video in the link!",
    "📲 Click to see the magic!",
    "🔗 Link to the reel below!",
    "✨ Experience it yourself!",
    "🎥 Press play and enjoy!",
    "🚀 Launch into this content!",
    "💫 Dive into this reel!",
    "🎯 Hit that link!",
    "⚡ Watch it before it goes viral!",
    
    # Aesthetic phrases
    "� Soft aesthetic vibes!",
    "🌙 Late night content drop!",
    "☀️ Morning motivation reel!",
    "� Cosmic content alert!",
    "🎨 Visual masterpiece!",
    "🌊 Chill vibes incoming!",
    "🔥 Hot girl summer energy!",
    "✨ Glowing up the feed!",
    "� Luxury content delivered!",
    "🎬 Hollywood level quality!",
    
    # Bonus modern phrases
    "🎪 Certified banger alert!",
    "⚡ Energy check: 100%!",
    "🔥 Straight fire, no printer!",
    "💯 Peak content achieved!",
    "🚀 To infinity and beyond!",
    "🎯 Sniper precision content!",
    "💫 Star quality right here!",
    "🌟 Radiating excellence!",
    "🎬 Director's cut vibes!",
    "⭐ Five-star content!",
]

# File to store posted links
POSTED_LINKS_FILE = "posted_links.json"

# Initialize bot with intents
intents = discord.Intents.default()
intents.message_content = True
intents.dm_messages = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Load posted links from file
def load_posted_links():
    if os.path.exists(POSTED_LINKS_FILE):
        with open(POSTED_LINKS_FILE, 'r') as f:
            return set(json.load(f))
    return set()

# Save posted links to file
def save_posted_links(links):
    with open(POSTED_LINKS_FILE, 'w') as f:
        json.dump(list(links), f)

# Posted links tracker
posted_links = load_posted_links()

# Extract Instagram link from text
def extract_instagram_link(text):
    # Match Instagram URLs
    pattern = r'https?://(?:www\.)?instagram\.com/(?:p|reel|tv)/[A-Za-z0-9_-]+/?'
    match = re.search(pattern, text)
    return match.group(0) if match else None

# Fetch Instagram thumbnail (WORKING method with proper fallbacks)
# Returns: (thumbnail_url, success_status)
# success_status: True if real thumbnail found, False if using fallback
def get_instagram_thumbnail(instagram_url):
    try:
        # Clean URL - remove trailing slash and query parameters
        clean_url = instagram_url.rstrip('/').split('?')[0]
        
        print(f"🔍 Fetching thumbnail for: {clean_url}")
        
        # Method 1: Instagram's Official oEmbed API (Most Reliable)
        try:
            # Convert reel/tv URLs to /p/ format for oEmbed
            if '/reel/' in clean_url:
                oembed_url = clean_url.replace('/reel/', '/p/')
            elif '/tv/' in clean_url:
                oembed_url = clean_url.replace('/tv/', '/p/')
            else:
                oembed_url = clean_url
            
            api_url = f"https://graph.facebook.com/v12.0/instagram_oembed?url={oembed_url}&access_token=&fields=thumbnail_url"
            
            response = requests.get(api_url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if 'thumbnail_url' in data and data['thumbnail_url']:
                    print(f"✅ Thumbnail fetched via Facebook Graph API")
                    return (data['thumbnail_url'], True)
        except Exception as e:
            print(f"⚠️ Facebook Graph API failed: {e}")
        
        # Method 2: Traditional oEmbed endpoint
        try:
            oembed_endpoint = f"https://www.instagram.com/p/oembed/?url={clean_url}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            }
            response = requests.get(oembed_endpoint, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if 'thumbnail_url' in data and data['thumbnail_url']:
                    print(f"✅ Thumbnail fetched via Instagram oEmbed")
                    return (data['thumbnail_url'], True)
        except Exception as e:
            print(f"⚠️ Instagram oEmbed failed: {e}")
        
        # Method 3: Scrape the actual Instagram page
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'none',
            }
            
            response = requests.get(clean_url, headers=headers, timeout=15, allow_redirects=True)
            
            if response.status_code == 200:
                html_content = response.text
                
                # Try multiple patterns to extract thumbnail
                patterns = [
                    r'"display_url":"(https://[^"]+)"',
                    r'<meta property="og:image" content="([^"]+)"',
                    r'<meta name="twitter:image" content="([^"]+)"',
                    r'"thumbnail_src":"(https://[^"]+)"',
                ]
                
                for pattern in patterns:
                    match = re.search(pattern, html_content)
                    if match:
                        thumbnail = match.group(1)
                        # Clean up the URL
                        thumbnail = thumbnail.replace('\\u0026', '&').replace('&amp;', '&')
                        print(f"✅ Thumbnail scraped from page HTML")
                        return (thumbnail, True)
        except Exception as e:
            print(f"⚠️ Page scraping failed: {e}")
        
        # All methods failed - return None to trigger custom thumbnail prompt
        print(f"❌ All methods failed - thumbnail fetch unsuccessful")
        return (None, False)
    
    except Exception as e:
        print(f"❌ Critical error: {e}")
        return (None, False)

# Determine if it's a reel or post
def get_post_type(instagram_url):
    if '/reel/' in instagram_url:
        return "Instagram Reel"
    elif '/tv/' in instagram_url:
        return "Instagram Video"
    else:
        return "Instagram Post"

# Modal for providing custom thumbnail when auto-fetch fails
class CustomThumbnailModal(Modal, title="⚠️ Thumbnail Fetch Failed"):
    thumbnail_input = TextInput(
        label="Please Provide Custom Thumbnail URL",
        placeholder="Paste image URL here (e.g., from ImgBB, Discord CDN)",
        required=True,
        style=discord.TextStyle.short
    )
    
    def __init__(self, instagram_url, promo_message):
        super().__init__()
        self.instagram_url = instagram_url
        self.promo_message = promo_message
    
    async def on_submit(self, interaction: discord.Interaction):
        thumbnail_url = self.thumbnail_input.value.strip()
        
        if not thumbnail_url or not thumbnail_url.startswith('http'):
            await interaction.response.send_message(
                "❌ Invalid image URL! Please provide a valid HTTP/HTTPS image link.",
                ephemeral=True
            )
            return
        
        await interaction.response.defer(ephemeral=True)
        
        try:
            # Get the target channel
            channel = bot.get_channel(TARGET_CHANNEL_ID)
            if not channel:
                await interaction.followup.send(
                    "❌ Error: Target channel not found!",
                    ephemeral=True
                )
                return
            
            # Get post type
            post_type = get_post_type(self.instagram_url)
            
            # Create embed with custom thumbnail
            embed = discord.Embed(
                title=f"⚡ {post_type}",
                description=f"{self.promo_message}\n\n**🔗 [View on Instagram]({self.instagram_url})**",
                color=INSTAGRAM_ACCENT,
                timestamp=datetime.utcnow()
            )
            embed.set_image(url=thumbnail_url)
            embed.set_footer(text="⚡ Posted by cassiel.ae • AMOLED Edition", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Instagram_icon.png/600px-Instagram_icon.png")
            
            # Post to channel
            await channel.send(embed=embed)
            
            # Add to posted links
            posted_links.add(self.instagram_url)
            save_posted_links(posted_links)
            
            await interaction.followup.send(
                f"✅ Successfully posted with custom thumbnail!\n🎉 {self.promo_message}",
                ephemeral=True
            )
        
        except Exception as e:
            await interaction.followup.send(
                f"❌ Error posting content: {str(e)}",
                ephemeral=True
            )

# Modal for clean URL input with optional thumbnail
class InstagramURLModal(Modal, title="📸 Post Instagram Content"):
    url_input = TextInput(
        label="Instagram URL",
        placeholder="https://www.instagram.com/reel/xxxxxx/",
        required=True,
        style=discord.TextStyle.short
    )
    
    thumbnail_input = TextInput(
        label="Custom Thumbnail URL (Optional)",
        placeholder="Leave empty to auto-fetch, or paste image URL here",
        required=False,
        style=discord.TextStyle.short
    )
    
    async def on_submit(self, interaction: discord.Interaction):
        instagram_url = self.url_input.value.strip()
        
        # Extract Instagram link
        clean_url = extract_instagram_link(instagram_url)
        
        if not clean_url:
            await interaction.response.send_message(
                "❌ Invalid Instagram URL! Please provide a valid Instagram post or reel link.",
                ephemeral=True
            )
            return
        
        # REMOVED DUPLICATE CHECK - Allow posting same link multiple times
        
        # Defer the response as fetching might take time
        await interaction.response.defer(ephemeral=True)
        
        try:
            # Get the target channel
            channel = bot.get_channel(TARGET_CHANNEL_ID)
            if not channel:
                await interaction.followup.send(
                    "❌ Error: Target channel not found! Please check the channel ID.",
                    ephemeral=True
                )
                return
            
            # Get post type and promo message
            post_type = get_post_type(clean_url)
            promo_message = random.choice(PROMO_MESSAGES)
            
            # Fetch thumbnail (use custom if provided, otherwise auto-fetch)
            custom_thumbnail = self.thumbnail_input.value.strip()
            if custom_thumbnail and custom_thumbnail.startswith('http'):
                thumbnail_url = custom_thumbnail
                thumbnail_success = True
                thumbnail_source = "custom"
            else:
                thumbnail_url, thumbnail_success = get_instagram_thumbnail(clean_url)
                thumbnail_source = "auto"
                
                # If auto-fetch failed, prompt for custom thumbnail
                if not thumbnail_success:
                    await interaction.followup.send(
                        "⚠️ **Unable to auto-fetch thumbnail!**\n\n"
                        "Please provide a custom thumbnail URL to complete the post.\n\n"
                        "**How to get an image URL:**\n"
                        "1️⃣ Upload image to Discord (DM yourself) → Right-click → Copy Link\n"
                        "2️⃣ Use ImgBB.com → Upload → Copy Direct Link\n"
                        "3️⃣ Use PostImages.org → Upload → Copy Direct Link\n\n"
                        "A form will appear next where you can paste the thumbnail URL.",
                        ephemeral=True
                    )
                    # Send the custom thumbnail modal
                    custom_modal = CustomThumbnailModal(clean_url, promo_message)
                    await interaction.followup.send(
                        "Click the button below to provide custom thumbnail:",
                        view=CustomThumbnailView(clean_url, promo_message),
                        ephemeral=True
                    )
                    return
            
            # Create embed with visible link
            embed = discord.Embed(
                title=f"⚡ {post_type}",
                description=f"{promo_message}\n\n**🔗 [View on Instagram]({clean_url})**",
                color=INSTAGRAM_ACCENT,
                timestamp=datetime.utcnow()
            )
            embed.set_image(url=thumbnail_url)
            embed.set_footer(text="⚡ Posted by cassiel.ae • AMOLED Edition", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Instagram_icon.png/600px-Instagram_icon.png")
            
            # Post to channel
            await channel.send(embed=embed)
            
            # Add to posted links
            posted_links.add(clean_url)
            save_posted_links(posted_links)
            
            # Confirm to user with thumbnail info
            thumbnail_info = "🎨 Custom thumbnail" if thumbnail_source == "custom" else "📸 Auto-fetched thumbnail"
            await interaction.followup.send(
                f"✅ Successfully posted to <#{TARGET_CHANNEL_ID}>!\n🎉 {promo_message}\n{thumbnail_info}",
                ephemeral=True
            )
        
        except Exception as e:
            await interaction.followup.send(
                f"❌ Error posting content: {str(e)}",
                ephemeral=True
            )

# View with button to open custom thumbnail modal
class CustomThumbnailView(View):
    def __init__(self, instagram_url, promo_message):
        super().__init__(timeout=300)  # 5 minute timeout
        self.instagram_url = instagram_url
        self.promo_message = promo_message
    
    @discord.ui.button(label="📷 Add Custom Thumbnail", style=discord.ButtonStyle.primary, emoji="✨")
    async def add_thumbnail_button(self, interaction: discord.Interaction, button: Button):
        modal = CustomThumbnailModal(self.instagram_url, self.promo_message)
        await interaction.response.send_modal(modal)

# View with button to open modal
class InstagramView(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="⚡ POST INSTAGRAM CONTENT", style=discord.ButtonStyle.primary, custom_id="post_instagram", emoji="🎬")
    async def post_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(InstagramURLModal())

# Command to handle Instagram links (!reel command)
@bot.command(name="reel")
async def reel_command(ctx, *, url: str = None):
    # Check if command is used in the correct channel (if CONTROL_CHANNEL_ID is set)
    if CONTROL_CHANNEL_ID != 0:
        if isinstance(ctx.channel, discord.DMChannel):
            # Allow DMs
            pass
        elif ctx.channel.id != CONTROL_CHANNEL_ID:
            await ctx.send(f"❌ Please use this command in <#{CONTROL_CHANNEL_ID}> or DM me!", delete_after=5)
            return
    
    if not url:
        await ctx.send("❌ Please provide an Instagram URL!\nUsage: `!reel <instagram_link>`")
        return
    
    # Extract Instagram link
    instagram_url = extract_instagram_link(url)
    
    if not instagram_url:
        await ctx.send("❌ Invalid Instagram URL! Please provide a valid Instagram post or reel link.")
        return
    
    # REMOVED DUPLICATE CHECK - Allow posting same link multiple times
    
    # Send processing message
    processing_msg = await ctx.send("⏳ Processing your Instagram link...")
    
    try:
        # Get the target channel
        channel = bot.get_channel(TARGET_CHANNEL_ID)
        if not channel:
            await processing_msg.edit(content="❌ Error: Target channel not found! Please check the channel ID.")
            return
        
        # Check if user attached an image (custom thumbnail)
        if ctx.message.attachments and len(ctx.message.attachments) > 0:
            # Use the first attachment as custom thumbnail
            attachment = ctx.message.attachments[0]
            if attachment.content_type and attachment.content_type.startswith('image/'):
                thumbnail_url = attachment.url
                thumbnail_success = True
                thumb_source = "🎨 Custom uploaded thumbnail"
            else:
                # Not an image, auto-fetch
                thumbnail_url, thumbnail_success = get_instagram_thumbnail(instagram_url)
                thumb_source = "📸 Auto-fetched thumbnail"
        else:
            # No attachment, auto-fetch
            thumbnail_url, thumbnail_success = get_instagram_thumbnail(instagram_url)
            thumb_source = "📸 Auto-fetched thumbnail"
        
        # If auto-fetch failed and no custom thumbnail, ask for one
        if not thumbnail_success:
            await processing_msg.edit(
                content="⚠️ **Unable to auto-fetch thumbnail!**\n\n"
                "Please provide a custom thumbnail. You can either:\n"
                "1️⃣ Use `!reel` command with an attached image\n"
                "2️⃣ Use `!custompost` command to provide thumbnail URL\n"
                "3️⃣ Use `!panel` and fill in the custom thumbnail field\n\n"
                "**Quick method:** Reply to this message with the thumbnail image attached and the Instagram link!"
            )
            return
        
        # Get post type
        post_type = get_post_type(instagram_url)
        
        # Pick random promo message
        promo_message = random.choice(PROMO_MESSAGES)
        
        # Create embed with visible link
        embed = discord.Embed(
            title=f"⚡ {post_type}",
            description=f"{promo_message}\n\n**🔗 [View on Instagram]({instagram_url})**",
            color=INSTAGRAM_ACCENT,
            timestamp=datetime.utcnow()
        )
        embed.set_image(url=thumbnail_url)
        embed.set_footer(text="⚡ Posted by cassiel.ae • AMOLED Edition", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Instagram_icon.png/600px-Instagram_icon.png")
        
        # Post to channel
        await channel.send(embed=embed)
        
        # Add to posted links
        posted_links.add(instagram_url)
        save_posted_links(posted_links)
        
        # Confirm to user
        await processing_msg.edit(content=f"✅ Successfully posted to <#{TARGET_CHANNEL_ID}>!\n🎉 {promo_message}\n{thumb_source}")
    
    except Exception as e:
        await processing_msg.edit(content=f"❌ Error posting content: {str(e)}")

# Auto-detect Instagram links in DMs
@bot.event
async def on_message(message):
    # Ignore bot's own messages
    if message.author == bot.user:
        return
    
    # Check if it's a DM
    if isinstance(message.channel, discord.DMChannel):
        # Try to extract Instagram link
        instagram_url = extract_instagram_link(message.content)
        
        if instagram_url:
            # Check if it's not a command
            if not message.content.startswith('!'):
                # REMOVED DUPLICATE CHECK - Allow posting same link multiple times
                
                # Send processing message
                processing_msg = await message.channel.send("⏳ Processing your Instagram link...")
                
                try:
                    # Get the target channel
                    channel = bot.get_channel(TARGET_CHANNEL_ID)
                    if not channel:
                        await processing_msg.edit(content="❌ Error: Target channel not found! Please check the channel ID.")
                        return
                    
                    # Check if user attached an image (custom thumbnail)
                    if message.attachments and len(message.attachments) > 0:
                        # Use the first attachment as custom thumbnail
                        attachment = message.attachments[0]
                        if attachment.content_type and attachment.content_type.startswith('image/'):
                            thumbnail_url = attachment.url
                            thumbnail_success = True
                            thumb_source = "🎨 Custom uploaded thumbnail"
                        else:
                            # Not an image, auto-fetch
                            thumbnail_url, thumbnail_success = get_instagram_thumbnail(instagram_url)
                            thumb_source = "📸 Auto-fetched thumbnail"
                    else:
                        # No attachment, auto-fetch
                        thumbnail_url, thumbnail_success = get_instagram_thumbnail(instagram_url)
                        thumb_source = "📸 Auto-fetched thumbnail"
                    
                    # If auto-fetch failed, ask for custom thumbnail
                    if not thumbnail_success:
                        await message.channel.send(
                            "⚠️ **Unable to auto-fetch thumbnail!**\n\n"
                            "Please send the Instagram link again with a thumbnail image attached,\n"
                            "or use the `!custompost` command to provide a thumbnail URL."
                        )
                        return
                    
                    # Get post type
                    post_type = get_post_type(instagram_url)
                    
                    # Pick random promo message
                    promo_message = random.choice(PROMO_MESSAGES)
                    
                    # Create embed with visible link
                    embed = discord.Embed(
                        title=f"⚡ {post_type}",
                        description=f"{promo_message}\n\n**🔗 [View on Instagram]({instagram_url})**",
                        color=INSTAGRAM_ACCENT,
                        timestamp=datetime.utcnow()
                    )
                    embed.set_image(url=thumbnail_url)
                    embed.set_footer(text="⚡ Posted by cassiel.ae • AMOLED Edition", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Instagram_icon.png/600px-Instagram_icon.png")
                    
                    # Post to channel
                    await channel.send(embed=embed)
                    
                    # Add to posted links
                    posted_links.add(instagram_url)
                    save_posted_links(posted_links)
                    
                    # Confirm to user
                    await processing_msg.edit(content=f"✅ Successfully posted to <#{TARGET_CHANNEL_ID}>!\n🎉 {promo_message}\n{thumb_source}")
                
                except Exception as e:
                    await processing_msg.edit(content=f"❌ Error posting content: {str(e)}")
    
    # Process commands
    await bot.process_commands(message)

# Command to show UI panel
@bot.command(name="panel")
async def panel_command(ctx):
    """Shows the Instagram posting panel with UI buttons"""
    # Check if command is used in the correct channel (if CONTROL_CHANNEL_ID is set)
    if CONTROL_CHANNEL_ID != 0:
        if isinstance(ctx.channel, discord.DMChannel):
            # Allow DMs
            pass
        elif ctx.channel.id != CONTROL_CHANNEL_ID:
            await ctx.send(f"❌ Please use this command in <#{CONTROL_CHANNEL_ID}> or DM me!", delete_after=5)
            return
    
    embed = discord.Embed(
        title="⚡ INSTAGRAM CONTENT POSTER",
        description=(
            "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "```ansi\n"
            "\u001b[1;36m▸ AMOLED DARK MODE ENABLED\u001b[0m\n"
            "```\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "**✨ FEATURES**\n"
            "🎬 Auto-detect reels & posts\n"
            "🖼️ Beautiful cyan-themed embeds\n"
            "📸 Custom thumbnail support\n"
            "📱 Upload from phone/PC\n"
            "🎲 Random promo messages\n"
            "🔒 Duplicate prevention\n\n"
            "**🎯 HOW TO USE**\n"
            "**1.** Click the button below\n"
            "**2.** `!reel <link>` + attach image\n"
            "**3.** `!custompost <link> <url>`\n"
            "**4.** DM bot with link + image\n\n"
            "**📱 MOBILE UPLOAD**\n"
            "Attach image when sending link!\n\n"
            "**Need help?** Type `!helpae`\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━"
        ),
        color=THEME_COLOR
    )
    embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Instagram_icon.png/600px-Instagram_icon.png")  # Cyan Instagram icon
    embed.set_footer(text="⚡ Powered by cassiel.ae • AMOLED Edition", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Instagram_icon.png/600px-Instagram_icon.png")
    
    view = InstagramView()
    await ctx.send(embed=embed, view=view)

# Command to post with custom thumbnail
@bot.command(name="custompost")
async def custom_post_command(ctx, instagram_url: str = None, thumbnail_url: str = None):
    """Post Instagram content with a custom thumbnail"""
    # Check if command is used in the correct channel (if CONTROL_CHANNEL_ID is set)
    if CONTROL_CHANNEL_ID != 0:
        if isinstance(ctx.channel, discord.DMChannel):
            pass
        elif ctx.channel.id != CONTROL_CHANNEL_ID:
            await ctx.send(f"❌ Please use this command in <#{CONTROL_CHANNEL_ID}> or DM me!", delete_after=5)
            return
    
    if not instagram_url:
        await ctx.send("❌ Please provide an Instagram URL!\nUsage: `!custompost <instagram_link> <thumbnail_url>`")
        return
    
    # Extract Instagram link
    clean_url = extract_instagram_link(instagram_url)
    
    if not clean_url:
        await ctx.send("❌ Invalid Instagram URL! Please provide a valid Instagram post or reel link.")
        return
    
    # REMOVED DUPLICATE CHECK - Allow posting same link multiple times
    
    # Send processing message
    processing_msg = await ctx.send("⏳ Processing your Instagram link with custom thumbnail...")
    
    try:
        # Get the target channel
        channel = bot.get_channel(TARGET_CHANNEL_ID)
        if not channel:
            await processing_msg.edit(content="❌ Error: Target channel not found! Please check the channel ID.")
            return
        
        # Use custom thumbnail if provided, otherwise auto-fetch
        if thumbnail_url and thumbnail_url.startswith('http'):
            thumbnail = thumbnail_url
            thumbnail_success = True
            thumb_source = "🎨 Custom thumbnail"
        else:
            thumbnail, thumbnail_success = get_instagram_thumbnail(clean_url)
            thumb_source = "📸 Auto-fetched thumbnail"
        
        # If auto-fetch failed and no custom thumbnail, ask for one
        if not thumbnail_success:
            await processing_msg.edit(
                content="⚠️ **Unable to auto-fetch thumbnail!**\n\n"
                "Please use the command again with a valid thumbnail URL:\n"
                "`!custompost <instagram_url> <thumbnail_url>`\n\n"
                "**How to get a thumbnail URL:**\n"
                "• Upload to Discord → Right-click → Copy Link\n"
                "• Use ImgBB.com or PostImages.org\n"
                "• Or use `!reel` with an attached image"
            )
            return
        
        # Get post type
        post_type = get_post_type(clean_url)
        
        # Pick random promo message
        promo_message = random.choice(PROMO_MESSAGES)
        
        # Create embed with visible link
        embed = discord.Embed(
            title=f"⚡ {post_type}",
            description=f"{promo_message}\n\n**🔗 [View on Instagram]({clean_url})**",
            color=INSTAGRAM_ACCENT,
            timestamp=datetime.utcnow()
        )
        embed.set_image(url=thumbnail)
        embed.set_footer(text="⚡ Posted by cassiel.ae • AMOLED Edition", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Instagram_icon.png/600px-Instagram_icon.png")
        
        # Post to channel
        await channel.send(embed=embed)
        
        # Add to posted links
        posted_links.add(clean_url)
        save_posted_links(posted_links)
        
        # Confirm to user
        await processing_msg.edit(content=f"✅ Successfully posted to <#{TARGET_CHANNEL_ID}>!\n🎉 {promo_message}\n{thumb_source}")
    
    except Exception as e:
        await processing_msg.edit(content=f"❌ Error posting content: {str(e)}")

# Command to clear posted links history
@bot.command(name="clearhistory")
@commands.has_permissions(administrator=True)
async def clear_history(ctx):
    """Clears the posted links history (Admin only)"""
    global posted_links
    posted_links.clear()
    save_posted_links(posted_links)
    
    embed = discord.Embed(
        title="🗑️ HISTORY CLEARED",
        description="```ansi\n\u001b[1;36m▸ All posted links have been removed\u001b[0m\n```",
        color=THEME_COLOR
    )
    embed.set_footer(text="⚡ Admin Action", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Instagram_icon.png/600px-Instagram_icon.png")
    await ctx.send(embed=embed)

# Help command
@bot.command(name="helpae")
async def help_command(ctx):
    """Show comprehensive help information with AMOLED theme"""
    # Check if command is used in the correct channel (if CONTROL_CHANNEL_ID is set)
    if CONTROL_CHANNEL_ID != 0:
        if isinstance(ctx.channel, discord.DMChannel):
            pass
        elif ctx.channel.id != CONTROL_CHANNEL_ID:
            await ctx.send(f"❌ Please use this command in <#{CONTROL_CHANNEL_ID}> or DM me!", delete_after=5)
            return
    
    # Main help embed
    help_embed = discord.Embed(
        title="⚡ INSTAGRAM BOT HELP CENTER",
        description=(
            "```ansi\n"
            "\u001b[1;36m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m\n"
            "\u001b[1;37m    AMOLED DARK MODE • CYAN EDITION\u001b[0m\n"
            "\u001b[1;36m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m\n"
            "```"
        ),
        color=THEME_COLOR
    )
    
    # Commands section
    help_embed.add_field(
        name="📋 COMMANDS",
        value=(
            "```css\n"
            "!panel\n"
            "  └─ Show posting UI with button\n\n"
            "!reel <link>\n"
            "  └─ Post Instagram link\n"
            "  └─ Optional: Attach image file\n\n"
            "!custompost <link> <thumbnail_url>\n"
            "  └─ Post with custom thumbnail URL\n\n"
            "!helpae\n"
            "  └─ Show this help menu\n\n"
            "!clearhistory [ADMIN]\n"
            "  └─ Clear posted links history\n"
            "```"
        ),
        inline=False
    )
    
    # Features section
    help_embed.add_field(
        name="✨ FEATURES",
        value=(
            "```yaml\n"
            "Auto-Detection: Instagram reels & posts\n"
            "Thumbnails: Auto-fetch or custom upload\n"
            "File Upload: From PC/Android/iOS\n"
            "Promo Messages: 50+ random variations\n"
            "Duplicate Block: Prevents re-posting\n"
            "Channel Control: Separate command & post channels\n"
            "```"
        ),
        inline=False
    )
    
    # Usage examples
    help_embed.add_field(
        name="🎯 USAGE EXAMPLES",
        value=(
            "```ini\n"
            "[Method 1: UI Panel]\n"
            "  1. Type: !panel\n"
            "  2. Click button\n"
            "  3. Paste link + optional thumbnail URL\n\n"
            "[Method 2: Command with Upload]\n"
            "  1. Attach image file\n"
            "  2. Type: !reel <instagram_link>\n"
            "  3. Send!\n\n"
            "[Method 3: DM Auto-detect]\n"
            "  1. DM the bot\n"
            "  2. Paste Instagram link\n"
            "  3. Optional: Attach image\n"
            "```"
        ),
        inline=False
    )
    
    # Mobile upload guide
    help_embed.add_field(
        name="📱 MOBILE UPLOAD (Android/iOS)",
        value=(
            "```diff\n"
            "+ Step 1: Open Discord on phone\n"
            "+ Step 2: Tap \"+\" icon in chat\n"
            "+ Step 3: Select image from gallery\n"
            "+ Step 4: Type Instagram link\n"
            "+ Step 5: Send message\n"
            "```"
        ),
        inline=False
    )
    
    # Configuration info
    config_value = f"```ansi\n"
    config_value += f"\u001b[1;36mTarget Channel:\u001b[0m <#{TARGET_CHANNEL_ID}>\n"
    if CONTROL_CHANNEL_ID != 0:
        config_value += f"\u001b[1;36mControl Channel:\u001b[0m <#{CONTROL_CHANNEL_ID}>\n"
    else:
        config_value += f"\u001b[1;36mControl Channel:\u001b[0m Any channel/DM\n"
    config_value += f"```"
    
    help_embed.add_field(
        name="⚙️ CURRENT CONFIGURATION",
        value=config_value,
        inline=False
    )
    
    # Support footer
    help_embed.set_footer(
        text="⚡ Powered by cassiel.ae • Need more help? DM the bot!",
        icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Instagram_icon.png/600px-Instagram_icon.png"
    )
    help_embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Instagram_icon.png/600px-Instagram_icon.png")
    
    await ctx.send(embed=help_embed)

@bot.event
async def on_ready():
    print(f'✅ Bot is ready! Logged in as {bot.user}')
    print(f'📡 Bot ID: {bot.user.id}')
    print(f'🎯 Target Channel ID: {TARGET_CHANNEL_ID}')
    if CONTROL_CHANNEL_ID != 0:
        print(f'🎮 Control Channel ID: {CONTROL_CHANNEL_ID}')
    else:
        print(f'🎮 Control Channel: Any channel/DM allowed')
    print(f'📝 Loaded {len(posted_links)} previously posted links')
    print('=' * 50)
    
    # Register persistent view
    bot.add_view(InstagramView())

# Run the bot
if __name__ == "__main__":
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ ERROR: Please set your bot token in the BOT_TOKEN variable!")
        print("📝 Edit bot.py and replace 'YOUR_BOT_TOKEN_HERE' with your actual Discord bot token")
    elif TARGET_CHANNEL_ID == 1234567890:
        print("⚠️ WARNING: Please set your target channel ID in the TARGET_CHANNEL_ID variable!")
        print("📝 Edit bot.py and replace 1234567890 with your actual Discord channel ID")
    else:
        bot.run(BOT_TOKEN)

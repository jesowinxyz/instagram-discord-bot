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
# =========================================

# Promotional messages dataset (50+ messages)
PROMO_MESSAGES = [
    "🎥 Watch my new reel!",
    "🚀 Just dropped something fresh!",
    "✨ New content alert! Check this out!",
    "🔥 Fire content incoming!",
    "💎 Don't miss this one!",
    "🌟 Something special for you!",
    "👀 You need to see this!",
    "💫 Fresh off the press!",
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
    "🍿 Grab your popcorn for this!",
    "🎸 Rocking your feed!",
    "🌊 Making waves with this!",
    "🔮 Magic happens here!",
    "🎯 Hitting all the right notes!",
    "🌙 Moonlight vibes!",
    "☀️ Sunshine on your timeline!",
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
    "🌈 Rainbow of awesomeness!",
    "🎭 Drama and delight!",
    "🎸 Strumming your heartstrings!",
    "🌊 Surf's up on this content!",
    "⚡ Lightning strikes twice!",
    "🎨 Canvas of creativity!",
    "🚁 Sky-high quality!",
    "🍿 Binge-worthy material!",
    "🎯 On target and on fire!",
    "🌙 Dreamy content ahead!",
    "☀️ Brightening your day!",
    "🎪 Spectacular spectacular!",
    "🏆 Championship content!",
    "💫 Stardust and magic!",
    "🌺 Exotic and exciting!",
    "🎬 Oscar-worthy reel!",
    "🔮 Crystal clear quality!",
    "💝 Love at first sight!",
    "🌸 Blossom into greatness!"
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

# Fetch Instagram thumbnail (improved method)
def get_instagram_thumbnail(instagram_url):
    try:
        # Method 1: Try Instagram's oEmbed API (public endpoint)
        oembed_url = f"https://www.instagram.com/p/oembed/?url={instagram_url}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Try oEmbed first
        try:
            oembed_response = requests.get(oembed_url, headers=headers, timeout=10)
            if oembed_response.status_code == 200:
                oembed_data = oembed_response.json()
                if 'thumbnail_url' in oembed_data:
                    return oembed_data['thumbnail_url']
        except:
            pass
        
        # Method 2: Scrape og:image from the page
        try:
            response = requests.get(instagram_url, headers=headers, timeout=10)
            if response.status_code == 200:
                # Look for og:image meta tag
                og_image_match = re.search(r'<meta property="og:image" content="([^"]+)"', response.text)
                if og_image_match:
                    return og_image_match.group(1)
                
                # Also try twitter:image
                twitter_image_match = re.search(r'<meta name="twitter:image" content="([^"]+)"', response.text)
                if twitter_image_match:
                    return twitter_image_match.group(1)
        except:
            pass
        
        # Fallback: return a generic Instagram icon
        return "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Instagram_icon.png/600px-Instagram_icon.png"
    
    except Exception as e:
        print(f"Error fetching thumbnail: {e}")
        # Return Instagram logo as fallback
        return "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Instagram_icon.png/600px-Instagram_icon.png"

# Determine if it's a reel or post
def get_post_type(instagram_url):
    if '/reel/' in instagram_url:
        return "Instagram Reel"
    elif '/tv/' in instagram_url:
        return "Instagram Video"
    else:
        return "Instagram Post"

# Modal for clean URL input
class InstagramURLModal(Modal, title="📸 Post Instagram Content"):
    url_input = TextInput(
        label="Instagram URL",
        placeholder="https://www.instagram.com/reel/xxxxxx/",
        required=True,
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
        
        # Check for duplicates
        if clean_url in posted_links:
            await interaction.response.send_message(
                "⚠️ This link has already been posted!",
                ephemeral=True
            )
            return
        
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
            
            # Fetch thumbnail
            thumbnail_url = get_instagram_thumbnail(clean_url)
            
            # Get post type
            post_type = get_post_type(clean_url)
            
            # Pick random promo message
            promo_message = random.choice(PROMO_MESSAGES)
            
            # Create embed
            embed = discord.Embed(
                title=post_type,
                description=promo_message,
                url=clean_url,
                color=discord.Color.from_rgb(225, 48, 108),  # Instagram pink
                timestamp=datetime.utcnow()
            )
            embed.set_image(url=thumbnail_url)
            embed.set_footer(text="Posted via Instagram Bot", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Instagram_icon.png/600px-Instagram_icon.png")
            
            # Post to channel
            await channel.send(embed=embed)
            
            # Add to posted links
            posted_links.add(clean_url)
            save_posted_links(posted_links)
            
            # Confirm to user
            await interaction.followup.send(
                f"✅ Successfully posted to <#{TARGET_CHANNEL_ID}>!\n🎉 {promo_message}",
                ephemeral=True
            )
        
        except Exception as e:
            await interaction.followup.send(
                f"❌ Error posting content: {str(e)}",
                ephemeral=True
            )

# View with button to open modal
class InstagramView(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="📸 Post Instagram Content", style=discord.ButtonStyle.primary, custom_id="post_instagram")
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
    
    # Check for duplicates
    if instagram_url in posted_links:
        await ctx.send("⚠️ This link has already been posted!")
        return
    
    # Send processing message
    processing_msg = await ctx.send("⏳ Processing your Instagram link...")
    
    try:
        # Get the target channel
        channel = bot.get_channel(TARGET_CHANNEL_ID)
        if not channel:
            await processing_msg.edit(content="❌ Error: Target channel not found! Please check the channel ID.")
            return
        
        # Fetch thumbnail
        thumbnail_url = get_instagram_thumbnail(instagram_url)
        
        # Get post type
        post_type = get_post_type(instagram_url)
        
        # Pick random promo message
        promo_message = random.choice(PROMO_MESSAGES)
        
        # Create embed
        embed = discord.Embed(
            title=post_type,
            description=promo_message,
            url=instagram_url,
            color=discord.Color.from_rgb(225, 48, 108),  # Instagram pink
            timestamp=datetime.utcnow()
        )
        embed.set_image(url=thumbnail_url)
        embed.set_footer(text="Posted via Instagram Bot", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Instagram_icon.png/600px-Instagram_icon.png")
        
        # Post to channel
        await channel.send(embed=embed)
        
        # Add to posted links
        posted_links.add(instagram_url)
        save_posted_links(posted_links)
        
        # Confirm to user
        await processing_msg.edit(content=f"✅ Successfully posted to <#{TARGET_CHANNEL_ID}>!\n🎉 {promo_message}")
    
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
                # Check for duplicates
                if instagram_url in posted_links:
                    await message.channel.send("⚠️ This link has already been posted!")
                    return
                
                # Send processing message
                processing_msg = await message.channel.send("⏳ Processing your Instagram link...")
                
                try:
                    # Get the target channel
                    channel = bot.get_channel(TARGET_CHANNEL_ID)
                    if not channel:
                        await processing_msg.edit(content="❌ Error: Target channel not found! Please check the channel ID.")
                        return
                    
                    # Fetch thumbnail
                    thumbnail_url = get_instagram_thumbnail(instagram_url)
                    
                    # Get post type
                    post_type = get_post_type(instagram_url)
                    
                    # Pick random promo message
                    promo_message = random.choice(PROMO_MESSAGES)
                    
                    # Create embed
                    embed = discord.Embed(
                        title=post_type,
                        description=promo_message,
                        url=instagram_url,
                        color=discord.Color.from_rgb(225, 48, 108),  # Instagram pink
                        timestamp=datetime.utcnow()
                    )
                    embed.set_image(url=thumbnail_url)
                    embed.set_footer(text="Posted via Instagram Bot", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Instagram_icon.png/600px-Instagram_icon.png")
                    
                    # Post to channel
                    await channel.send(embed=embed)
                    
                    # Add to posted links
                    posted_links.add(instagram_url)
                    save_posted_links(posted_links)
                    
                    # Confirm to user
                    await processing_msg.edit(content=f"✅ Successfully posted to <#{TARGET_CHANNEL_ID}>!\n🎉 {promo_message}")
                
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
        title="📸 Instagram Content Poster",
        description="Click the button below to post Instagram content to your channel!\n\n**Features:**\n• Auto-detect reels and posts\n• Beautiful embeds with thumbnails\n• Random promotional messages\n• Duplicate prevention\n\n**How to use:**\n1. Click the button below, OR\n2. Use `!reel <link>` command, OR\n3. Just paste an Instagram link in my DMs!",
        color=discord.Color.from_rgb(225, 48, 108)
    )
    embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Instagram_icon.png/600px-Instagram_icon.png")
    
    view = InstagramView()
    await ctx.send(embed=embed, view=view)

# Command to clear posted links history
@bot.command(name="clearhistory")
@commands.has_permissions(administrator=True)
async def clear_history(ctx):
    """Clears the posted links history (Admin only)"""
    global posted_links
    posted_links.clear()
    save_posted_links(posted_links)
    await ctx.send("✅ Posted links history has been cleared!")

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


import asyncio
import sys

from AlexaMusic.core.bot import AlexaBot
from AlexaMusic.core.dir import dirr
from AlexaMusic.core.git import git
from AlexaMusic.core.userbot import Userbot
from AlexaMusic.misc import dbb, heroku

from .logging import LOGGER


if sys.platform != "win32":
    try:
        import uvloop

        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        LOGGER(__name__).info("Using Uvloop Event Loop for Enhanced Performance")
    except ImportError:
        LOGGER(__name__).warning("Uvloop not found, using default event loop.")


# Directories
dirr()

# Check Git Updates
git()

# Initialize Memory DB
dbb()

# Heroku APP
heroku()

# Bot Client
app = AlexaBot()

# Assistant Client
userbot = Userbot()

from .platforms import *

YouTube = YouTubeAPI()
Carbon = CarbonAPI()
Spotify = SpotifyAPI()
Apple = AppleAPI()
Resso = RessoAPI()
SoundCloud = SoundAPI()
Telegram = TeleAPI()


# Use a logger for debug output - this will be managed by gPodder.
import logging
from pypresence import Presence # The simple rich presence client in pypresence
import time
import threading

logger = logging.getLogger(__name__)

# Provide some metadata that will be displayed in the gPodder GUI.
__title__ = 'Discord Rich Presence'
__description__ = 'Adds Discord Rich Presence to GPodder'
__only_for__ = 'gtk, cli'
__authors__ = 'amaki'
playing = False
whatisplaying = "Nothing"

def discord_rpc():
    global RPC
    global whatisplaying
    RPC = Presence("1054429322858999898")  # Initialize the Presence client
    RPC.connect()
    while True:
        print("Currently playing : " + whatisplaying)
        RPC.update(state="Listening to : '" + whatisplaying + "'")
        time.sleep(15)

x = threading.Thread(target=discord_rpc)
x.start()

class gPodderExtension:
    # The extension will be instantiated the first time it's used.
    # You can do some sanity checks here and raise an Exception if
    # you want to prevent the extension from being loaded.
    def __init__(self, container):
        self.container = container

    # This function will be called when the extension is enabled or
    # loaded. This is when you want to create helper objects or hook
    # into various parts of gPodder.
    def on_load(self):
        logger.info('Discord RPC Extension is being loaded.')


    # This function will be called when the extension is disabled or
    # when gPodder shuts down. You can use this to destroy/delete any
    # objects that you created in on_load().
    def on_unload(self):
        logger.info('Extension is being unloaded.')

    def on_ui_object_available(self, name, ui_object):
        """
        Called by gPodder when ui is ready.
        """
        if name == 'gpodder-gtk':
            self.gpodder = ui_object

    def on_episode_playback(self, episode):
        global whatisplaying
        print(episode.title)
        whatisplaying = episode.title




# Concurrency Warning: use gpodder.util.Popen() instead of subprocess.Popen()
#
# When using subprocess.Popen() to spawn a long-lived external command,
# such as ffmpeg, be sure to include the "close_fds=True" argument.
#
# https://docs.python.org/3/library/subprocess.html#subprocess.Popen
#
# This is expecially important for extensions responding to
# on_episode_downloaded(), which runs whenever a download finishes.
#
# Otherwise that process will inherit ALL file descriptors gPodder
# happens to have open at the moment (like other active downloads).
# Those files will remain 'in-use' until that process exits, a race
# condition which prevents gPodder from renaming or deleting them on Windows.
#
# Caveat: On Windows, you cannot set close_fds to true and also
# redirect the standard handles (stdin, stdout or stderr). To collect
# output/errors from long-lived external commands, it may be necessary
# to create a (temp) log file and read it afterward.

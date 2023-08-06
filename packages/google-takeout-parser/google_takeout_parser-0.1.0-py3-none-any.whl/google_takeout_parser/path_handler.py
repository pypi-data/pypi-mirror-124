"""
This handles mapping the filenames in the export
to the corresponding functions
"""

import os
import json
from pathlib import Path
from typing import Iterator, Union, Any

from cachew import cachew

from .common import Res
from .cache import takeout_cache_path
from .log import logger

from .models import (
    Activity,
    YoutubeComment,
    LikedYoutubeVideo,
    PlayStoreAppInstall,
    Location,
)

from .parse_html.activity import _parse_html_activity
from .parse_html.comment import _parse_html_comment_file
from .parse_json import (
    _parse_likes,
    _parse_app_installs,
    _parse_json_activity,
    _parse_location_history,
)

# when single_takeout_dir is called, register it with
# a global dict that knows the base path of the single takeout
# dir, so relative paths can be figured out
def simplify_path(p: Path) -> str:
    pass


Event = Union[
    Activity, YoutubeComment, LikedYoutubeVideo, PlayStoreAppInstall, Location
]

Results = Iterator[Res[Event]]


def parse_takeout(single_takeout_dir: Path) -> Results:

    handler_map = {
        "Google Photos": None,  # some of my old takeouts have this, dont use it anymore
        "Google Play Store/Devices": None,  # not that interesting
        "archive_browser.html": None,  # description of takeout, not useful
        "Google Play Store/Installs": _parse_app_installs,
        "Google Play Store/Library": None,
        "Google Play Store/Purchase History": None,
        "Google Play Store/Subscriptions": None,
        "Google Play Store/Redemption History": None,
        "Google Play Store/Promotion History": None,
        "My Activity/Takeout/MyActivity.html": None,
        "YouTube and YouTube Music/subscriptions": None,
        "YouTube and YouTube Music/videos": None,
        "Location History/Semantic Location History": None,  # not that much data here. maybe parse it?
        "Location History/Location History": _parse_location_history,
        "YouTube and YouTube Music/history/search-history.html": _parse_html_activity,
        "YouTube and YouTube Music/history/watch-history.html": _parse_html_activity,
        "YouTube and YouTube Music/history/search-history.json": _parse_json_activity,
        "YouTube and YouTube Music/history/watch-history.json": _parse_json_activity,
        "YouTube and YouTube Music/my-comments": _parse_html_comment_file,
        "YouTube and YouTube Music/my-live-chat-messages": _parse_html_comment_file,
        "YouTube and YouTube Music/playlists/likes.json": _parse_likes,
        "YouTube and YouTube Music/playlists/": None,  # dicts are ordered, so the rest of the stuff is ignored
        "My Activity/Ads": _parse_html_activity,
        "My Activity/Android": _parse_html_activity,
        "My Activity/Assistant": _parse_html_activity,
        "My Activity/Books": _parse_html_activity,
        "My Activity/Chrome": _parse_html_activity,
        "My Activity/Drive": _parse_html_activity,
        "My Activity/Developers": _parse_html_activity,
        "My Activity/Discover": _parse_html_activity,
        "My Activity/Gmail": _parse_html_activity,
        "My Activity/Google Analytics": _parse_html_activity,
        "My Activity/Google Apps": _parse_html_activity,
        "My Activity/Google Cloud": _parse_html_activity,
        "My Activity/Google Play Music": _parse_html_activity,
        "My Activity/Google Cloud": _parse_html_activity,
        "My Activity/Google Play Store": _parse_html_activity,
        "My Activity/Google Translate": _parse_html_activity,
        "My Activity/Podcasts": _parse_html_activity,
        "My Activity/Help": _parse_html_activity,
        "My Activity/Image Search": _parse_html_activity,
        "My Activity/Maps": _parse_html_activity,
        "My Activity/News": _parse_html_activity,
        "My Activity/Search": _parse_html_activity,
        "My Activity/Shopping": _parse_html_activity,
        "My Activity/Video Search": _parse_html_activity,
        "My Activity/YouTube": _parse_html_activity,
    }
    for f in single_takeout_dir.rglob("*"):
        handler: Any
        for prefix, h in handler_map.items():
            if (
                not str(f).startswith(os.path.join(single_takeout_dir, prefix))
                and f.is_file()
            ):
                continue
            handler = h
            break
        else:
            if f.is_dir():
                continue  # ignore directories
            else:
                e = RuntimeError(f"Unhandled file: {f}")
                logger.debug(str(e))
                yield e
                continue

        if handler is None:
            # explicitly ignored
            continue

        yield from handler(f)

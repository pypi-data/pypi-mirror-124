#!/usr/bin/env python3
# coding=utf-8

import logging
from typing import Optional

from praw.models import Submission

from bdfr.resource import Resource
from bdfr.site_authenticator import SiteAuthenticator
from bdfr.site_downloaders.fallback_downloaders.fallback_downloader import BaseFallbackDownloader
from bdfr.site_downloaders.youtube import Youtube

logger = logging.getLogger(__name__)


class YoutubeDlFallback(BaseFallbackDownloader, Youtube):
    def __init__(self, post: Submission):
        super(YoutubeDlFallback, self).__init__(post)

    def find_resources(self, authenticator: Optional[SiteAuthenticator] = None) -> list[Resource]:
        out = Resource(
            self.post,
            self.post.url,
            super()._download_video({}),
            super().get_video_attributes(self.post.url)['ext'],
        )
        return [out]

    @staticmethod
    def can_handle_link(url: str) -> bool:
        attributes = YoutubeDlFallback.get_video_attributes(url)
        if attributes:
            return True
        else:
            return False

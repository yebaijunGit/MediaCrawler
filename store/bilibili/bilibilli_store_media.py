# -*- coding: utf-8 -*-
# Copyright (c) 2025 relakkes@gmail.com
#
# This file is part of MediaCrawler project.
# Repository: https://github.com/NanmiCoder/MediaCrawler/blob/main/store/bilibili/bilibilli_store_media.py
# GitHub: https://github.com/NanmiCoder
# Licensed under NON-COMMERCIAL LEARNING LICENSE 1.1
#

# 声明：本代码仅供学习和研究目的使用。使用者应遵守以下原则：
# 1. 不得用于任何商业用途。
# 2. 使用时应遵守目标平台的使用条款和robots.txt规则。
# 3. 不得进行大规模爬取或对平台造成运营干扰。
# 4. 应合理控制请求频率，避免给目标平台带来不必要的负担。
# 5. 不得用于任何非法或不当的用途。
#
# 详细许可条款请参阅项目根目录下的LICENSE文件。
# 使用本代码即表示您同意遵守上述原则和LICENSE中的所有条款。

# -*- coding: utf-8 -*-
# @Author  : helloteemo
# @Time    : 2024/7/12 20:01
# @Desc    : Bilibili media storage
import pathlib
from typing import Dict

import aiofiles

from base.base_crawler import AbstractStoreImage, AbstractStoreVideo
from tools import utils
import config


class BilibiliVideo(AbstractStoreVideo):
    def __init__(self):
        if config.SAVE_DATA_PATH:
            self.video_store_path = f"{config.SAVE_DATA_PATH}/bili/videos"
        else:
            self.video_store_path = "data/bili/videos"

    async def store_video(self, video_content_item: Dict):
        """
        store content

        Args:
            video_content_item:

        Returns:

        """
        aid = video_content_item.get("aid")
        title = video_content_item.get("title", str(aid))
        user_nickname = video_content_item.get("user_nickname", "Unknown")
        collection_name = video_content_item.get("collection_name", "")  # New: video set/collection title
        
        # Sanitize for safe filenames and folder names
        import re
        title = re.sub(r'[\\/:*?"<>|]', '_', title)
        user_nickname = re.sub(r'[\\/:*?"<>|]', '_', user_nickname)
        if collection_name:
            collection_name = re.sub(r'[\\/:*?"<>|]', '_', collection_name)
        
        await self.save_video(
            aid, 
            video_content_item.get("video_content"), 
            video_content_item.get("extension_file_name"),
            title=title,
            user_nickname=user_nickname,
            collection_name=collection_name
        )

    def make_save_file_name(self, aid: str, extension_file_name: str, title: str = "", user_nickname: str = "", collection_name: str = "") -> str:
        """
        make save file name by store type

        Args:
            aid: aid
            extension_file_name: video filename with extension
            title: sanitized video title
            user_nickname: sanitized creator nickname
            collection_name: sanitized collection/video set name

        Returns:

        """
        # New structure: videos / Nickname / [CollectionTitle] / Title.mp4
        folder_path = f"{self.video_store_path}/{user_nickname}" if user_nickname else self.video_store_path
        if collection_name:
            folder_path = f"{folder_path}/{collection_name}"
        
        file_name = f"{title}.mp4" if title else extension_file_name
        return f"{folder_path}/{file_name}"

    async def save_video(self, aid: int, video_content: str, extension_file_name="mp4", title: str = "", user_nickname: str = "", collection_name: str = "") -> None:
        """
        save video to local

        Args:
            aid: aid
            video_content: video content
            extension_file_name: video filename with extension
            title: video title
            user_nickname: creator nickname
            collection_name: collection/video set name

        Returns:

        """
        # Create user sub-folder and collection sub-folder if exists
        folder_path = self.video_store_path + "/" + user_nickname if user_nickname else self.video_store_path
        if collection_name:
            folder_path = folder_path + "/" + collection_name
            
        pathlib.Path(folder_path).mkdir(parents=True, exist_ok=True)
        
        save_file_name = self.make_save_file_name(str(aid), extension_file_name, title=title, user_nickname=user_nickname, collection_name=collection_name)
        async with aiofiles.open(save_file_name, 'wb') as f:
            await f.write(video_content)
            utils.logger.info(f"[BilibiliVideoImplement.save_video] save save_video {save_file_name} success ...")

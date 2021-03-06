from vkbottle.tools import PhotoMessageUploader, DocMessagesUploader
from vkbottle.api import API
from os.path import abspath
from random import randint
from typing import Optional
import re


async def get_photo(photo_path: str, vk_api: API) -> str:
    """Returns an attachment as a photo, uploaded on a server

    :param photo_path: Path to a photo
    :param vk_api: Api for a bot
    :returns: An attachment string
    :raises: TODO
    """
    msg_uploader: PhotoMessageUploader = PhotoMessageUploader(vk_api)
    upload_str = await msg_uploader.upload(abspath(photo_path))
    return upload_str


async def get_document(document_path: str, vk_api: API, pid: int) -> str:
    """Returns an attachment as a document, uploaded on a server

    :param document_path: Path to a document
    :param vk_api: Api for a bot
    :param peer_id: Peer_id of a chat for uploading the document to
    :returns: An attachment string
    :raises: TODO
    """
    msg_uploader: DocMessagesUploader = DocMessagesUploader(vk_api)
    document_path = abspath(document_path)
    doctype: Optional[re.Match] = re.search(r"(?:\/\w+\.)\w+$", document_path)
    if doctype:
        upload_name: str = f"dance{randint(1, 999999)}.{doctype.group()}"
        upload_str = await msg_uploader.upload(
            upload_name,
            document_path,
            peer_id=pid
        )
        return upload_str
    else:
        raise FileNotFoundError("No document file extension was found")

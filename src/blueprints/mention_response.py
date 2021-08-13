from vkbottle.bot import Blueprint, Message
from vkbottle_types.objects import UsersUserXtrCounters
import re
from typing import List, Tuple
from src.commands.mention_commands import string_with_everyone, string_with_user

bp = Blueprint("For mention response")


async def extract_users(message: Message) -> List[UsersUserXtrCounters]:
    all_users: List[str] = re.findall(r"(?:id)\d+", message.text)
    if all_users:
        users: List[UsersUserXtrCounters] = []
        for user in all_users:
            usersQuery: List[UsersUserXtrCounters] = await bp.api.users.get(user)
            users.append(usersQuery[0])
        return users
    else:
        return await bp.api.users.get(message.from_id)


@bp.on.message(regexp=[
    r"(?i).*(обним|обнял|обнять).*(чарли|слайма|все|all|онлайн|\[id).*",
    r"(?i).*(чарли|слайм).*обними.*"
])
async def hug_command(message: Message, match: Tuple) -> None:
    if re.findall(r"all|все|онлайн", message.text):
        await message.answer(await string_with_everyone("localization/choices/hug.txt"))
    else:
        users: List[UsersUserXtrCounters] = await extract_users(message)
        await message.answer(await string_with_user(
            "localization/choiceswnames/hug.txt",
            users[0]
        ))


@bp.on.message(regexp=[
    r"(?i).*(поцеловать|целую|чмок).*(чарли|слайма|\[id).*",
    r"(?i).*(чарли|слайм).*поцелуй.*(меня|\[id)"
])
async def kiss_command(message: Message, match: Tuple) -> None:
    users: List[UsersUserXtrCounters] = await extract_users(message)
    localization_file: str = ""
    if re.findall(r"\[id", message.text):
        localization_file = "localization/choiceswnames/kiss_someone.txt"
    else:
        localization_file = "localization/choices/kiss_to.txt"
    await message.answer(await string_with_user(localization_file, users[0]))


@bp.on.message(regexp=[
    r"(?i).*(погладить|глажу).*(чарли|слайма|\[id).*",
    r"(?i).*(чарли|слайм).*гладь.*(меня|\[id).*"
])
async def pet_command(message: Message, match: Tuple) -> None:
    users: List[UsersUserXtrCounters] = await extract_users(message)
    localization_file: str = ""
    if re.findall(r"\[id", message.text):
        localization_file = "localization/choiceswnames/pet_someone.txt"
    else:
        localization_file = "localization/choices/pet_to.txt"
    await message.answer(await string_with_user(localization_file, users[0]))
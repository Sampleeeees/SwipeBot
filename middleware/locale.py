from datetime import datetime

from aiogram import BaseMiddleware
from aiogram.utils.i18n.middleware import I18nMiddleware
from aiogram.types import TelegramObject, User, CallbackQuery
from typing import Optional, cast
from typing import Dict, Any
from database.database import get_info_user, set_language_user_db
from config.config import redis
from typing import Any, Awaitable, Callable, Dict, Optional, Set, cast


class Localization(I18nMiddleware):

    async def get_user_language(self, user_id):
        user = get_info_user(user_id=user_id)
        if user:
            return user
        return None

    async def set_user_language(self, user_id, language):
        await set_language_user_db(user_id, language)

    async def get_locale(self, event: TelegramObject, data: Dict[str, Any]) -> str:
        message_dict = event.dict()
        user_id = message_dict['from_user']['id']
        user_language = await self.get_user_language(user_id)

        if user_language:
            return user_language

        return self.i18n.default_locale
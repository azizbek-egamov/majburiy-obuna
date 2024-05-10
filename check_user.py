from aiogram import BaseMiddleware
from aiogram.types import InlineKeyboardButton, Update
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import bot

DEFAULT_RATE_LIMIT = .1
kanallar = [-1001950814051, -1001835995666]

class User_checkMiddleware(BaseMiddleware):
    def __init__(self, limit=DEFAULT_RATE_LIMIT, key_prefix='antiflood_'):
        self.rate_limit = limit
        self.prefix = key_prefix
        super(User_checkMiddleware, self).__init__()

    async def __call__(self, handler, event: Update, data):
        if event.message:
            user_id = event.message.from_user.id
        elif event.callback_query:
            user_id = event.callback_query.from_user.id
        k = []
        force = False
        for x in kanallar:
            kanals = await bot.get_chat(x)
            try:
                res = await bot.get_chat_member(chat_id=x, user_id=user_id)
            except:
                continue
            if res.status == 'member' or res.status == 'administrator' or res.status == 'creator':
                pass
            else:
                k.append(InlineKeyboardButton(text=f"{kanals.title}", url=f"{await kanals.export_invite_link()}"))
                force = True
        builder = InlineKeyboardBuilder()
        builder.add(*k)
        text = "Tasdiqlash"
        builder.add(InlineKeyboardButton(text=text, callback_data="check"))
        builder.adjust(1)
        if force:
            await bot.send_message(chat_id=user_id, text="Bot to'liq ishlashi uchun kanallarga obuna bo'ling!", reply_markup=builder.as_markup())
        else:
            return await handler(event, data)


from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from bot import bot, dp
from configurebot import cfg
from aiogram.dispatcher.filters.state import State, StatesGroup

class FSMQuestion(StatesGroup):
    text = State()


tehchatid = cfg['teh_chat_id']
message_seneded = cfg['question_ur_question_sended_message']

class FSMQuestion(StatesGroup):
    text = State()

async def newquestion(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            if message.content_type == 'photo':
                data['text'] = message.caption or "Фото без подписи"
            else:
                data['text'] = message.text or "Сообщение без текста"

        await state.finish()

        who = f"@{message.chat.username}" if message.chat.username else "Ник не установлен"
        question = data['text']

        if message.content_type == 'photo':
            photo_id = message.photo[-1].file_id
            await message.reply(message_seneded, parse_mode='Markdown')
            await bot.send_photo(
                chat_id=tehchatid,
                photo=photo_id,
                caption=f"✉ | Новый вопрос\nОт: {who}\nВопрос: `{question}`\n\n📝 Чтобы ответить на вопрос, введите `/ответ {message.chat.id} Ваш ответ`",
                parse_mode='Markdown'
            )
        else:
            await message.reply(message_seneded, parse_mode='Markdown')
            await bot.send_message(
                chat_id=tehchatid,
                text=f"✉ | Новый вопрос\nОт: {who}\nВопрос: `{question}`\n\n📝 Чтобы ответить на вопрос, введите `/ответ {message.chat.id} Ваш ответ`",
                parse_mode='Markdown'
            )
    except Exception as e:
        cid = message.chat.id
        await bot.send_message(tehchatid, f"Случилась ошибка в чате {cid}\nСтатус ошибки: `{e}`", parse_mode='Markdown')
        print(f"Error: {e}")

def register_handler_FSM():
    dp.register_message_handler(newquestion, state=FSMQuestion.text, content_types=['photo', 'text'])


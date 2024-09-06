from aiogram import types
import kb
from bot import dp, bot
from handlers.db import db_profile_exist, db_profile_insertone, db_profile_banned
from configurebot import cfg
from handlers.fsm import FSMQuestion
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


welcomemessage = cfg['welcome_message']
errormessage = cfg['error_message']
devid = cfg['dev_id']
aboutus = cfg['about_us']
question_first_msg = cfg['question_type_ur_question_message']
faq = cfg['question_faq']

handler_button_new_question = cfg['button_new_question']
handler_button_about_us = cfg['button_about_us']
handler_button_faq = cfg['button_faq']

async def client_start(message: types.Message):
    try:
        if message.chat.type != 'private':
            await message.answer('Данную команду можно использовать только в личных сообщениях с ботом.')
            return
        if db_profile_exist(message.from_user.id):
            await message.answer(f'{welcomemessage}', parse_mode='Markdown', reply_markup=kb.mainmenu)
        else:
            db_profile_insertone(message.from_user.id, message.from_user.username, 0, 0)
            print('Новый пользователь!')
            await message.answer(f'{welcomemessage}', parse_mode='Markdown', reply_markup=kb.mainmenu)
    except Exception as e:
        cid = message.chat.id
        await message.answer(f"{errormessage}", parse_mode='Markdown')
        await bot.send_message(devid, f"Случилась *ошибка* в чате *{cid}*\nСтатус ошибки: `{e}`", parse_mode='Markdown')

async def client_newquestion(message: types.Message):
    try:
        if message.text == handler_button_new_question:
            if db_profile_banned(message.from_user.id):
                await message.answer("⚠ Вы *заблокированы* в боте!", parse_mode='Markdown')
                return
            await message.answer(f"{question_first_msg}")
            await FSMQuestion.text.set()
        elif message.text == handler_button_about_us:
            if db_profile_banned(message.from_user.id):
                await message.answer("⚠ Вы *заблокированы* в боте!", parse_mode='Markdown')
                return
            await message.answer(f"{aboutus}", disable_web_page_preview=True, parse_mode='Markdown')
        elif message.text == handler_button_faq:
            if db_profile_banned(message.from_user.id):
                await message.answer("⚠ Вы *заблокированы* в боте!", parse_mode='Markdown')
                return
            markup = InlineKeyboardMarkup()
            button1 = InlineKeyboardButton(text='Вопрос 1', callback_data="butt_id_1")
            button2 = InlineKeyboardButton(text='Вопрос 2', callback_data="butt_id_2")
            markup.add(button1, button2)
            await bot.send_message(message.chat.id, f"{faq}", reply_markup=markup)
            @dp.callback_query_handler(lambda c: c.data == "butt_id_1")
            async def to_query(call: types.callback_query):
                await bot.answer_callback_query(call.id)
                await bot.send_message(call.message.chat.id, "Ответ на вопрос 1")
            @dp.callback_query_handler(lambda c: c.data == "butt_id_2")
            async def to_query2(call: types.CallbackQuery):
                await bot.answer_callback_query(call.id)
                await bot.send_message(call.message.chat.id, "Ответ на вопрос 2")


    except Exception as e:
        cid = message.chat.id
        await message.answer(f"{errormessage}", parse_mode='Markdown')
        await bot.send_message(devid, f"Случилась *ошибка* в чате *{cid}*\nСтатус ошибки: `{e}`", parse_mode='Markdown')

async def client_getgroupid(message: types.Message):
    try:
        await message.answer(f"Chat id is: *{message.chat.id}*\nYour id is: *{message.from_user.id}*", parse_mode='Markdown')
    except Exception as e:
        cid = message.chat.id
        await message.answer(f"{errormessage}", parse_mode='Markdown')
        await bot.send_message(devid, f"Случилась *ошибка* в чате *{cid}*\nСтатус ошибки: `{e}`", parse_mode='Markdown')

def register_handler_client():
    dp.register_message_handler(client_start, commands='start', state=None)
    dp.register_message_handler(client_getgroupid, commands='getchatid')
    dp.register_message_handler(client_newquestion)

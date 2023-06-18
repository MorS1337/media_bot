import asyncio
import logging
from emoji import emojize

from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.types.message import ContentType
from aiogram.utils.markdown import text, bold, italic, code, pre
from aiogram.types import ParseMode, InputMediaPhoto, InputMediaVideo, ChatActions

from cfg import TOKEN

logging.basicConfig(format=u'%(filename)s [ LINE:%(lineno)+3s ]#%(levelname)+8s [%(asctime)s]  %(message)s',
                    level=logging.INFO)

CAT_BIG_EYES = "AgACAgIAAxkDAANBZEWIU3jzPspuL9yZV5YSRu88MuQAAivKMRtbTTFKez4TuQV57FMBAAMCAANtAAMvBA"
IMAGES = [
    'AgACAgIAAxkDAAMlZEV8ylt2q-lrZ4OO6RBJbJJjtkwAAqLJMRtbTTFKRakBwFq_Y4ABAAMCAAN4AAMvBA',
    'AgACAgIAAxkDAAMmZEV8ykb1AAEkVmTAJ4zsC-V-NcZsAAKjyTEbW00xSsROsElCSnsqAQADAgADeQADLwQ',
    'AgACAgIAAxkDAAMrZEWDMMafGOzu_l8Juudp7LtYwrYAAqHJMRtbTTFKv-DQScW4J74BAAMCAAN3AAMvBA',
]
VOICE = 'AwACAgIAAxkDAAMpZEWDL7wp-qD1KVMlf1hAnxQZ4ncAAikrAAJbTTFKom88pv_SlFQvBA'
VIDEO = 'BAACAgIAAxkDAAMnZEV8yzsQsqJ7fTPCJTCKptFvwC8AAvIqAAJbTTFKYGnjzem_SMYvBA'
TEXT_FILE = 'BQACAgIAAxkDAANvZEa8QYqasMIg9qZSGCLJ2XHYVVgAApovAAIO_TFKIgjbpE7TmWEvBA'
VIDEO_NOTE = 'DQACAgIAAxkDAAMqZEWDL3BZaJX-WWgJrywj9sn3DW8AAiorAAJbTTFKVDHTzOWvGmovBA'
IMAGE_LINK = 'https://cdn.discordapp.com/attachments/1097954893735665816/1098317963507015761/IMG-20220830-WA0000.jpg'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def process_start_command(message: types.Message):
    await message.reply('Привет!\nИспользуй команду /help,'\
                        'чтобы узнать узнать список доступных комманд')
    
    
@dp.message_handler(commands=["help"])
async def process_help_command(message: types.Message):
    msg = text(bold('Я могу ответить на следующие команды'),
                    '/voice', '/photo', '/group', '/note', 
                    '/file', '/testpre', '/geo', '/video', 
                    '/music', '/photobylink', sep='\n')
    await message.reply(msg, parse_mode=ParseMode.MARKDOWN)
    
@dp.message_handler(commands=["voice"])
async def process_voice_command(message: types.Message):
    await bot.send_voice(message.from_user.id, VOICE, 
                         reply_to_message_id=message.message_id)
    
@dp.message_handler(commands=['photo'])
async def process_photo_command(message: types.Message):
    caption = 'Какие глазки! :eyes:'
    await bot.send_photo(message.from_user.id, CAT_BIG_EYES,
                         caption=emojize(caption),
                         reply_to_message_id=message.message_id)
    
@dp.message_handler(commands=['group'])
async def process_group_command(message: types.Message):
    media = [InputMediaVideo(VIDEO, 'кто это блять')]
    for photo_id in IMAGES:
        media.append(InputMediaPhoto(photo_id))
    await bot.send_media_group(message.from_user.id, media)
        
@dp.message_handler(commands=['note'])
async def process_note_command(message: types.Message):
    user_id = message.from_user.id
    await bot.send_chat_action(user_id, ChatActions.RECORD_VIDEO_NOTE)
    await asyncio.sleep(1)  # конвертируем видео и отправляем его пользователю
    await bot.send_video_note(message.from_user.id, VIDEO_NOTE)
    
@dp.message_handler(commands=["file"])
async def process_file_command(message: types.Message):
    user_id = message.from_user.id
    await bot.send_chat_action(user_id, ChatActions.UPLOAD_DOCUMENT)
    await asyncio.sleep(1)
    await bot.send_document(user_id, TEXT_FILE,
                            caption="Это специально для тебя!")
    
@dp.message_handler(commands=['testpre'])
async def process_testpre_command(message: types.Message):
    message_text = pre(emojize('''@dp.message_handler(commands=['testpre'])
async def process_testpre_command(message: types.Message):
    message_text = pre(emojize('Ха! Не в этот раз :smirk:'))
    await bot.send_message(message.from_user.id, message_text)'''))
    await bot.send_message(message.from_user.id, message_text,
                           parse_mode=ParseMode.MARKDOWN)
    
@dp.message_handler(commands=["geo"])
async def process_geo_command(message: types.Message):
    user_id = message.from_user.id
    await bot.send_location(user_id, 
                            45.393925,
                            -101.757789,)
    
@dp.message_handler(commands=["video"])
async def process_video_command(message: types.Message):
    user_id = message.from_user.id
    await bot.send_video(user_id, VIDEO, reply_to_message_id=message.message_id)
    
@dp.message_handler(commands=["music"])
async def process_geo_command(message: types.Message):
    user_id = message.from_user.id
    await bot.send_message(user_id, 'This function is under maintenance')
    

@dp.message_handler(commands=["photobylink"])
async def process_photobylink_command(message: types.Message):
    user_id = message.from_user.id
    await bot.send_photo(user_id, IMAGE_LINK)
  
@dp.message_handler()
async def echo(message: types.Message):
    await bot.send_message(message.from_user.id, message.text)
    
@dp.message_handler(content_types=ContentType.ANY)
async def unknown_message(msg: types.Message):
    message_text = text(emojize('Я не знаю, что с этим делать :backpack:'),
                        italic('\nЯ просто напомню,'), 'что есть',
                        code('команда'), '/help')
    await msg.reply(message_text, parse_mode=ParseMode.MARKDOWN)


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp)
    
import os
import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import CommandHandler, CallbackQueryHandler, MessageHandler, Filters, Updater
from audio import handle_audio_file
from image import handle_image_file
from text import handle_text_file
from video import handle_video_file
from rar import handle_rar_file
from zip import handle_zip_file
from torrent import handle_torrent_file

TOKEN = "7457408733:AAFMHva49ZnlHIok_HQoT08krevNiwos3lQ"

def start(update: Update, context):
    bot_info = context.bot.get_me()  # Get bot info
    bot_name = bot_info.first_name  # Get the bot's first name

    start_command = (
        f"Welcome to {bot_name}. This is a 𝗳𝗶𝗹𝗲 𝗰𝗼𝗻𝘃𝗲𝗿𝘀𝗶𝗼𝗻 𝗯𝗼𝘁 that converts files from different formats to your desired format 👾\n\n"
        "𝗦𝘂𝗽𝗽𝗼𝗿𝘁𝗲𝗱 𝗳𝗼𝗿𝗺𝗮𝘁𝘀 𝗶𝗻𝗰𝗹𝘂𝗱𝗲:\n"
        "- 𝗜𝗺𝗮𝗴𝗲𝘀: JPEG, PNG, GIF, BMP, and more.\n"
        "- 𝗔𝘂𝗱𝗶𝗼: MP3, WAV, AAC, FLAC, and more.\n"
        "- 𝗩𝗶𝗱𝗲𝗼: MP4, AVI, MKV, MOV, and more.\n"
        "- 𝗗𝗼𝗰𝘂𝗺𝗲𝗻𝘁𝘀: PDF, DOCX, TXT, and more.\n\n"
        "To get started, simply send me the file you want to convert, followed by the format you wish to convert it to. I am here to help you with all your conversion needs!"
    )

    image_link = "https://i.imghippo.com/files/892kR1727928004.jpg"

    inline_buttons = [
        [InlineKeyboardButton("𝗝𝗼𝗶𝗻 𝗖𝗵𝗮𝗻𝗻𝗲𝗹", url="https://t.me/AlcyoneBots")],
        [InlineKeyboardButton("𝗝𝗼𝗶𝗻 𝗦𝘂𝗽𝗽𝗼𝗿𝘁", url="https://t.me/Alcyone_support")]
    ]

    # Send the welcome message with the image and inline buttons
    update.message.reply_photo(photo=image_link, caption=start_command, reply_markup=InlineKeyboardMarkup(inline_buttons))

def create_conversion_keyboard():
    keyboard = [
        [InlineKeyboardButton("Image Conversion", callback_data='convert_image')],
        [InlineKeyboardButton("Audio Conversion", callback_data='convert_audio')],
        [InlineKeyboardButton("Text to PDF", callback_data='convert_text')],
        [InlineKeyboardButton("Video Conversion", callback_data='convert_video')],
        [InlineKeyboardButton("RAR Extraction", callback_data='extract_rar')],
        [InlineKeyboardButton("ZIP Extraction", callback_data='extract_zip')],
        [InlineKeyboardButton("Torrent Conversion", callback_data='convert_torrent')],
    ]
    return InlineKeyboardMarkup(keyboard)

def handle_file(update: Update, context):
    conversion_type = context.user_data.get('conversion_type')

    if conversion_type == 'convert_image':
        handle_image_file(update, context)
    elif conversion_type == 'convert_audio':
        handle_audio_file(update, context)
    elif conversion_type == 'convert_text':
        handle_text_file(update, context)
    elif conversion_type == 'convert_video':
        handle_video_file(update, context)
    elif conversion_type == 'extract_rar':
        handle_rar_file(update, context)
    elif conversion_type == 'extract_zip':
        handle_zip_file(update, context)
    elif conversion_type == 'convert_torrent':
        handle_torrent_file(update, context)

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(handle_file, pattern='^(convert_image|convert_audio|convert_text|convert_video|extract_rar|extract_zip|convert_torrent)$'))
    dp.add_handler(MessageHandler(Filters.document, handle_file))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

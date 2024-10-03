import os
import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, MessageHandler, Filters, Updater
from audio import handle_audio_file
from image import handle_image_file
from text import handle_text_file
from video import handle_video_file
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

def convert(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("Image Conversion", callback_data='convert_image')],
        [InlineKeyboardButton("Audio Conversion", callback_data='convert_audio')],
        [InlineKeyboardButton("Text to PDF", callback_data='convert_text')],
        [InlineKeyboardButton("Video Conversion", callback_data='convert_video')],
        [InlineKeyboardButton("ZIP Extraction", callback_data='extract_zip')],
        [InlineKeyboardButton("Torrent Conversion", callback_data='convert_torrent')],
    ]
    update.message.reply_text("Please choose the conversion type:", reply_markup=InlineKeyboardMarkup(keyboard))

def button_callback(update: Update, context):
    query = update.callback_query
    query.answer()  # Acknowledge the callback to avoid issues

    # Set the conversion type in user_data for later use
    conversion_type = query.data
    context.user_data['conversion_type'] = conversion_type

    # Notify user that the bot is waiting for a file
    query.edit_message_text(f"You selected {conversion_type.replace('_', ' ').capitalize()}. Please upload the file for conversion.")

def handle_file(update: Update, context):
    # Retrieve the conversion type set by the inline button
    conversion_type = context.user_data.get('conversion_type')

    if not conversion_type:
        update.message.reply_text("Please choose a conversion type using the /convert command before sending a file.")
        return

    # Log the conversion type for debugging
    print(f"Received file for conversion: {conversion_type}")

    # Process the file based on the conversion type
    try:
        if conversion_type == 'convert_image':
            handle_image_file(update, context)
        elif conversion_type == 'convert_audio':
            handle_audio_file(update, context)
        elif conversion_type == 'convert_text':
            handle_text_file(update, context)
        elif conversion_type == 'convert_video':
            handle_video_file(update, context)
        elif conversion_type == 'extract_zip':
            handle_zip_file(update, context)
        elif conversion_type == 'convert_torrent':
            handle_torrent_file(update, context)
        else:
            update.message.reply_text("Invalid conversion type selected.")
    except Exception as e:
        update.message.reply_text(f"An error occurred during conversion: {str(e)}")
        print(f"Error during conversion: {str(e)}")  # Log the error for debugging

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    # Command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("convert", convert))

    # Callback query handler for inline buttons
    dp.add_handler(CallbackQueryHandler(button_callback))

    # Message handler for file uploads
    dp.add_handler(MessageHandler(Filters.document, handle_file))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

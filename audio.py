import io
from telegram import Update
from pydub import AudioSegment
from telegram.ext import CallbackContext

def handle_audio_file(update: Update, context: CallbackContext):
    file = update.message.document
    file.download(file.file_name)
    context.user_data['file_path'] = file.file_name

    # Show inline keyboard for audio format selection
    keyboard = [
        [InlineKeyboardButton("Convert to WAV", callback_data='convert_to_wav')],
        [InlineKeyboardButton("Convert to MP3", callback_data='convert_to_mp3')],
        [InlineKeyboardButton("Convert to OGG", callback_data='convert_to_ogg')],
    ]
    update.message.reply_text("Select the format to convert:", reply_markup=InlineKeyboardMarkup(keyboard))

def convert_audio(file_path, output_format):
    audio = AudioSegment.from_file(file_path)
    output = io.BytesIO()

    if output_format == 'convert_to_wav':
        audio.export(output, format="wav")
    elif output_format == 'convert_to_mp3':
        audio.export(output, format="mp3")
    elif output_format == 'convert_to_ogg':
        audio.export(output, format="ogg")

    output.seek(0)
    return output

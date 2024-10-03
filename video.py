import io
from telegram import Update
from moviepy.editor import VideoFileClip
from telegram.ext import CallbackContext

def handle_video_file(update: Update, context: CallbackContext):
    file = update.message.document
    file.download(file.file_name)
    context.user_data['file_path'] = file.file_name

    # Show inline keyboard for video format selection
    keyboard = [
        [InlineKeyboardButton("Convert to MP4", callback_data='convert_to_mp4')],
        [InlineKeyboardButton("Convert to AVI", callback_data='convert_to_avi')],
        [InlineKeyboardButton("Convert to MKV", callback_data='convert_to_mkv')],
    ]
    update.message.reply_text("Select the format to convert:", reply_markup=InlineKeyboardMarkup(keyboard))

def convert_video(file_path, output_format):
    video = VideoFileClip(file_path)
    output = io.BytesIO()

    if output_format == 'convert_to_mp4':
        video.write_videofile(output, codec='libx264', fps=24)
    elif output_format == 'convert_to_avi':
        video.write_videofile(output, codec='rawvideo', fps=24)
    elif output_format == 'convert_to_mkv':
        video.write_videofile(output, codec='libx264', fps=24)

    output.seek(0)
    return output

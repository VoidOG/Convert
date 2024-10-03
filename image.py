import io
from telegram import Update
from PIL import Image
from telegram.ext import CallbackContext

def handle_image_file(update: Update, context: CallbackContext):
    file = update.message.document
    file.download(file.file_name)
    context.user_data['file_path'] = file.file_name

    # Show inline keyboard for image format selection
    keyboard = [
        [InlineKeyboardButton("Convert to JPG", callback_data='convert_to_jpg')],
        [InlineKeyboardButton("Convert to PNG", callback_data='convert_to_png')],
        [InlineKeyboardButton("Convert to BMP", callback_data='convert_to_bmp')],
        [InlineKeyboardButton("Convert to GIF", callback_data='convert_to_gif')],
        [InlineKeyboardButton("Convert to WEBP", callback_data='convert_to_webp')],
    ]
    update.message.reply_text("Select the format to convert:", reply_markup=InlineKeyboardMarkup(keyboard))

def convert_image(file_path, output_format):
    image = Image.open(file_path)
    output = io.BytesIO()

    if output_format == 'convert_to_jpg':
        image.convert("RGB").save(output, format="JPEG")
    elif output_format == 'convert_to_png':
        image.save(output, format="PNG")
    elif output_format == 'convert_to_bmp':
        image.save(output, format="BMP")
    elif output_format == 'convert_to_gif':
        image.save(output, format="GIF")
    elif output_format == 'convert_to_webp':
        image.save(output, format="WEBP")
    
    output.seek(0)
    return output

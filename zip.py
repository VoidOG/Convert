import io
import zipfile
from telegram import Update
from telegram.ext import CallbackContext

def handle_zip_file(update: Update, context: CallbackContext):
    file = update.message.document
    file.download(file.file_name)
    context.user_data['file_path'] = file.file_name

    extracted_files = extract_zip(context.user_data['file_path'])
    for name, content in extracted_files:
        update.message.reply_document(content, filename=name)

def extract_zip(file_path):
    extracted_files = []
    with zipfile.ZipFile(file_path, 'r') as zf:
      for name in zf.namelist():
            with zf.open(name) as file:
                extracted_content = io.BytesIO(file.read())
                extracted_files.append((name, extracted_content))
    return extracted_files

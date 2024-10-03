import io
import rarfile
from telegram import Update
from telegram.ext import CallbackContext

def handle_rar_file(update: Update, context: CallbackContext):
    file = update.message.document
    file.download(file.file_name)
    context.user_data['file_path'] = file.file_name

    extracted_files = extract_rar(context.user_data['file_path'])
    for name, content in extracted_files:
        update.message.reply_document(content, filename=name)

def extract_rar(file_path):
    extracted_files = []
    with rarfile.RarFile(file_path) as rf:
        for name in rf.namelist():
            extracted_content = io.BytesIO(rf.read(name))
            extracted_files.append((name, extracted_content))
    return extracted_files

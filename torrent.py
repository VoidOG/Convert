import os
import io
import libtorrent as lt
from telegram import Update
from telegram.ext import CallbackContext

def handle_torrent_file(update: Update, context: CallbackContext):
    file = update.message.document
    file.download(file.file_name)
    context.user_data['file_path'] = file.file_name

    # Start torrent download
    torrent_file_path = context.user_data['file_path']
    download_torrent(torrent_file_path, update)

def download_torrent(torrent_file_path, update: Update):
    ses = lt.session()
    info = lt.torrent_info(torrent_file_path)
    h = ses.add_torrent({'ti': info, 'save_path': './'})

    # Start downloading the torrent
    while not h.is_seed():
        s = h.status()
        update.message.reply_text(f'Downloading: {s.progress * 100:.2f}% complete')
        time.sleep(1)

    # Once the torrent is downloaded, send the files to the user
    for file in info.files():
        file_path = os.path.join('./', file.path)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                output = io.BytesIO(f.read())
                update.message.reply_document(output, filename=file.path)

    update.message.reply_text("Download complete!")

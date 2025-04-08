from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import Update
import pytesseract
from PIL import Image
import requests
import io

import logging
logging.basicConfig(level=logging.INFO)

TOKEN = "YOUR_BOT_TOKEN"
user_states = {}

def start(update: Update, context):
    update.message.reply_text("Send your payment screenshot...")

def handle_photo(update: Update, context):
    user_id = update.message.from_user.id
    photo_file = update.message.photo[-1].get_file()
    photo_bytes = photo_file.download_as_bytearray()

    image = Image.open(io.BytesIO(photo_bytes))
    text = pytesseract.image_to_string(image)

    logging.info(f"OCR Output from {user_id}: {text}")

    amount = 0
    if "100" in text or "₹100" in text:
        amount

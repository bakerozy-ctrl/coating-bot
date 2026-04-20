import os
from datetime import datetime
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Load ENV
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
SPREADSHEET_NAME = os.getenv("SPREADSHEET_NAME")

# Google Sheets setup
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

sheet_blast = client.open(SPREADSHEET_NAME).worksheet("BLASTING")

# Helper
def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def today():
    return datetime.now().strftime("%Y-%m-%d")

# Command /blast
async def blast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text.replace("/blast ", "")
        parts = [p.strip() for p in text.split("|")]

        asset, rsw, system, s1, s2, p1, p2 = parts

        sheet_blast.append_row([
            now(), today(), asset, rsw, system,
            s1, s2, p1, p2, "OK",
            update.effective_user.first_name,
            datetime.now().strftime("%H:%M")
        ])

        await update.message.reply_text("✅ BLASTING saved")

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

# Main
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("blast", blast))

print("🚀 Bot Running...")
app.run_polling()

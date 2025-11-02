import json
import os
from telegram import Update, User
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# የተጠቃሚዎች ዝርዝር ለማከማቻ (በ RAM ውስጥ ወይም በፋይል)
users_db = {}  # {user_id: {"name": "Ali", "username": "ali_user"}}
DB_FILE = "users.json"

# የ DB ፋይል ከተቀመጠ ያንሱ
if os.path.exists(DB_FILE):
    with open(DB_FILE, "r") as f:
        users_db = json.load(f)

def save_db():
    with open(DB_FILE, "w") as f:
        json.dump(users_db, f)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user: User = update.effective_user
    await update.message.reply_text(
        "ሰላም! እባክህ ስምህን ይላክ (ለምሳሌ: Ali)"
    )
    # የተጠቃሚውን መለያ ማስቀመጥ (ለአሁን ስም ያስገቡ)
    context.user_data["awaiting_name"] = True

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user: User = update.effective_user
    text = update.message.text.strip()

    # ስም ሲጠየቅ
    if context.user_data.get("awaiting_name"):
        name = text
        username = user.username or f"user_{user.id}"
        users_db[str(user.id)] = {
            "name": name,
            "username": username,
            "id": user.id
        }
        save_db()
        context.user_data["awaiting_name"] = False
        await update.message.reply_text(
            f"እንኳን ደስ አለህ {name}! አሁን ሌላ ሰው ስም ሲፃፍ አታውን እንልከው!"
        )
        return

    # ሌላ ሰው ስም ሲፈለግ
    name_to_find = text
    found = []
    for uid, data in users_db.items():
        if data["name"].lower() == name_to_find.lower():
            found.append(data)
    
    if found:
        user_info = found[0]
        display_name = user_info["name"]
        username = user_info["username"]
        if username.startswith("user_"):
            reply = f"👤 {display_name} አታውን ነው: [የተጠቃሚ መለያ የለም] (ID: {user_info['id']})"
        else:
            reply = f"👤 {display_name} አታውን ነው: @{username}"
        await update.message.reply_text(reply)
    else:
        await update.message.reply_text("❌ ይህ ስም የተመዘገበ አይደለም!")

def main():
    TELEGRAM_TOKEN = "8521872647:AAHwWhKioDdmxTTgzOSSJTAl-S8kDXN5AyA"  # ይቀይሩ!
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("✅ የተጠቃሚ የምዝገባ ቦት እየሰራ ነው...")
    app.run_polling()

if __name__ == "__main__":
    main()

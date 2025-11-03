import json
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

DB_FILE = "users.json"
users_db = {}

if os.path.exists(DB_FILE):
try:
with open(DB_FILE, "r", encoding="utf-8") as f:
users_db = json.load(f)
except:
users_db = {}

def save_db():
with open(DB_FILE, "w", encoding="utf-8") as f:
json.dump(users_db, f, ensure_ascii=False, indent=2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
await update.message.reply_text("ሰላም! 😊\nእባክህ ስምህን ይላክ (ለምሳሌ: አሊ)")
context.user_data["awaiting_name"] = True

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
text = update.message.text.strip()
user = update.effective_user

if context.user_data.get("awaiting_name"):  
    if text:  
        name = text  
        username = user.username or f"user_{user.id}"  
        users_db[str(user.id)] = {  
            "name": name,  
            "username": username,  
            "id": user.id  
        }  
        save_db()  
        context.user_data["awaiting_name"] = False  
        await update.message.reply_text(f"እንኳን ደስ አለህ፣ {name}! 🎉\nአሁን ሌላ ሰው ስም ሲፃፍ፣ አታውን እንልከው!")  
    else:  
        await update.message.reply_text("ስምህን እባክህ ይፃፍ!")  
    return  

# ሌላ ሰው ስም ሲፈለግ  
for data in users_db.values():  
    if data["name"].lower() == text.lower():  
        if data["username"].startswith("user_"):  
            reply = f"👤 {data['name']} አታውን ነው: [የቴሌግራም መለያ የለም] (ID: {data['id']})"  
        else:  
            reply = f"👤 {data['name']} አታውን ነው: @{data['username']}"  
        await update.message.reply_text(reply)  
        return  
await update.message.reply_text("❌ ይህ ስም የተመዘገበ አይደለም!")

def main():
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
print("❌ የቴሌግራም ቶክን ያስገቡ! (TELEGRAM_BOT_TOKEN)")
return
app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
print("✅ የተጠቃሚ ዝርዝር ቦት እየሰራ ነው...")
app.run_polling()

if name == "main":
main()
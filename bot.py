import os
import telebot
import google.generativeai as genai

# আপনার টেলিগ্রাম বটের টোকেন এবং এডমিন আইডি
TELEGRAM_TOKEN = '8835942040:AAGn7nbMH8-4sizglx954OPV93tCSNpcesI'
ADMIN_ID = 8357226129
GEMINI_API_KEY = "AQ.Ab8RN6JLhA5uE_duODuWrbUJ22i3-GQYjdPlWRL7LyLSCY1CGA"

bot = telebot.TeleBot(TELEGRAM_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "আসসালামু আলাইকুম! আপনাকে কীভাবে সাহায্য করতে পারি?")

@bot.message_handler(func=lambda message: message.from_user.id != ADMIN_ID and message.chat.type == 'private')
def handle_customer(message):
    user_id = message.chat.id
    username = message.from_user.first_name
    text = message.text

    # এডমিন ইনবক্সে নোটিফিকেশন পাঠানো
    try:
        notification = (
            f"📩 **নতুন কাস্টমার মেসেজ!**\n\n"
            f"👤 নাম: {username}\n"
            f"🆔 ইউজার আইডি: `{user_id}`\n"
            f"💬 মেসেজ: {text}"
        )
        bot.send_message(ADMIN_ID, notification, parse_com="Markdown")
    except Exception as e:
        print(f"Notification Error: {e}")

    # জেমিনি এআই রেসপন্স
    prompt = f"""
    You are a professional and smart AI customer support assistant for a Gmail buying and selling shop. 
    You must reply in the exact language the user writes in (Bengali or English).

    Here are our official shop rates (only mention these rates if the user asks about prices, buying, selling, or rates):
    1. Buying Rates (When customers buy from us):
       - Old Gmail: 45 BDT / $0.40
       - Fresh Gmail: 30 BDT / $0.25
       - Phone Verified (PVA) Gmail: 40 BDT / $0.35

    2. Selling Rates (When we buy from customers/customers sell to us):
       - Old Gmail: 35 BDT / $0.30
       - Phone Verified (PVA) Gmail: 30 BDT / $0.25
       - Fresh Gmail: 22 BDT / $0.22

    Guidelines:
    - If the user greets you or asks casual questions, reply naturally and politely without showing the price list.
    - If the user asks about Gmail accounts, prices, buying, or selling, provide the correct rates.
    
    User message: {text}
    """
    
    try:
        response = model.generate_content(prompt)
        bot.reply_to(message, response.text)
    except Exception:
        bot.reply_to(message, "ওয়ালাইকুম আসসালাম! বলুন, জিমেইল সংক্রান্ত কী জানতে চান?")

bot.infinity_polling()

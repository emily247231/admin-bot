import os
import telebot
import google.generativeai as genai

# আপনার টেলিগ্রাম বটের টোকেন, এডমিন আইডি এবং জেমিনি এআই কি
TELEGRAM_TOKEN = '8835942040:AAGn7nbMH8-4sizglx954OPV93tCSNpcesI'
ADMIN_ID = 8357226129
GEMINI_API_KEY = "AQ.Ab8RN6JLhA5uE_duODuWrbUJ22i3-GQYjdPlWRL7LyLSCY1CGA"

bot = telebot.TeleBot(TELEGRAM_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "আসসালামু আলাইকুম! জিমেইল বাই-সেল শপে আপনাকে স্বাগতম। কীভাবে সাহায্য করতে পারি?")

# কাস্টমারের মেসেজ হ্যান্ডেল করা এবং অ্যাডমিনকে নোটিফিকেশন পাঠানো
@bot.message_handler(func=lambda message: message.from_user.id != ADMIN_ID and message.chat.type == 'private')
def handle_customer(message):
    user_id = message.chat.id
    username = message.from_user.first_name
    text = message.text

    # অ্যাডমিন ইনবক্সে কাস্টমারের মেসেজ পাঠানোর কোড
    try:
        notification = (
            f"📩 **নতুন কাস্টমার মেসেজ!**\n\n"
            f"👤 নাম: {username}\n"
            f"🆔 ইউজার আইডি: `{user_id}`\n"
            f"💬 মেসেজ: {text}"
        )
        bot.send_message(ADMIN_ID, notification, parse_mode="Markdown")
    except Exception as e:
        print(f"Notification Error: {e}")

    # জেমিনি এআই প্রম্পট ও রেট লিস্ট
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
    - If the user greets you or asks casual questions (like how are you, hi, hello), reply naturally and politely without showing the price list.
    - If the user asks about Gmail accounts, prices, buying, or selling, provide the correct rates accurately.
    
    User message: {text}
    """
    
    try:
        response = model.generate_content(prompt)
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Gemini Error: {e}")
        bot.reply_to(message, "ওয়ালাইকুম আসসালাম! বলুন, জিমেইল সংক্রান্ত কী জানতে চান?")

# অ্যাডমিন যদি কোনো মেসেজ রিলাই করে সরাসরি কাস্টমারকে পাঠাতে চায়
@bot.message_handler(func=lambda message: message.from_user.id == ADMIN_ID and message.reply_to_message is not None)
def admin_reply(message):
    try:
        replied_text = message.reply_to_message.text
        # নোটিফিকেশন থেকে ইউজার আইডি বের করা
        if "ইউজার আইডি:" in replied_text:
            parts = replied_text.split("ইউজার আইডি:")
            target_user_id = int(parts[1].split("\n")[0].strip().replace("`", ""))
            
            # কাস্টমারকে অ্যাডমিনের মেসেজ পাঠানো
            bot.send_message(target_user_id, f"💬 **অ্যাডমিন থেকে উত্তর:**\n\n{message.text}")
            bot.reply_to(message, "✅ মেসেজটি সফলভাবে কাস্টমারের কাছে পাঠানো হয়েছে!")
    except Exception as e:
        bot.reply_to(message, f"❌ সেন্ড করতে সমস্যা হয়েছে: {e}")

bot.infinity_polling()

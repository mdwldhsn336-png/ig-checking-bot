import telebot
import instaloader

# আপনার টেলিগ্রাম বট API টোকেন এখানে বসান
TOKEN = '8789592665:AAFX1Nlx6ArxpR3kgbTNWIerVN9V6GyeCMc'

bot = telebot.TeleBot(TOKEN)
L = instaloader.Instaloader()

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "স্বাগতম! আমাকে কোনো Instagram ইউজারনেম পাঠান, আমি সেটির পাবলিক তথ্য দেব।")

@bot.message_handler(func=lambda message: True)
def get_ig_info(message):
    username = message.text.strip()
    bot.send_message(message.chat.id, f"🔍 [{username}] এর তথ্য খোঁজা হচ্ছে...")

    try:
        profile = instaloader.Profile.from_username(L.context, username)
        
        info = (
            f"👤 ইউজারনেম: {profile.username}\n"
            f"📝 নাম: {profile.full_name}\n"
            f"ℹ️ বায়ো: {profile.biography}\n"
            f"👥 ফলোয়ার: {profile.followers}\n"
            f"🤝 ফলোয়িং: {profile.followees}\n"
            f"🔒 প্রাইভেট একাউন্ট: {'হ্যাঁ' if profile.is_private else 'না'}"
        )
        
        # প্রোফাইল পিকচারসহ তথ্য পাঠানো
        bot.send_photo(message.chat.id, profile.profile_pic_url, caption=info)
        
    except Exception as e:
        bot.send_message(message.chat.id, "❌ এরর: সঠিক ইউজারনেম দিন অথবা একাউন্টটি খুঁজে পাওয়া যায়নি।")

print("বটটি এখন সচল আছে...")
bot.infinity_polling()


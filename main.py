import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler
import pytz
from datetime import datetime

# 1. ബോട്ട് ടോക്കൺ ഇവിടെ സെറ്റ് ചെയ്യുന്നു
# സുരക്ഷാ കാരണങ്ങളാൽ ഈ ടോക്കൺ പിന്നീട് മാറ്റാൻ ശ്രദ്ധിക്കുക
TOKEN = '8456375787:AAGK1bScNtIsdHAAtk1YyvBJEcY-mnLMJTI'

# ലാംഗ്വേജ് ഡിക്ഷണറി
STRINGS = {
    'en': {
        'welcome': "Welcome to UAE Smart Sahayi! Please select your language:",
        'main_menu': "How can I help you today?",
        'visa_fine': "Visa Fine Calculator",
        'parking': "Parking SMS",
        'official_links': "Official Gov Links",
        'fine_msg': "Overstay fine is 50 AED per day. Check official links below:",
    },
    'ml': {
        'welcome': "UAE സ്മാർട്ട് സഹായിയിലേക്ക് സ്വാഗതം! നിങ്ങളുടെ ഭാഷ തിരഞ്ഞെടുക്കുക:",
        'main_menu': "ഇന്ന് ഞാൻ നിങ്ങളെ എങ്ങനെ സഹായിക്കണം?",
        'visa_fine': "വിസ ഫൈൻ കാൽക്കുലേറ്റർ",
        'parking': "പാർക്കിംഗ് SMS",
        'official_links': "ഗവൺമെന്റ് ലിങ്കുകൾ",
        'fine_msg': "വിസ കാലാവധി കഴിഞ്ഞാൽ ഒരു ദിവസത്തേക്ക് 50 AED ആണ് ഫൈൻ. താഴെ പറയുന്ന ലിങ്കുകൾ വഴി കൂടുതൽ പരിശോധിക്കാം:",
    },
    'zh': {
        'welcome': "欢迎来到阿联酋智能助手！请选择您的语言：",
        'main_menu': "今天我能为您做什么？",
        'visa_fine': "签证罚款计算器",
        'parking': "停车短信",
        'official_links': "政府官方链接",
        'fine_msg': "签证逾期罚款为每天 50 迪拉姆。请点击下方查看官方链接：",
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
        await update.message.reply_text(STRINGS['en']['welcome'], reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data.startswith('lang_'):
        lang = query.data.split('_')[1]
        context.user_data['lang'] = lang
        
        keyboard = [
            [InlineKeyboardButton(STRINGS[lang]['visa_fine'], callback_data='visa')],
            [InlineKeyboardButton(STRINGS[lang]['official_links'], callback_data='links')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(STRINGS[lang]['main_menu'], reply_markup=reply_markup)
        
    elif query.data == 'visa':
        lang = context.user_data.get('lang', 'en')
        links = [
            [InlineKeyboardButton("ICP Portal", url="https://smartservices.icp.gov.ae/")],
            [InlineKeyboardButton("GDRFA Dubai", url="https://smart.gdrfad.gov.ae/")]
        ]
        reply_markup = InlineKeyboardMarkup(links)
        await query.edit_message_text(STRINGS[lang]['fine_msg'], reply_markup=reply_markup)

if __name__ == '__main__':
    # ബോട്ട് നിർമ്മിക്കുന്നു
    application = ApplicationBuilder().token(TOKEN).build()
    
    # ഹാൻഡ്‌ലറുകൾ ചേർക്കുന്നു
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button))
    
    print("UAE Smart Sahayi Bot is running...")
    application.run_polling()

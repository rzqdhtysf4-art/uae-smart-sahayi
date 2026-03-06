import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler

# ================== DEBUG LOGGING (error കാണാൻ) ==================
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

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
        'parking_msg': "To check parking violations:\n• Send vehicle number to 7725\n• Or use RTA Dubai App",
        'links_title': "Official Government Links:",
    },
    'ml': {
        'welcome': "UAE സ്മാർട്ട് സഹായിയിലേക്ക് സ്വാഗതം! നിങ്ങളുടെ ഭാഷ തിരഞ്ഞെടുക്കുക:",
        'main_menu': "ഇന്ന് ഞാൻ നിങ്ങളെ എങ്ങനെ സഹായിക്കണം?",
        'visa_fine': "വിസ ഫൈൻ കാൽക്കുലേറ്റർ",
        'parking': "പാർക്കിംഗ് SMS / ഫൈൻ",
        'official_links': "ഗവൺമെന്റ് ഔദ്യോഗിക ലിങ്കുകൾ",
        'fine_msg': "വിസ കാലാവധി കഴിഞ്ഞാൽ ഒരു ദിവസം 50 AED ഫൈൻ.\n\nനിങ്ങളുടെ സ്റ്റാറ്റസ് ഇവിടെ ചെക്ക് ചെയ്യാം:",
        'parking_msg': "പാർക്കിംഗ് ഫൈൻ ചെക്ക് ചെയ്യാൻ:\n• വാഹന നമ്പർ 7725 ലേക്ക് അയക്കുക\n• RTA Dubai App ഉപയോഗിക്കുക",
        'links_title': "ഔദ്യോഗിക ഗവൺമെന്റ് ലിങ്കുകൾ:",
    },
    'zh': {
        'welcome': "欢迎来到阿联酋智能助手！请选择您的语言：",
        'main_menu': "今天我能为您做什么？",
        'visa_fine': "签证罚款计算器",
        'parking': "停车短信",
        'official_links': "政府官方链接",
        'fine_msg': "签证逾期罚款为每天 50 迪拉姆。\n\n请在此处检查您的状态：",
        'parking_msg': "检查停车违规：\n• 将车牌号发送至 7725\n• 或使用 RTA Dubai App",
        'links_title': "官方政府链接：",
    }
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("🚀 /start command received!")
    keyboard = [
        [InlineKeyboardButton("English 🇬🇧", callback_data='lang_en')],
        [InlineKeyboardButton("മലയാളം 🇮🇳", callback_data='lang_ml')],
        [InlineKeyboardButton("中文
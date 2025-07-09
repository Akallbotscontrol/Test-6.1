# plugins/search.py

from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from client import bot
from config import LOG_CHANNEL
from utils.script import get_spell1, get_spell2, save_user
# plugins/search.py

from utils.recent import recent_requests
from utils.helpers import save_last_query  # now this works fine

from plugins.fsub_utils import is_fsub_enabled, is_subscribed  # ✅ now from fsub_utils
from plugins.generate import search_posts
from uuid import uuid4
import math

PAGES = {}
recent_requests = {}

def paginate_results(results_list, page=1, per_page=5):
    total = len(results_list)
    total_pages = math.ceil(total / per_page)
    start = (page - 1) * per_page
    end = start + per_page
    page_results = results_list[start:end]

    return {
        "page_results": page_results,
        "total_pages": total_pages,
        "current_page": page
    }

@bot.on_message(filters.private & filters.text & ~filters.command(["start", "help"]))
async def search_handler(client, message: Message):
    user_id = message.from_user.id
    query = message.text.strip()

    save_user(user_id)
    await save_last_query(user_id, message.chat.id, query)

    if await is_fsub_enabled(message.chat.id):
        if not await is_subscribed(client, message):
            recent_requests[user_id] = SearchRequest(user_id, query, message.chat.id)
            return

    await message.reply_text(f"🔍 Searching for: `{query}`")

    spell1 = get_spell1()
    spell2 = get_spell2()
    results = await search_posts(query, spell1=spell1, spell2=spell2)

    if results:
        query_id = str(uuid4())[:8]
        pages = paginate_results(results, page=1)
        text = "\n\n".join(pages["page_results"]) + f"\n\n📄 Page 1 of {pages['total_pages']}"

        buttons = []
        if pages["total_pages"] > 1:
            buttons = [[
                InlineKeyboardButton("◀️", callback_data=f"page_{query_id}_{pages['current_page'] - 1}") if pages["current_page"] > 1 else InlineKeyboardButton("🛑", callback_data="noop"),
                InlineKeyboardButton(f"{pages['current_page']} / {pages['total_pages']}", callback_data="noop"),
                InlineKeyboardButton("▶️", callback_data=f"page_{query_id}_{pages['current_page'] + 1}")
            ]]

        await message.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)
        PAGES[query_id] = results
    else:
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔎 Check Spelling", url=f"https://www.google.com/search?q={query}")],
            [InlineKeyboardButton("🗓 Release Date", url=f"https://www.google.com/search?q={query}+release+date")],
            [InlineKeyboardButton("📩 Request Upload", callback_data=f"request_upload_{query}")]
        ])
        await message.reply_text(
            f"❗ No results found for: `{query}`\n\n"
            "Please type movie name only and check the spelling.",
            reply_markup=buttons
        )

@bot.on_callback_query(filters.regex(r"request_upload_(.+)"))
async def handle_upload_request(_, query: CallbackQuery):
    keyword = query.data.split("_", 2)[2]
    user = query.from_user

    await bot.send_message(
        LOG_CHANNEL,
        f"📥 Upload Request:\n\nFrom: [{user.first_name}](tg://user?id={user.id}) (`{user.id}`)\nQuery: `{keyword}`"
    )
    await query.answer("✅ Request sent to admin!", show_alert=True)
    await query.message.edit("📩 Your request has been sent to admin.")

@bot.on_callback_query(filters.regex(r"^page_(\w+)_(\d+)$"))
async def paginate_callback(client, query: CallbackQuery):
    query_id, page = query.matches[0].group(1), int(query.matches[0].group(2))

    if query_id not in PAGES:
        return await query.answer("⚠️ Pagination expired!", show_alert=True)

    results = PAGES[query_id]
    pages = paginate_results(results, page=page)
    text = "\n\n".join(pages["page_results"]) + f"\n\n📄 Page {page} of {pages['total_pages']}"

    buttons = []
    if pages["total_pages"] > 1:
        buttons = [[
            InlineKeyboardButton("◀️", callback_data=f"page_{query_id}_{page - 1}") if page > 1 else InlineKeyboardButton("🛑", callback_data="noop"),
            InlineKeyboardButton(f"{page} / {pages['total_pages']}", callback_data="noop"),
            InlineKeyboardButton("▶️", callback_data=f"page_{query_id}_{page + 1}") if page < pages['total_pages'] else InlineKeyboardButton("🛑", callback_data="noop")
        ]]

    await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)
    await query.answer()

class SearchRequest:
    def __init__(self, user_id, query, chat_id):
        self.user_id = user_id
        self.query = query
        self.chat_id = chat_id

    async def continue_search(self):
        spell1 = get_spell1()
        spell2 = get_spell2()
        await bot.send_message(self.user_id, f"🔍 Searching for: `{self.query}`")
        results = await search_posts(self.query, spell1=spell1, spell2=spell2)

        if results:
            query_id = str(uuid4())[:8]
            pages = paginate_results(results, page=1)
            text = "\n\n".join(pages["page_results"]) + f"\n\n📄 Page 1 of {pages['total_pages']}"

            buttons = []
            if pages["total_pages"] > 1:
                buttons = [[
                    InlineKeyboardButton("◀️", callback_data=f"page_{query_id}_{pages['current_page'] - 1}"),
                    InlineKeyboardButton(f"{pages['current_page']} / {pages['total_pages']}", callback_data="noop"),
                    InlineKeyboardButton("▶️", callback_data=f"page_{query_id}_{pages['current_page'] + 1}")
                ]]

            await bot.send_message(self.user_id, text, reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)
            PAGES[query_id] = results
        else:
            buttons = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔎 Check Spelling", url=f"https://www.google.com/search?q={self.query}")],
                [InlineKeyboardButton("🗓 Release Date", url=f"https://www.google.com/search?q={self.query}+release+date")],
                [InlineKeyboardButton("📩 Request Upload", callback_data=f"request_upload_{self.query}")]
            ])
            await bot.send_message(
                self.user_id,
                f"❗ No results found for: `{self.query}`\n\n"
                "Please type movie name only and check the spelling.",
                reply_markup=buttons
            )

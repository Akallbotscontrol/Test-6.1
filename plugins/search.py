from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from client import bot
from utils.helpers import search_posts, save_last_query, get_last_query
from utils.script import get_spell1, get_spell2, save_user
from config import LOG_CHANNEL
from uuid import uuid4
import math

# 🔁 In-memory page cache
PAGES = {}
recent_requests = {}

# 🔄 Pagination helper
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

# 🔍 Handle user search
@bot.on_message(filters.private & filters.text & ~filters.command(["start", "help"]))
async def search_handler(client, message: Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    query = message.text.strip()
    save_user(user_id)
    await save_last_query(user_id, chat_id, query)

    await message.reply_text(f"🔎 Searching for: `{query}`...")

    spell1 = get_spell1()
    spell2 = get_spell2()
    results = await search_posts(query, spell1=spell1, spell2=spell2)

    if results:
        query_id = str(uuid4())[:8]
        pages = paginate_results(results, page=1)
        text = "\n\n".join(pages["page_results"]) + f"\n\n📄 Page 1 of {pages['total_pages']}"
        buttons = []

        if pages["total_pages"] > 1:
            buttons = [
                [
                    InlineKeyboardButton("◀️", callback_data=f"page_{query_id}_1"),
                    InlineKeyboardButton(f"🗂 1/{pages['total_pages']}", callback_data="noop"),
                    InlineKeyboardButton("▶️", callback_data=f"page_{query_id}_2")
                ]
            ]
        await message.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)
        PAGES[query_id] = results
    else:
        recent_requests[user_id] = SearchRequest(user_id, query, message)
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔎 Click here to check spelling", url=f"https://www.google.com/search?q={query}")],
            [InlineKeyboardButton("🗓 Click here for release date", url=f"https://www.google.com/search?q={query}+release+date")],
            [InlineKeyboardButton("📩 Request Upload", callback_data=f"request_upload_{query}")]
        ])
        await message.reply_text(
            f"❗ No results found for: `{query}`\n\n"
            "ℹ️ Please type movie name only\n"
            "🔍 Search correct spelling on Google",
            reply_markup=buttons
        )

# 📩 Upload Request Handler
@bot.on_callback_query(filters.regex(r"request_upload_(.+)"))
async def handle_upload_request(_, query):
    keyword = query.data.split("_", 2)[2]
    user = query.from_user

    await bot.send_message(
        LOG_CHANNEL,
        f"📥 Upload Request:\n\n👤 From: [{user.first_name}](tg://user?id={user.id}) (`{user.id}`)\n🔍 Query: `{keyword}`"
    )
    await query.answer("✅ Request sent to admin!", show_alert=True)
    await query.message.edit("📩 Your request has been sent to admin.")

# ⏪ Pagination Callback
@bot.on_callback_query(filters.regex(r"^page_(\w+)_(\d+)$"))
async def paginate_callback(client, query: CallbackQuery):
    query_id, page = query.matches[0].group(1), int(query.matches[0].group(2))

    if query_id not in PAGES:
        return await query.answer("⚠️ Pagination expired!", show_alert=True)

    results = PAGES[query_id]
    pages = paginate_results(results, page=page)

    text = "\n\n".join(pages["page_results"]) + f"\n\n📄 Page {pages['current_page']} of {pages['total_pages']}"
    total_pages = pages["total_pages"]
    nav = []

    row = []
    if page > 1:
        row.append(InlineKeyboardButton("◀️", callback_data=f"page_{query_id}_{page - 1}"))
    row.append(InlineKeyboardButton(f"🗂 {page}/{total_pages}", callback_data="noop"))
    if page < total_pages:
        row.append(InlineKeyboardButton("▶️", callback_data=f"page_{query_id}_{page + 1}"))
    nav.append(row)

    await query.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup(nav),
        disable_web_page_preview=True
    )
    await query.answer()

# 🔁 Retry Search after Force Sub
class SearchRequest:
    def __init__(self, user_id, query, message):
        self.user_id = user_id
        self.query = query
        self.message = message

    async def continue_search(self):
        spell1 = get_spell1()
        spell2 = get_spell2()
        results = await search_posts(self.query, spell1=spell1, spell2=spell2)

        if results:
            query_id = str(uuid4())[:8]
            pages = paginate_results(results, page=1)
            text = "\n\n".join(pages["page_results"]) + f"\n\n📄 Page 1 of {pages['total_pages']}"
            buttons = []

            if pages["total_pages"] > 1:
                buttons = [
                    [
                        InlineKeyboardButton("◀️", callback_data=f"page_{query_id}_1"),
                        InlineKeyboardButton(f"🗂 1/{pages['total_pages']}", callback_data="noop"),
                        InlineKeyboardButton("▶️", callback_data=f"page_{query_id}_2")
                    ]
                ]
            await bot.send_message(self.user_id, f"🔎 Searching for: `{self.query}`...")
            await bot.send_message(self.user_id, text, reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)
            PAGES[query_id] = results
        else:
            buttons = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔎 Click here to check spelling", url=f"https://www.google.com/search?q={self.query}")],
                [InlineKeyboardButton("🗓 Click here for release date", url=f"https://www.google.com/search?q={self.query}+release+date")],
                [InlineKeyboardButton("📩 Request Upload", callback_data=f"request_upload_{self.query}")]
            ])
            await bot.send_message(
                self.user_id,
                f"❗ No results found for: `{self.query}`\n\n"
                "ℹ️ Please type movie name only\n"
                "🔍 Search correct spelling on Google",
                reply_markup=buttons
            )

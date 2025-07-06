from pyrogram import filters
from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent, InlineQuery
from client import bot
from utils.script import get_spell1, get_spell2
from utils.helpers import search_posts

@bot.on_inline_query()
async def inline_handler(client, query: InlineQuery):
    user_id = query.from_user.id
    keyword = query.query.strip()

    if not keyword:
        return

    spell1 = get_spell1()
    spell2 = get_spell2()

    # Search posts based on user keyword
    results = await search_posts(keyword, spell1=spell1, spell2=spell2)

    # Use a set to avoid duplicates
    seen = set()
    inline_results = []

    for result in results:
        title = result.split("\n")[0][:60]  # First line as title
        if title in seen:
            continue
        seen.add(title)

        inline_results.append(
            InlineQueryResultArticle(
                title=title,
                description="Tap to view full result",
                input_message_content=InputTextMessageContent(result, disable_web_page_preview=True)
            )
        )

        if len(inline_results) >= 50:
            break

    if inline_results:
        await query.answer(inline_results, cache_time=1)
    else:
        await query.answer([
            InlineQueryResultArticle(
                title="No Results Found",
                description="Try using only the movie name.",
                input_message_content=InputTextMessageContent("❗ No results found.\n\nTry using only the movie name.")
            )
        ], cache_time=1)
      

from pyrogram import Client, filters
from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent, InlineQuery
from utils.script import get_spell1, get_spell2
from utils.helpers import search_posts
from uuid import uuid4

@Client.on_inline_query()
async def inline_query_handler(client, inline_query: InlineQuery):
    query = inline_query.query.strip()

    if not query:
        return await inline_query.answer([], cache_time=1)

    spell1 = get_spell1()
    spell2 = get_spell2()

    results = await search_posts(query, spell1=spell1, spell2=spell2)
    unique_set = set()
    inline_results = []

    for result in results:
        cleaned = result.strip()
        if cleaned not in unique_set:
            unique_set.add(cleaned)
            inline_results.append(
                InlineQueryResultArticle(
                    title="📥 Result Found",
                    description=cleaned[:80] + "...",
                    input_message_content=InputTextMessageContent(cleaned),
                    id=str(uuid4())
                )
            )
        if len(inline_results) >= 50:
            break

    await inline_query.answer(inline_results, cache_time=1)

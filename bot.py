"""
NuroWorks Telegram bot — main entry point.
Run with: python bot.py
Requires TELEGRAM_BOT_TOKEN set as an environment variable.
"""

import logging
import os
from datetime import datetime, timedelta, timezone

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

import config
import storage

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")


# ---------- Keyboards ----------

def main_menu_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎁 Get the free checklist", callback_data="menu:checklist")],
        [InlineKeyboardButton("🛍 Browse products", callback_data="menu:products")],
        [InlineKeyboardButton("🚀 Start a service", callback_data="menu:services")],
        [InlineKeyboardButton("💬 Talk to a human", callback_data="menu:human")],
    ])


def back_button(target="menu:main"):
    return InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back to menu", callback_data=target)]])


def checklist_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📥 Send me the checklist", callback_data="checklist:send")],
    ])


def checklist_followup_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("👀 View Brand Identity System", callback_data="service:brand")],
        [InlineKeyboardButton("⬅ Back to menu", callback_data="menu:main")],
    ])


def products_kb():
    rows = [
        [InlineKeyboardButton(f"{p['name']} — {p['price']}", callback_data=f"product:{key}")]
        for key, p in config.PRODUCTS.items()
    ]
    rows.append([InlineKeyboardButton("⬅ Back to menu", callback_data="menu:main")])
    return InlineKeyboardMarkup(rows)


def product_detail_kb(key):
    url = config.PRODUCTS[key]["checkout_url"]
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔗 Get it now", url=url)],
        [InlineKeyboardButton("⬅ Back to products", callback_data="menu:products")],
    ])


def services_kb():
    rows = [
        [InlineKeyboardButton(f"{s['name']} — {s['price']}", callback_data=f"service:{key}")]
        for key, s in config.SERVICES.items()
    ]
    rows.append([InlineKeyboardButton("⬅ Back to menu", callback_data="menu:main")])
    return InlineKeyboardMarkup(rows)


def service_detail_kb(key):
    url = config.SERVICES[key]["checkout_url"]
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔗 Get started", url=url)],
        [InlineKeyboardButton("⬅ Back to services", callback_data="menu:services")],
    ])


def human_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅ Back to menu", callback_data="menu:main")],
    ])


# ---------- Handlers ----------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    storage.touch_user(chat_id, update.effective_user.username)
    await update.message.reply_text(
        config.WELCOME_MESSAGE, reply_markup=main_menu_kb(), parse_mode="Markdown"
    )
    schedule_followup(context, chat_id)


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat_id
    data = query.data

    if data == "menu:main":
        await query.edit_message_text(config.WELCOME_MESSAGE, reply_markup=main_menu_kb())

    elif data == "menu:checklist":
        await query.edit_message_text(
            config.CHECKLIST_INTRO, reply_markup=checklist_kb(), parse_mode="Markdown"
        )

    elif data == "checklist:send":
        storage.mark_event(chat_id, "got_checklist")
        try:
            with open(config.CHECKLIST_PDF_PATH, "rb") as f:
                await context.bot.send_document(chat_id=chat_id, document=f)
        except FileNotFoundError:
            logger.warning("Checklist PDF not found at %s", config.CHECKLIST_PDF_PATH)
        await context.bot.send_message(
            chat_id=chat_id, text=config.CHECKLIST_DELIVERED, reply_markup=checklist_followup_kb()
        )

    elif data == "menu:products":
        await query.edit_message_text(config.PRODUCTS_INTRO, reply_markup=products_kb())

    elif data.startswith("product:"):
        key = data.split(":", 1)[1]
        storage.mark_event(chat_id, "viewed_product")
        p = config.PRODUCTS[key]
        text = f"*{p['name']} — {p['price']}*\n\n{p['desc']}"
        await query.edit_message_text(text, reply_markup=product_detail_kb(key), parse_mode="Markdown")

    elif data == "menu:services":
        await query.edit_message_text(config.SERVICES_INTRO, reply_markup=services_kb())

    elif data.startswith("service:"):
        key = data.split(":", 1)[1]
        storage.mark_event(chat_id, "started_service")
        s = config.SERVICES[key]
        text = f"*{s['name']} — {s['price']}*\n\n{s['desc']}"
        await query.edit_message_text(text, reply_markup=service_detail_kb(key), parse_mode="Markdown")

    elif data == "menu:human":
        await query.edit_message_text(config.HUMAN_HANDOFF, reply_markup=human_kb())

    elif data == "followup:optout":
        storage.mark_event(chat_id, "opted_out")
        await query.edit_message_text("Got it — no more nudges. Reach out anytime with /start.")


# ---------- Follow-up job ----------

def schedule_followup(context: ContextTypes.DEFAULT_TYPE, chat_id: int):
    context.job_queue.run_once(
        send_followup_if_needed,
        when=timedelta(hours=config.FOLLOWUP_DELAY_HOURS),
        chat_id=chat_id,
        data={"chat_id": chat_id},
        name=f"followup_{chat_id}",
    )


async def send_followup_if_needed(context: ContextTypes.DEFAULT_TYPE):
    chat_id = context.job.data["chat_id"]
    row = storage.get_user(chat_id)
    if row is None:
        return
    # columns: chat_id, username, first_seen, got_checklist, viewed_product,
    #          started_service, followup_sent, opted_out
    _, _, _, got_checklist, viewed_product, started_service, followup_sent, opted_out = row
    if started_service or followup_sent or opted_out:
        return
    if not (got_checklist or viewed_product):
        return

    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎨 View Brand Identity System", callback_data="service:brand")],
        [InlineKeyboardButton("🔕 No thanks", callback_data="followup:optout")],
    ])
    await context.bot.send_message(chat_id=chat_id, text=config.FOLLOWUP_MESSAGE, reply_markup=kb)
    storage.mark_event(chat_id, "followup_sent")


# ---------- Startup ----------

def main():
    if not TOKEN:
        raise RuntimeError("Set TELEGRAM_BOT_TOKEN as an environment variable before running.")

    storage.init_db()

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    logger.info("NuroWorks bot starting (polling mode)...")
    app.run_polling()


if __name__ == "__main__":
    main()
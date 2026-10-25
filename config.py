"""
All editable bot copy and links live here.
Change prices, links, or wording without touching bot.py.
"""

WELCOME_MESSAGE = (
    "Welcome to NuroWorks 👋\n\n"
    "You're one step from professional brand systems, ready-to-post content, "
    "and full business launch kits — built in days, not months.\n\n"
    "What can I help you with?"
)

CHECKLIST_INTRO = (
    "*The 25-Point Brand Identity Checklist*\n\n"
    "See exactly what your brand has, what's missing, and what to build next — "
    "before you spend a cent on a designer.\n\n"
    "Tap below and it's yours."
)

CHECKLIST_DELIVERED = (
    "Here you go — your 25-Point Brand Identity Checklist. ✅\n\n"
    "While you've got it open: if you tick fewer than 15 boxes, our Brand "
    "Identity System (from $97) fixes the gaps in 3–5 days.\n\n"
    "Want to see it?"
)

CHECKLIST_PDF_PATH = "assets/brand_checklist.pdf"  # put your PDF here

PRODUCTS_INTRO = (
    "Self-serve digital products. Instant access, no waiting.\n\n"
    "Pick one to see details:"
)

PRODUCTS = {
    "socialflow": {
        "name": "SocialFlow Pro",
        "price": "$47",
        "desc": (
            "6-niche AI social media content system. Strategy, blueprints, "
            "and 20+ prompts built in. Instant access after checkout."
        ),
        "checkout_url": "https://payhip.com/b/IeDX8",
    },
    "leadflow": {
        "name": "LeadFlow Pro",
        "price": "$97",
        "desc": (
            "7-module client acquisition system. Scripts, playbook, AI "
            "proposal generator, 30-day calendar. Instant access after checkout."
        ),
        "checkout_url": "https://payhip.com/b/klfom",
    },
    "growthos": {
        "name": "Growth Operating System",
        "price": "$127",
        "desc": (
            "All three tools bundled — save $64 vs. buying separately. "
            "Instant access after checkout."
        ),
        "checkout_url": "https://payhip.com/b/PBgi2",
    },
}

SERVICES_INTRO = (
    "Done-for-you systems. You submit a brief, we run the workflow, a "
    "finished system lands in your inbox.\n\n"
    "Which one fits where you're at?"
)

SERVICES = {
    "brand": {
        "name": "Brand Identity System",
        "price": "from $97",
        "desc": (
            "Colour palette, typography, 3 logo directions, brand voice "
            "guide, 5+ branded templates, and a brand standards one-pager.\n\n"
            "Delivered in 3–5 days. Checkout first — your brief form arrives "
            "by email right after."
        ),
        "checkout_url": "https://payhip.com/b/eNzV6",
    },
    "content": {
        "name": "30-Day Content System",
        "price": "from $147",
        "desc": (
            "30 captions, 5 content pillars, a full posting calendar, "
            "hashtag sets, and 10 reel hooks.\n\n"
            "Delivered in 48 hours. Checkout first — your brief form arrives "
            "by email right after."
        ),
        "checkout_url": "https://payhip.com/b/0FwBU",
    },
    "launch": {
        "name": "Full Launch Kit",
        "price": "from $297",
        "desc": (
            "Brand identity + 30-day content system, plus onboarding kit, "
            "welcome sequence, and a 30-day post-launch action plan.\n\n"
            "Delivered in 5–7 days. Checkout first — your brief form arrives "
            "by email right after."
        ),
        "checkout_url": "https://payhip.com/b/iqOp0",
    },
}

HUMAN_HANDOFF = (
    "Prefer to ask a real person first?\n\n"
    "📧 hello@nuroworks.com — replies within 1 business day\n"
    "💬 Or join the community group below for quick questions"
)


FOLLOWUP_MESSAGE = (
    "Still deciding? No pressure — just a nudge.\n\n"
    "If your brand checklist turned up more gaps than you expected, the "
    "Brand Identity System closes them in days, not weeks. 30-day "
    "money-back guarantee either way."
)

FOLLOWUP_DELAY_HOURS = 48

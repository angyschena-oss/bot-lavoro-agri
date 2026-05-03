import feedparser
import requests

TELEGRAM_TOKEN = "TOKEN"
CHAT_ID = "CHATID"

KEYWORDS = [
    "agronomo","agricolo","agroalimentare","zootecnico",
    "qualità","HACCP","laboratorio",
    "GDO","store manager","area manager"
]

CONCORSI_KEYWORDS = [
    "agronomo","forestale","agricolo",
    "perito agrario","ASL","ARPA"
]

RSS_FEEDS = [
    "https://it.indeed.com/rss?q=agronomo+Puglia",
    "https://it.indeed.com/rss?q=agroalimentare+Puglia",
    "https://it.indeed.com/rss?q=store+manager+Puglia",
    "https://it.indeed.com/rss?q=remote+agriculture",
    "https://www.freshplaza.it/rss",
    "https://www.almalaurea.it/rss/offerte-lavoro"
]

CONCORSI_FEEDS = [
    "https://www.gazzettaufficiale.it/rss/concorsi",
    "https://www.concorsi.it/rss"
]

def match(text, keys):
    text = text.lower()
    return any(k in text for k in keys)

def jobs():
    out = []
    for url in RSS_FEEDS:
        feed = feedparser.parse(url)
        for e in feed.entries:
            t = e.title + e.get("summary","")
            if match(t, KEYWORDS):
                out.append(f"🔹 {e.title}\n{e.link}")
    return out

def concorsi():
    out = []
    for url in CONCORSI_FEEDS:
        feed = feedparser.parse(url)
        for e in feed.entries:
            t = e.title + e.get("summary","")
            if match(t, CONCORSI_KEYWORDS):
                out.append(f"🏛️ {e.title}\n{e.link}")
    return out

def send(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

j = jobs()
c = concorsi()

msg = ""

if j:
    msg += "🌱 LAVORO:\n\n" + "\n\n".join(j[:7]) + "\n\n"

if c:
    msg += "🏛️ CONCORSI:\n\n" + "\n\n".join(c[:5])

if msg:
    send(msg)

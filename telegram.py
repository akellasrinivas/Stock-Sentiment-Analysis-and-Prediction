import asyncio
from telethon import TelegramClient
import re
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Telegram API credentials from .env file
API_ID = os.getenv("TELEGRAM_API_ID")
API_HASH = os.getenv("TELEGRAM_API_HASH")

# Logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Predefined list of Telegram channel usernames or invite links
channel_names = [
    '@TradingGuru33', '@TradeInGreen',
    '@CAJagadeesh','@StockPro_Online',
    '@StockMarketFO', '@UshasAnalysis',
]

# Helper function to clean and format message text
def clean_message_text(text):
    text = re.sub(r"#\w+", "", text)  # Remove hashtags
    text = re.sub(r"http\S+", "", text)  # Remove URLs
    text = re.sub(r"[^A-Za-z0-9.,!? ]", "", text)  # Remove special characters
    return text.strip() if text.strip() else None

# Asynchronous function to fetch messages from a single channel
async def fetch_messages_from_channel(client, channel_name, stock_name, limit):
    messages = []
    try:
        async for message in client.iter_messages(channel_name, limit=limit):  # Limit the number of messages fetched
            if message.text and stock_name.lower() in message.text.lower():
                clean_text = clean_message_text(message.text)
                if clean_text:
                    messages.append({
                        "date": message.date,
                        "text": clean_text,
                    })
    except Exception as e:
        if "flood wait" in str(e).lower():
            wait_time = int(re.search(r"(\d+)", str(e)).group(1))  # Extract wait time in seconds
            logging.warning(f"Rate limit hit: waiting for {wait_time}s before retrying...")
            await asyncio.sleep(wait_time)  # Wait dynamically
            return await fetch_messages_from_channel(client, channel_name, stock_name, limit)
        else:
            logging.error(f"Error fetching messages from {channel_name}: {e}")
    return messages

# Asynchronous function to fetch messages concurrently from multiple channels
async def fetch_messages(client, stock_name, limit=2000):
    all_messages = []

    # Create a list of tasks for concurrent execution
    tasks = [fetch_messages_from_channel(client, channel_name, stock_name, limit) for channel_name in channel_names]

    # Await all tasks concurrently
    results = await asyncio.gather(*tasks)

    # Combine all results from different channels
    for result in results:
        all_messages.extend(result)

    # Sort messages by date and time
    all_messages.sort(key=lambda x: x["date"])
    return all_messages

# Main function for scraping and saving messages
def scrape_messages(stock_name, limit=2000):
    async def run_scraper():
        async with TelegramClient('session_name', API_ID, API_HASH) as client:
            logging.info("Connected to Telegram!")
            messages = await fetch_messages(client, stock_name, limit)

            if not messages:
                logging.info(f"No relevant messages found for {stock_name}.")
                return []

            return messages

    return asyncio.run(run_scraper())

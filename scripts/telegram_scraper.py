from telethon import TelegramClient, events
import csv
import os
from dotenv import load_dotenv
from pathlib import Path
import asyncio
import pandas as pd

# Load .env file from the script's directory
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

# Load environment variables
api_id = os.getenv('TG_API_ID')
api_hash = os.getenv('TG_API_HASH')
phone = os.getenv('PHONE_NUMBER')

# Validate environment variables
if not all([api_id, api_hash, phone]):
    print("ERROR: Missing required environment variables in .env")
    exit(1)

api_id = int(api_id)

# Set up Telegram client
client = TelegramClient('scraping_session', api_id, api_hash)


def get_channels_from_excel(excel_path):
    try:
        df = pd.read_excel(excel_path)
        # Try to find a column with channel usernames
        for col in df.columns:
            if df[col].astype(str).str.startswith('@').any():
                channels = df[col].dropna().astype(str).unique().tolist()
                break
        else:
            print(f"No column with Telegram channel usernames (starting with @) found in {excel_path}")
            return []
        if len(channels) < 5:
            print(f"Warning: Only {len(channels)} channels found in {excel_path}. At least 5 are recommended.")
        return channels
    except Exception as e:
        print(f"Error reading {excel_path}: {e}")
        return []


def write_message_to_csv(writer, channel_title, channel_username, message, media_path):
    writer.writerow([
        channel_title,
        channel_username,
        message.id,
        (message.text or message.message) if message.message else "",
        message.date,
        media_path
    ])


def download_media_sync(message, media_dir):
    # Helper for synchronous media download in event handler
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(client.download_media(message.media, file=media_dir))


async def scrape_channel(client, channel_username, writer, media_dir):
    try:
        entity = await client.get_entity(channel_username)
        channel_title = entity.title

        async for message in client.iter_messages(entity, limit=1000):
            media_path = ""

            if message.media:
                filename = f"{channel_username}_{message.id}"

                if hasattr(message.media, 'photo'):
                    filename += '.jpg'
                elif hasattr(message.media, 'document'):
                    mime = message.media.document.mime_type
                    ext = mime.split('/')[-1] if mime else 'bin'
                    filename += f'.{ext}'

                media_path = os.path.join(media_dir, filename)
                await client.download_media(message.media, file=media_path)

            write_message_to_csv(writer, channel_title, channel_username, message, media_path)

    except Exception as e:
        print(f"[ERROR] while scraping {channel_username}: {str(e)}")


async def main():
    try:
        await client.start(phone=phone)
        print("Client started successfully.")

        media_dir = 'photos'
        os.makedirs(media_dir, exist_ok=True)

        channels = get_channels_from_excel('channels_to_crawl.xlsx')
        if not channels:
            print("No channels to scrape. Exiting.")
            return

        # Historical scrape
        with open('telegram_data.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Channel Title', 'Channel Username', 'Message ID', 'Message', 'Date', 'Media Path'])
            for channel in channels:
                print(f"Scraping: {channel}")
                await scrape_channel(client, channel, writer, media_dir)
                print(f"Finished scraping {channel}.")

        # Real-time ingestion: listen for new messages
        @client.on(events.NewMessage(chats=channels))
        async def handler(event):
            message = event.message
            channel = await event.get_chat()
            channel_title = getattr(channel, 'title', str(channel))
            channel_username = getattr(channel, 'username', None)
            if channel_username:
                channel_username = f"@{channel_username}" if not channel_username.startswith('@') else channel_username
            else:
                channel_username = str(channel.id)
            media_path = ""
            if message.media:
                filename = f"{channel_username}_{message.id}"
                if hasattr(message.media, 'photo'):
                    filename += '.jpg'
                elif hasattr(message.media, 'document'):
                    mime = message.media.document.mime_type
                    ext = mime.split('/')[-1] if mime else 'bin'
                    filename += f'.{ext}'
                media_path = os.path.join(media_dir, filename)
                await client.download_media(message.media, file=media_path)
            # Append to CSV
            with open('telegram_data.csv', 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                write_message_to_csv(writer, channel_title, channel_username, message, media_path)
            print(f"[REAL-TIME] New message from {channel_username} saved.")

        print("Listening for new messages in real time. Press Ctrl+C to stop.")
        await client.run_until_disconnected()

    except Exception as e:
        print(f"Fatal error: {str(e)}")
    finally:
        await client.disconnect()


if __name__ == '__main__':
    asyncio.run(main())

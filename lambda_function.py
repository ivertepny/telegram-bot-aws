import os
import asyncio
import boto3
import re

print("1. Lambda import started")

from telethon import TelegramClient
from telethon.sessions import StringSession

print("2. Telethon imported")

s3 = boto3.client("s3")

S3_BUCKET = os.environ["S3_BUCKET"]
S3_KEY = os.environ["S3_KEY"]

TG_API_ID = int(os.environ["TG_API_ID"])
TG_API_HASH = os.environ["TG_API_HASH"]
TG_SESSION_STRING = os.environ["TG_SESSION_STRING"]
TG_TARGET = os.environ["TG_TARGET"]

print("3. Variables loaded")


async def send_to_telegram(text):
    print("4. Creating Telegram client")

    client = TelegramClient(
        StringSession(TG_SESSION_STRING),
        TG_API_ID,
        TG_API_HASH,
    )

    print("5. Connecting Telegram")

    # Accept both ";" and "," as separators to avoid env formatting issues.
    targets = [target.strip() for target in re.split(r"[;,]", TG_TARGET) if target.strip()]
    if not targets:
        raise ValueError("TG_TARGET does not contain any valid targets")

    await client.connect()
    try:
        print(f"6. Sending message to {len(targets)} target(s)")
        for target in targets:
            print(f"6.1 Sending to: {target}")
            await client.send_message(target, text)

        print("7. Done")
    finally:
        await client.disconnect()


def lambda_handler(event, context):

    print("8. Lambda started")

    response = s3.get_object(Bucket=S3_BUCKET, Key=S3_KEY)

    text = response["Body"].read().decode("utf-8")

    print("9. Text loaded")

    asyncio.run(send_to_telegram(text))

    return {
        "statusCode": 200
    }
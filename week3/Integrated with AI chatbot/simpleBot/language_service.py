import os
from dotenv import load_dotenv

from azure.ai.textanalytics.aio import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential


load_dotenv()

LANGUAGE_ENDPOINT = os.getenv("LANGUAGE_ENDPOINT")
LANGUAGE_KEY = os.getenv("LANGUAGE_KEY")


if not LANGUAGE_ENDPOINT:
    raise ValueError("AZURE_LANGUAGE_ENDPOINT is missing")

if not LANGUAGE_KEY:
    raise ValueError("AZURE_LANGUAGE_KEY is missing")


async def analyze_text(text):

    client = TextAnalyticsClient(
        endpoint=LANGUAGE_ENDPOINT,
        credential=AzureKeyCredential(LANGUAGE_KEY)
    )

    try:
        results = await client.analyze_sentiment([text])

        result = results[0]

        return {
            "sentiment": result.sentiment,
            "positive": result.confidence_scores.positive,
            "neutral": result.confidence_scores.neutral,
            "negative": result.confidence_scores.negative
        }

    finally:
        await client.close()
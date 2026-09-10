import os
from dotenv import load_dotenv

from azure.ai.textanalytics.aio import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential


# Load variables from .env
load_dotenv()

AZURE_LANGUAGE_ENDPOINT = os.getenv("AZURE_LANGUAGE_ENDPOINT")
AZURE_LANGUAGE_KEY = os.getenv("AZURE_LANGUAGE_KEY")


if not AZURE_LANGUAGE_ENDPOINT:
    raise ValueError("AZURE_LANGUAGE_ENDPOINT is missing")

if not AZURE_LANGUAGE_KEY:
    raise ValueError("AZURE_LANGUAGE_KEY is missing")


async def analyze_text(text):

    client = TextAnalyticsClient(
        endpoint=AZURE_LANGUAGE_ENDPOINT,
        credential=AzureKeyCredential(AZURE_LANGUAGE_KEY)
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
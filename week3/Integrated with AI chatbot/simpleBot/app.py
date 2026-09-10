from aiohttp import web
from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import Activity
from bot import SimpleBot

from language_service import analyze_text


async def home(request):
    return web.FileResponse("templates/index.html")


async def messages(request):

    body = await request.json()

    activity = Activity().deserialize(body)

    responses = []

    class SimpleAdapter:

        async def send_activities(self, context, activities):

            for activity in activities:

                if activity.type == "message":
                    responses.append(activity.text)

            return []


    myAdapter = SimpleAdapter()

    # Fixed typo here
    context = TurnContext(myAdapter, activity)

    bot = SimpleBot()

    await bot.on_turn(context)

    # Get user's message
    user_message = activity.text

    # Send user's message to Azure Text Analytics
    analysis = await analyze_text(user_message)

    # Add Azure result to chatbot response
    azure_response = (
        f"Sentiment: {analysis['sentiment']}\n"
        f"Positive: {analysis['positive']:.2f}\n"
        f"Neutral: {analysis['neutral']:.2f}\n"
        f"Negative: {analysis['negative']:.2f}"
    )

    return web.json_response({
        "text": azure_response
    })


app = web.Application()

app.router.add_get("/", home)

app.router.add_post("/api/messages", messages)


print("Open http://localhost:3978")


web.run_app(
    app,
    host="localhost",
    port=3978
)
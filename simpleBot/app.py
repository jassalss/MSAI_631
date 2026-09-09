from aiohttp import web
from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import Activity
from bot import SimpleBot



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

    context = TurnContext(myAdapteradapter, activity)

    bot = SimpleBot()

    await bot.on_turn(context)

    return web.json_response({
        "text": responses[-1] if responses else ""
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
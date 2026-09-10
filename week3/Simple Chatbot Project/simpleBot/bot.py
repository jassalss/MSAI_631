from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ChannelAccount


class SimpleBot(ActivityHandler):

    async def on_message_activity(self, turn_context: TurnContext):
        user_message = turn_context.activity.text.lower()

        if "hello" in user_message or "hi" in user_message:
            response = "Hello! How can I help you?"

        elif "name" in user_message:
            response = "My name is SimpleBot. I am a chatbot built using MBF."

        elif "ai" in user_message:
            response = "AI stands for Artificial Intelligence. It give power to computers think like humans, and give more intelligence"

        elif "bye" in user_message:
            response = "Goodbye! Have a great day!"

        else:
            response = f"You said: {turn_context.activity.text}"

        await turn_context.send_activity(response)

    async def on_members_added_activity(
        self,
        members_added: list[ChannelAccount],
        turn_context: TurnContext
    ):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(
                    "Hello! I am your SimpleBot. Type hello or hi to start."
                )
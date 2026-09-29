import { pipeline } from
    "https://cdn.jsdelivr.net/npm/@huggingface/transformers@4.3.0";

const chatBox =
    document.getElementById("chatBox");

const userInput =
    document.getElementById("userInput");

const sendButton =
    document.getElementById("sendButton");

const clearButton =
    document.getElementById("clearButton");

const status =
    document.getElementById("status");


let chatbot = null;

let conversation = [];


async function loadAIModel() {

    try {

        status.textContent =
            "⏳ Loading AI model... First load may take some time.";

        sendButton.disabled = true;


        chatbot = await pipeline(
            "text-generation",
            "HuggingFaceTB/SmolLM2-360M-Instruct"
        );


        status.textContent =
            "✅ AI model ready! Ask me a question.";

        sendButton.disabled = false;

        userInput.disabled = false;

        userInput.focus();


    } catch (error) {

        console.error(
            "Model loading error:",
            error
        );


        status.textContent =
            "Could not load the AI model. Check the browser console.";

    }

}

function addMessage(message, sender) {

    const container =
        document.createElement("div");


    if (sender === "user") {

        container.className =
            "user-message";

    } else {

        container.className =
            "bot-message";

    }
    const bubble =
        document.createElement("div");


    bubble.className =
        "message";


    bubble.textContent =
        message;


    container.appendChild(bubble);


    chatBox.appendChild(container);


    chatBox.scrollTop =
        chatBox.scrollHeight;


    return bubble;

}

async function askAI(question) {

    if (!chatbot) {

        return "The AI model is still loading. Please wait.";

    }
    conversation.push({

        role: "user",

        content: question

    });
    const messages = [

        {

            role: "system",

            content:
                "You are Group 6 Smart Chatbot. " +
                "Answer questions clearly and simply. " +
                "Use simple English. " +
                "Keep answers concise but useful."

        },

        ...conversation

    ];

    const output =
        await chatbot(
            messages,
            {
                max_new_tokens: 150,

                temperature: 0.7,

                do_sample: true
            }
        );

    const generated =
        output[0].generated_text;


    let answer;
    if (Array.isArray(generated)) {

        answer =
            generated[
                generated.length - 1
            ].content;

    } else {

        answer =
            generated;

    }
    conversation.push({

        role: "assistant",

        content: answer

    });


    return answer;

}
async function sendMessage() {

    const question =
        userInput.value.trim();


    if (!question) {

        return;

    }
    addMessage(
        question,
        "user"
    );
    userInput.value = "";
    sendButton.disabled = true;
    const botBubble =
        addMessage(
            "Thinking...",
            "bot"
        );


    try {

        const answer =
            await askAI(question);


        botBubble.textContent =
            answer;


    } catch (error) {

        console.error(
            "AI error:",
            error
        );


        botBubble.textContent =
            "Sorry, I could not generate an answer.";

    }

    sendButton.disabled = false;

    userInput.focus();

}

sendButton.addEventListener(
    "click",
    sendMessage
);
userInput.addEventListener(
    "keydown",
    function(event) {

        if (event.key === "Enter") {

            sendMessage();

        }

    }
);

clearButton.addEventListener(
    "click",
    function() {

        conversation = [];

        chatBox.innerHTML = "";

        addMessage(
            "Hello!  I'm your smart AI chatbot. Ask me a question.",
            "bot"
        );

    }
);

loadAIModel();
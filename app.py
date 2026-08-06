# app.py
# -------------------------------------------------------------------------
# Local AI Chatbot powered by Shiny, Chatlas, and Ollama
# -------------------------------------------------------------------------

import json
import logging
from urllib.error import URLError
from urllib.request import urlopen

from chatlas import ChatOllama
from shiny import reactive
from shiny.express import input, ui


# -------------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------------

OLLAMA_MODELS_URL = "http://localhost:11434/api/tags"
DEFAULT_MODEL = "llama3:latest"

DEFAULT_SYSTEM_PROMPT = """
You are a helpful, friendly, and concise AI assistant.
Explain technical concepts clearly and provide examples when useful.
""".strip()

WELCOME_MESSAGE = (
    "Hello! I am a locally hosted AI assistant. "
    "How can I help you today?"
)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# -------------------------------------------------------------------------
# Ollama model discovery
# -------------------------------------------------------------------------

def format_model_name(model_name: str) -> str:
    """Convert an Ollama model name into a readable label."""

    name_without_tag = model_name.split(":", maxsplit=1)[0]

    return (
        name_without_tag
        .replace("-", " ")
        .replace("_", " ")
        .title()
    )


def get_installed_models() -> dict[str, str]:
    """Retrieve locally installed models from the Ollama API."""

    try:
        with urlopen(OLLAMA_MODELS_URL, timeout=3) as response:
            data = json.load(response)

        models = data.get("models", [])
        choices: dict[str, str] = {}

        for model in models:
            model_name = model.get("name")

            if not model_name:
                continue

            details = model.get("details", {})
            parameter_size = details.get("parameter_size", "Unknown")

            label = (
                f"{format_model_name(model_name)} "
                f"({parameter_size})"
            )

            choices[model_name] = label

        if choices:
            return choices

        logger.warning("No Ollama models were detected.")

    except (URLError, TimeoutError, json.JSONDecodeError, OSError) as error:
        logger.warning("Could not retrieve Ollama models: %s", error)

    # Fallback allows the app interface to load
    return {DEFAULT_MODEL: "Llama 3"}


AVAILABLE_MODELS = get_installed_models()

SELECTED_DEFAULT_MODEL = (
    DEFAULT_MODEL
    if DEFAULT_MODEL in AVAILABLE_MODELS
    else next(iter(AVAILABLE_MODELS))
)

# -------------------------------------------------------------------------
# Create the Ollama chat client
# -------------------------------------------------------------------------

chat_client = ChatOllama(
    model=SELECTED_DEFAULT_MODEL,
    system_prompt=DEFAULT_SYSTEM_PROMPT,
)

# -------------------------------------------------------------------------
# Page configuration
# -------------------------------------------------------------------------

ui.page_opts(
    title="Multi-Purpose AI Chatbot",
    fillable=True,
    fillable_mobile=True,
)

# -------------------------------------------------------------------------
# Sidebar settings
# -------------------------------------------------------------------------

with ui.sidebar(
    title="Chat Settings",
    open="desktop",
):

    ui.input_select(
        "model",
        "AI model",
        choices=AVAILABLE_MODELS,
        selected=SELECTED_DEFAULT_MODEL,
    )

    ui.help_text(
        "Models are detected automatically from your local "
        "Ollama installation."
    )

    ui.help_text(
        """
        Llama 3 – Best for general conversations.
        Mistral – Strong for reasoning and coding.
        Phi-3 – Fast and lightweight.
        """
    )

    ui.input_text_area(
        "system_prompt",
        "AI instructions",
        value=DEFAULT_SYSTEM_PROMPT,
        rows=7,
        resize="vertical",
    )

    ui.help_text(
        "Example: You are an experienced Python teacher "
        "helping adults prepare coding using python."
    )

    ui.input_slider(
        "temperature",
        "Response creativity",
        min=0.0,
        max=1.0,
        value=0.7,
        step=0.1,
    )

    ui.help_text(
        "Lower values are more focused and consistent. "
        "Higher values are more varied and creative."
    )

    ui.input_action_button(
        "clear_chat",
        "Clear conversation",
        class_="btn-danger",
    )

    ui.hr()

    ui.markdown(
        """
        **About**

        This chatbot runs locally using:

        - Shiny for Python
        - Chatlas
        - Ollama
        - Open-source language models

        Your conversation is processed locally on your computer.
        """
    )

# -------------------------------------------------------------------------
# Chat interface
# -------------------------------------------------------------------------

chat = ui.Chat(id="chat")

chat.ui(
    messages=[
        {
            "role": "assistant",
            "content": WELCOME_MESSAGE,
        }
    ],
    placeholder="Ask me anything...",
)

# -------------------------------------------------------------------------
# Clear conversation
# -------------------------------------------------------------------------

@reactive.effect
@reactive.event(input.clear_chat)
async def clear_conversation():
    """Clear the visible messages and model conversation memory."""

    await chat.clear_messages()
    chat_client.set_turns([])

# -------------------------------------------------------------------------
# Generate a response
# -------------------------------------------------------------------------

@chat.on_user_submit
async def handle_user_input(user_input: str):
    """Generate and stream an Ollama response."""

    cleaned_input = user_input.strip()

    if not cleaned_input:
        return

    try:
        selected_prompt = input.system_prompt().strip()

        chat_client.model = input.model()

        chat_client.system_prompt = (
            selected_prompt
            if selected_prompt
            else DEFAULT_SYSTEM_PROMPT
        )

        chat_client.set_model_params(
            temperature=input.temperature()
        )

        response = await chat_client.stream_async(cleaned_input)
        await chat.append_message_stream(response)

    except ConnectionError:
        logger.exception("Could not connect to Ollama.")

        await chat.append_message(
            {
                "role": "assistant",
                "content": (
                    "I could not connect to Ollama. "
                    "Please confirm that Ollama is running."
                ),
            }
        )

    except Exception as error:
        logger.exception("Unexpected chatbot error.")

        await chat.append_message(
            {
                "role": "assistant",
                "content": (
                    "An unexpected error occurred.\n\n"
                    f"```text\n"
                    f"{type(error).__name__}: {error}\n"
                    f"```"
                ),
            }
        )
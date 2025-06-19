import os
import openai
import gradio

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "meta-llama/llama-4-scout:free"
DEFAULT_TEXT = "Can you explain to me the origin of the High German, and then provide a simple text in German about its origin and current changes. Make the text concise, clear and signficant for a German language learner"
SUPPORTED_LANGUAGES = [
    "English",
    "Spanish",
    "German",
    "French",
    "Chinese",
]
LANGUAGE_CODES = {
    "English": "en",
    "Spanish": "es",
    "German": "ge",
    "French": "fr",
    "Chinese": "zh"
}
AVAILABLE_MODELS = {
    "DeepSeek": "",
    "Llama3": "",
    "Llama-4 Scout": "",
    "Llama-4 Maverick": ""
}

if OPENROUTER_API_KEY == "":
    raise Exception


def main(text: str, model: str = MODEL):
    client = openai.OpenAI(
        base_url="https://openrouter.ai/api/v1", api_key=OPENROUTER_API_KEY
    )
    completion = client.chat.completions.create(
        extra_headers={},
        extra_body={},
        model=model,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": text},
                ],
            }
        ],
    )
    print(f"LLM: {model}, question: {text}\nResponse:\n")
    print(completion.choices[0].message.content)


with gradio.Blocks() as landing_page:
    gradio.Markdown("🌍 Let's replace teachers together...")

    with gradio.Row():
        input_language = gradio.Dropdown(
            choices=SUPPORTED_LANGUAGES, value="English", label="Input Language", interactive=True
        )
        target_language = gradio.CheckboxGroup(
            choices=SUPPORTED_LANGUAGES, label="Target Languages (max 2 for quality)"
        )
    
    with gradio.Row():
        model_selector = gradio.Dropdown(
            choices=list(AVAILABLE_MODELS.keys()),
            value="Llama-4 Scout",
            label="Translation Model",
            interactive=True
        )
    
    with gradio.Row():
        audio_input = gradio.Audio(
            type="filepath", label="Speak the phrase to translate your native or target language.",
            interactive=True,
            show_download_button=True
        )
        text_input = gradio.Textbox(label="Or type it", elem_id="text_input")

    transcribed_audio = gradio.Textbox(label="Transcribed from audio", interactive=False)
    text_response_output = gradio.Textbox(label="Response", interactive=False)
    audio_response_output = gradio.Audio(label="Speech", interactive=False)


landing_page.launch()

import os
import openai
import gradio

DEFAULT_TEXT = "Can you explain to me the origin of the High German, and then provide a simple text in German about its origin and current changes. Make the text concise, clear and signficant for a German language learner"
SUPPORTED_LANGUAGES = [
  "English",
  "Spanish",
  "German",
  "French",
  "Chinese",
]
LANGUAGE_CODES = {"English": "en", "Spanish": "es", "German": "de", "French": "fr", "Chinese": "zh"}
AVAILABLE_MODELS = {
  "DeepSeek Llama 70B": "deepseek-r1-distill-llama-70b:free",
  "Llama-3 70B": "meta-llama/llama-3.3-70b-instruct:free",
  "Llama-4 Scout": "meta-llama/llama-4-scout-17b-16e:free",
  "Llama-4 Maverick": "meta-llama/llama-4-maverick-17b-128e:free",
}


def main(api_key: str):
  with gradio.Blocks() as landing_page:
    gradio.Markdown("🌍 Let's learn languages...")
    with gradio.Row():
      target_language_dropdown = gradio.Dropdown(
        choices=SUPPORTED_LANGUAGES, value="English", label="Target Language", interactive=True
      )
      model_selector = gradio.Dropdown(
        choices=list(AVAILABLE_MODELS.keys()),
        value="Llama-4 Scout MoE",
        label="LLM (OpenRouter)",
        interactive=True
      )
    with gradio.Row():
      audio_input = gradio.Audio(
        type="filepath", label="Speak your question...", interactive=True, show_download_button=True
      )
      text_input = gradio.Textbox(label="Or type your question")

    transcribed_audio_ouput = gradio.Textbox(value="Transcribed Text", label="Transcription from OpenAI (Whisper)",interactive=False)
    submit_button = gradio.Button("Process Input")

  landing_page.launch()


if __name__ == "__main__":
  api_key = os.getenv("OPENROUTER_API_KEY")
  if api_key == "" or api_key is None:
    raise Exception("OPENROUTER_API_KEY not set/found.")
  print(f"Found {api_key=}")
  main(api_key)

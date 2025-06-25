import os
import openai
import gradio
from pathlib import Path

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
  "Llama-4 Scout": "meta-llama/llama-4-scout:free",
  "Llama-4 Maverick": "meta-llama/llama-4-maverick-17b-128e:free",
}

def generate_speech(text: str | None):
  if not text:
    return None 

def generate_llm_response(client: openai.OpenAI, text: str, model_name: str, language: str):
  # It assumes the OpenAI - OpenRouter client
  default = "meta-llama/llama-4-scout-17b-16e:free"
  context = f"You are a polyglot assistant, aware of language details and how to teach each one. Provide your response in {language.upper()}"
  model_id = AVAILABLE_MODELS.get(model_name, default)
  print(f"Generate LLM request with {model_id=}")
  print(f"{client.base_url}")
  messages = [
    {"role": "system", "content": context},
    {"role": "user", "content": text}
  ]
  print(f"messages request\n: {messages}")
  # TODO: Llama4 Scout maximum context length of 64000 tokens.
  completion = client.chat.completions.create(
    extra_headers={},
    extra_body={},
    model=model_id,
    messages=messages,
    max_completion_tokens=1024 * 8
  )
  response_content = completion.choices[0].message.content
  print(f"LLM: {model_name}\nQuestion: {text}\nResponse: {response_content}")
  return response_content 

def transcribe_audio(audio_file: str | Path | None):
  """Transcribe audio with the OpenAI's Whisper API""" 
  if audio_file is None:
    return ""

def process_translation(
    openai_client: openai.OpenAI,
    openrouter_client: openai.OpenAI,
    audio_file, typed_text, target_language: str, model_name: str):
  """Handles STT -> LLM -> TTS"""
  print(f"{audio_file=}, {typed_text=}, {target_language=}, {model_name=}")
  transcribed_text= ""
  if audio_file:
    transcribed_text = transcribe_audio(audio_file)
  input_text = typed_text if typed_text else transcribed_text
  if not input_text:
    return "", "", None # Exit if input_text is ""
  llm_response_text = generate_llm_response(openrouter_client, input_text, model_name, target_language)
  audio_response_path = generate_speech(llm_response_text)
  return transcribed_text, llm_response_text, audio_response_path

def main(openrouter_api_key: str, openai_api_key: str = ""):
  openrouter_client = openai.OpenAI(api_key=openrouter_api_key, base_url="https://openrouter.ai/api/v1")
  openai_client = openai.OpenAI(api_key=openai_api_key)

  with gradio.Blocks() as landing_page:
    gradio.Markdown("🌍 Let's learn languages...")
    with gradio.Row():
      target_language_dropdown = gradio.Dropdown(
        choices=SUPPORTED_LANGUAGES, value="English", label="Target Language", interactive=True
      )
      model_selector = gradio.Dropdown(
        choices=list(AVAILABLE_MODELS.keys()),
        value="Llama-4 Scout",
        label="LLM (OpenRouter)",
        interactive=True
      )
    with gradio.Row():
      audio_input = gradio.Audio(
        type="filepath", label="Speak your question...", interactive=True, show_download_button=True
      )
      text_input = gradio.Textbox(label="Or type your question", value="e.g. Can you write a simple poem of the Spanish heritage in the USA? ")

    submit_button = gradio.Button("Process Input")
    transcribed_audio_ouput = gradio.Textbox(value="Transcribed Text", label="Transcription from OpenAI (Whisper)",interactive=False)
    text_response_output = gradio.Textbox(label="LLM Response", interactive=False)
    audio_response_output = gradio.Audio(label="Audio Response", interactive=False)

    def _client_translation(audio_file, typed_text, target_lang: str, model_name: str):
      return process_translation(openai_client, openrouter_client, audio_file, typed_text, target_lang, model_name)

    submit_button.click(
      fn=_client_translation,
      inputs=[audio_input, text_input, target_language_dropdown, model_selector],
      outputs=[transcribed_audio_ouput, text_response_output, audio_response_output]
    )

  landing_page.launch()


if __name__ == "__main__":
  openrouter_key = os.getenv("OPENROUTER_API_KEY")
  openai_key = os.getenv("OPENAI_API_KEY")
  if openrouter_key == "" or openrouter_key is None:
    raise Exception("OPENROUTER_API_KEY not set/found.")
  if openai_key is None:
    openai_key = ""

  main(openrouter_key, openai_key)

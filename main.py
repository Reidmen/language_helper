import os
import argparse
import openai

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if OPENROUTER_API_KEY == "":
  raise Exception


def main(text: str, model: str):
  client = openai.OpenAI(base_url="https://openrouter.ai/api/v1", api_key=OPENROUTER_API_KEY)
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


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--question", required=True, type=str, help="Question to send to the API")
  parser.add_argument(
    "--model",
    required=False,
    type=str,
    default="meta-llama/llama-4-scout:free",
    help="Model to use for inference. Default to Llama4 Scout 17B -16E (109B total params).",
  )
  args = parser.parse_args()
  main(args.question, args.model)

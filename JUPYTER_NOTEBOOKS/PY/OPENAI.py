import openai
import os

# Set up the OpenAI API client
openai.api_key = os.environ["OPENAI_API_KEY"]
model_engine = "davinci"  # the name of the OpenAI model to use

# Generate text using the OpenAI API
prompt = "Once upon a time"
response = openai.Completion.create(
  engine=model_engine,
  prompt=prompt,
  max_tokens=100,
)

print(response.choices[0].text)

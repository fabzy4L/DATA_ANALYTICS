import openai
import os

# Set your OpenAI API key
openai.api_key = os.environ["OPENAI_API_KEY"]

# Create an API request with the stream parameter
response = openai.Completion.create(
    engine="davinci",
    prompt="Hello,",
    max_tokens=5,
    n=1,
    stream=True
)

# Loop through the response and print each partial result
for result in response:
    print(result.choices[0].text)

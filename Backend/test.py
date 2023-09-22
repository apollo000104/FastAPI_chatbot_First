import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key=os.getenv("OPENAI_API_KEY")

messages=[]
def chatbot_response(msg):
    item =  {"role": "user", "content": msg}
    messages.append(item)
    # ChatGPT is powered by gpt-3.5-turbo, OpenAI’s most advanced language model.
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    print(str(response['choices'][0]['message']['content'])+"\n")
    return str(response['choices'][0]['message']['content'])

chatbot_response("what is python?")
# print(messages)
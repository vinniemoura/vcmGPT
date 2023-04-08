from flask import Flask, render_template, request
import os
import openai
import os
import sys

app = Flask(__name__)

try:
  openai.api_key = os.environ['OPENAI_API_KEY']
except KeyError:
  sys.stderr.write("""
    You haven't set up your API key yet.

    If you don't have an API key yet, visit:

    https://platform.openai.com/signup

    1. Make an account or sign in
    2. Click "View API Keys" from the top right menu.
    3. Click "Create new secret key"

    Then, open the Secrets Tool and add OPENAI_API_KEY as a secret.
    """)
  exit(1)

messages = [{
  "role": "system",
  "content": "Hello! What do you want to learn about?"
}]


@app.route('/')
def home():
  return render_template('index.html')


@app.route('/get')
def get_bot_response():
  global messages
  user_text = request.args.get('msg')
  messages.append({"role": "user", "content": user_text})
  response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                          messages=messages)
  content = response['choices'][0]['message']['content'].strip()
  messages.append({"role": "assistant", "content": content})
  return str(content)


if __name__ == '__main__':
  app.run(debug=True)

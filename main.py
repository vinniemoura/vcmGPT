import os
import os
import openai
import os
import sys
  
try:
  openai.api_key = os.environ.get('VERCEL_OPENAI_API_KEY')
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

topic = input("what do you want to learn about?/>".strip())

messages = [{"role":"system", "content": f"I want to do some interactive instruction. I want you to start explaining the concept of {topic} to me at a 10th grade level. Then stop, give  me a multiple choice quiz, grade the quiz, and resume the explanation. If I get the quiz     wrong, reduce the grade level by 3 for the explanation and language you use, making the language simpler. Otherwise increase it by three and make the language harder. Then quiz me again and repeat the process. Do not talk about the changing of the grade level. Don't give away the answer to the quiz before the user has chance to respond. Stop after you've asked each question to wait for the user to answer."}]

first = False
while True:
  if first:
    question = input("> ")
    messages.append({"role": "user", "content": question})

  first = True

  response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages
  )

  content = response['choices'][0]['message']['content'].strip()

  print(f"{content}")
  messages.append({"role": "assistant", "content": content})

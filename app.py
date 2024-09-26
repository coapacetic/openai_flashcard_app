from flask import Flask, render_template, request, jsonify
from pydantic import BaseModel
from openai import OpenAI
import json

app = Flask(__name__)

client = OpenAI()

class FlashCard(BaseModel):
    keyword: str
    definition: str

class FlashCardStack(BaseModel):
    cards: list[FlashCard]

def generate_flashcards(input_text):
    # Simple example: split input into words and create flashcards
    words = str(input_text)

    completion = client.beta.chat.completions.parse(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a tutor that is being asked to create flashcards for studying a specific topic"},
        {"role": "user", "content": words}
    ],
    response_format=FlashCardStack
    )

    flashcards = completion.choices[0].message.parsed.cards

    flashcards_json = [object_to_dict(card) for card in flashcards]

    print(flashcards_json)

    return flashcards_json

def object_to_dict(obj):
    return obj.__dict__  # Use __dict__ to get attributes as a dictionary

@app.route('/', methods=['GET', 'POST'])
def index():
    flashcards = {}
    if request.method == 'POST':
        user_input = request.form['user_input']
        flashcards = generate_flashcards(user_input)
    
    return render_template('index.html', flashcards=flashcards)

if __name__ == '__main__':
    app.run(debug=True)

# Specify the filename to save the JSON blob
# filename = 'flashcardstack.json'

# Open the file and write the JSON data
# with open(filename, 'w') as json_file:
#     json.dump(flashcardstack_json, json_file, indent=4)

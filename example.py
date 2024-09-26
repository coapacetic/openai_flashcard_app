from pydantic import BaseModel
from openai import OpenAI
import json

client = OpenAI()

class FlashCard(BaseModel):
    keyword: str
    definition: str

class FlashCardStack(BaseModel):
    cards: list[FlashCard]

completion = client.beta.chat.completions.parse(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a tutor that is being asked to create flashcards for studying a specific topic"},
        {"role": "user", "content": "Help me create flashcards for learning the 150 first pokemon and memorizing their types. The front of the flashcard should be the Pokemon's name and the back of the flashcard should be only the type of the pokemon.  An example of a type is psychic."
        }
    ],
    response_format=FlashCardStack
)

# print(completion.choices[0].message)
cards = completion.choices[0].message.parsed.cards
print(type(cards))
print(cards)

def object_to_dict(obj):
    return obj.__dict__  # Use __dict__ to get attributes as a dictionary

flashcardstack_json = [object_to_dict(card) for card in cards]

# Specify the filename to save the JSON blob
filename = 'flashcardstack.json'

# Open the file and write the JSON data
with open(filename, 'w') as json_file:
    json.dump(flashcardstack_json, json_file, indent=4)
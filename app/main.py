import os
import json
import random
import openai
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize the Flask app
app = Flask(__name__)

# File to store NPC data
DATA_FILE = os.path.join("data", "npc_data.json")

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Function to generate response using OpenAI
def generate_response(npc_name, user_message):
    try:
        # Define the messages for the conversation
        messages = [
            {"role": "system", "content": f"{npc_name} is a wise and engaging NPC in a tabletop RPG. Respond to the player's questions and comments thoughtfully."},
            {"role": "user", "content": user_message}
        ]

        # Use openai.completions.create with the updated API format
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Use the appropriate model, e.g., "gpt-4" if available
            messages=messages,
            max_tokens=150,
            temperature=0.7
        )

        # Correct access to response content
        npc_response = response.choices[0].message.content.strip()
        return npc_response

    except openai.OpenAIError as e:  # Generic OpenAI error handling
        print(f"Error generating response: {e}")
        return f"{npc_name} says: 'I'm having trouble responding right now.'"

    except openai.RateLimitError as e:  # Handling rate limit errors specifically
        print(f"Rate limit exceeded: {e}")
        return f"{npc_name} says: 'The system is temporarily overwhelmed. Please try again later.'"

# Save NPC data to a file
def save_data():
    # Ensure the data folder exists
    os.makedirs("data", exist_ok=True)
    # Save NPC data to the JSON file
    with open(DATA_FILE, "w") as file:
        json.dump(npcs, file, indent=4)

# Load NPC data from file
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            data = json.load(file)

        # Convert keys to integers and ensure each NPC has a 'messages' key
        converted_data = {}
        for npc_id, npc in data.items():
            int_id = int(npc_id)  # Convert key to integer
            if "messages" not in npc:
                npc["messages"] = []  # Initialize with an empty list
            converted_data[int_id] = npc

        return converted_data
    return {}

# In-memory storage for NPCs
npcs = load_data()

# Function to generate random NPC stats
def generate_npc():
    return {
        "name": random.choice(["Preacher", "Merchant", "Guard", "Scholar"]),
        "armor_class": random.randint(10, 20),
        "hit_points": f"{random.randint(8, 12)}d8 + {random.randint(10, 30)}",
        "speed": f"{random.randint(20, 40)} ft.",
        "stats": {
            "STR": random.randint(8, 18),
            "DEX": random.randint(8, 18),
            "CON": random.randint(8, 18),
            "INT": random.randint(8, 18),
            "WIS": random.randint(8, 18),
            "CHA": random.randint(8, 18),
        },
        "special_traits": [
            "Spellcasting",
            "Unshakeable Faith",
            "Multitasker",
        ],
        "actions": [
            {
                "name": "Morningstar",
                "description": "Melee Weapon Attack. +6 to hit, reach 5 ft., one target. Hit: 7 (1d8 + 3) piercing damage."
            },
            {
                "name": "Condemning Speech",
                "description": "The NPC speaks words of condemnation at one target within 30 feet. The target must make a DC 16 Wisdom saving throw."
            },
        ],
        "messages": []  # Initialize chat log as an empty list
    }

# Home route to display all NPCs
@app.route('/')
def home():
    return render_template('home.html', npcs=npcs)

# Route to generate a new NPC
@app.route('/generate_npc', methods=['POST'])
def generate_npc_route():
    npc_id = len(npcs) + 1
    npc = generate_npc()
    npcs[npc_id] = npc
    save_data()  # Save data after adding the NPC
    return redirect(url_for('home'))

# Route to chat with an NPC
@app.route('/chat/<int:npc_id>', methods=['GET', 'POST'])
def chat(npc_id):
    npc = npcs.get(npc_id)  # Get the NPC by ID
    if not npc:
        return "NPC not found", 404

    if "messages" not in npc:
        npc["messages"] = []  # Initialize if missing

    if request.method == 'POST':
        user_message = request.form['user_message']
        npc["messages"].append({"sender": "You", "text": user_message})

        # Generate the NPC response using OpenAI
        npc_response = generate_response(npc["name"], user_message)
        npc["messages"].append({"sender": npc['name'], "text": npc_response})

        save_data()  # Save updated data

    return render_template('chat.html', npc=npc, npc_id=npc_id, messages=npc["messages"])

# Run the Flask app (for debugging purposes)
if __name__ == "__main__":
    app.run(debug=True)

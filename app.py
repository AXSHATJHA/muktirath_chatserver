from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import google.generativeai as genai
import pandas as pd

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure Gemini
genai.configure(api_key="AIzaSyBb1ibq8MsRaRKoF_KZDZJCJwE7KKBInQ0")
model = genai.GenerativeModel("gemini-1.5-flash")

# Load the dataset using Pandas
df = pd.read_csv("courses.csv")

# Handle missing or non-string values in 'Category' and 'Title' columns
df['Category'] = df['Category'].fillna('').astype(str)  # Replace NaN with empty string
df['Title'] = df['Title'].fillna('').astype(str)  # Replace NaN with empty string
df['Skills Required'] = df['Skills Required'].fillna('None').astype(str)  # Replace NaN with 'None'
df['Next Course'] = df['Next Course'].fillna('None').astype(str)  # Replace NaN with 'None'

@app.route('/suggest', methods=['POST'])
def suggest_courses():
    user_input = request.json.get('input')

    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    # Convert the dataset into a string format for Gemini to process
    courses_str = ""
    for _, row in df.iterrows():
        courses_str += (
            f"Title: {row['Title']}, "
            f"Category: {row['Category']}, "
            f"Language: {row['Language']}, "
            f"Skills Required: {row['Skills Required']}, "
            f"Age: {row['Age']}, "
            f"Next Course: {row['Next Course']}, "
            f"URL: {row['URL']}\n"
        )

    # Use Gemini to generate a response based on user input and the courses
    response = model.generate_content(
        f"Here is a list of courses:\n{courses_str}\n\n"
        f"Based on the following user input, suggest relevant courses in a chatbot-like way: {user_input}"
    )

    # Return the Gemini response
    return jsonify({"response": response.text})

if __name__ == '__main__':
    app.run(debug=True)
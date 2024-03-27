from flask import Flask, request, jsonify, render_template
import openai
import os
from dotenv import load_dotenv
import traceback

load_dotenv()
app = Flask(__name__)

# Set your OpenAI API key
openai.api_key = os.getenv("API_KEY")
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/evaluate', methods=['POST'])
def evaluate_text():
    # Extract text data from the POST request form
    essay_title = request.form['essay_title']
    essay = request.form['essay']
    
    try:
        # Generate prompt for OpenAI
        prompt = f"Title: {essay_title}\nEssay: {essay}\nEvaluate the essay and provide feedback."

        # Send prompt to OpenAI API for evaluation
        response = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            temperature=0.7,
            max_tokens=200
        )

        # Process the API response
        evaluation = response['choices'][0]['text'].strip()

        # Split evaluation into separate components
        components = evaluation.split('\n')
        grade = components[0]
        relevance = components[1]
        errors = components[2]
        feedback = components[3]
        improvised_essay = components[4]

        # Pass evaluation results as JSON response
        return jsonify({
            'grade': grade,
            'relevance': relevance,
            'errors': errors,
            'feedback': feedback,
            'improvised_essay': improvised_essay
        })

    except openai.error.RateLimitedError as e:
        return jsonify({'error': 'Rate limit exceeded. Please try again later.'}), 429  # Return a 429 status code for rate limit exceeded

    except Exception as e:
        traceback.print_exc()  # Print the exception traceback to the console
        return jsonify({'error': 'Internal server error occurred. Please try again later.'}), 500

if __name__ == '__main__':
    # Run Flask using Gunicorn
    # Use the format "module_name:app" to specify the Flask app
    # Example: gunicorn myapp:app
    # Replace "myapp" with the name of your Python module
    # Replace "app" with the name of your Flask instance
    # Adjust host and port as needed
    gunicorn_command = "gunicorn -b 0.0.0.0:5000 app:app"
    os.system(gunicorn_command)

    app.run(debug=True)
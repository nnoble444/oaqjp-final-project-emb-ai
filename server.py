from flask import Flask, render_template, request
from EmotionDetection import emotion_detector

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/emotionDetector", methods=['GET', 'POST'])
def emotionDetector():
    if request.method == 'POST':
        text_to_analyze = request.form.get('textToAnalyze', '')
    else:
        text_to_analyze = request.args.get('textToAnalyze', '')
    
    if not text_to_analyze or text_to_analyze.strip() == "":
        return "Invalid text! Please try again."
    
    # Call the emotion detection function from the package
    result = emotion_detector(text_to_analyze)
    
    # Handle error case
    if result['dominant_emotion'] is None:
        return "Invalid text! Please try again."
    
    # Format the response as requested
    response_text = (
        f"For the given statement, the system response is "
        f"'anger': {result['anger']}, "
        f"'disgust': {result['disgust']}, "
        f"'fear': {result['fear']}, "
        f"'joy': {result['joy']} and "
        f"'sadness': {result['sadness']}. "
        f"The dominant emotion is {result['dominant_emotion']}."
    )
    
    return response_text

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

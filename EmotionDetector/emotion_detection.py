import requests
import json

def emotion_detector(text_to_analyze):
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    # Exact header from the original task (note the hyphen)
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    
    input_json = {
        "raw_document": {
            "text": text_to_analyze
        }
    }
    
    response = requests.post(url, headers=headers, json=input_json)
    
    # Debug: show status if something is wrong
    if response.status_code != 200:
        print(f"API Error - Status Code: {response.status_code}")
        print("Response:", response.text[:500])
        return {
            'anger': None, 'disgust': None, 'fear': None,
            'joy': None, 'sadness': None, 'dominant_emotion': None
        }
    
    try:
        formatted_response = response.json()
        
        # Correct structure for this Watson NLP endpoint
        emotions = formatted_response['emotionPredictions'][0]['emotion']
        
        anger = emotions.get('anger', 0.0)
        disgust = emotions.get('disgust', 0.0)
        fear = emotions.get('fear', 0.0)
        joy = emotions.get('joy', 0.0)
        sadness = emotions.get('sadness', 0.0)
        
        # Find dominant emotion
        emotion_scores = {
            'anger': anger,
            'disgust': disgust,
            'fear': fear,
            'joy': joy,
            'sadness': sadness
        }
        dominant_emotion = max(emotion_scores, key=emotion_scores.get)
        
        return {
            'anger': anger,
            'disgust': disgust,
            'fear': fear,
            'joy': joy,
            'sadness': sadness,
            'dominant_emotion': dominant_emotion
        }
        
    except Exception as e:
        print(f"Parsing Error: {e}")
        print("Raw response:", response.text[:500])
        return {
            'anger': None, 'disgust': None, 'fear': None,
            'joy': None, 'sadness': None, 'dominant_emotion': None
        }
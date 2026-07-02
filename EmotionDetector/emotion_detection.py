import requests
import json

def emotion_detector(text_to_analyze):
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    # Use the exact header from the original task (with hyphen)
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    
    input_json = {
        "raw_document": {
            "text": text_to_analyze
        }
    }
    
    response = requests.post(url, headers=headers, json=input_json)
    
    # Task 7 requirement: Check status_code for blank input handling
    if response.status_code == 400:
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }
    
    # For other non-200 responses, also return None values (safe default)
    if response.status_code != 200:
        print(f"API returned status code: {response.status_code}")
        print("Response body:", response.text[:500])
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }
    
    try:
        formatted_response = response.json()
        
        # This is the correct structure for the Watson NLP EmotionPredict endpoint
        emotions = formatted_response['emotionPredictions'][0]['emotion']
        
        anger = emotions.get('anger', 0.0)
        disgust = emotions.get('disgust', 0.0)
        fear = emotions.get('fear', 0.0)
        joy = emotions.get('joy', 0.0)
        sadness = emotions.get('sadness', 0.0)
        
        # Determine dominant emotion
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
        print(f"Error parsing response: {e}")
        print("Raw response text:", response.text[:500])
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }

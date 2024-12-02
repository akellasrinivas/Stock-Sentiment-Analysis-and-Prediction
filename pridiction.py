import numpy as np
import pandas as pd
import plotly.express as px
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import matplotlib.pyplot as plt
import yfinance as yf

# Load the saved model
model = load_model('model.h5')

# Define function to predict stock movement
def predict_stock_movement(sentiment_score):
    if sentiment_score == 2:  # Positive sentiment
        return 1  # Predict "Up"
    elif sentiment_score == 0:  # Negative sentiment
        return -1  # Predict "Down"
    else:
        return 0  # Neutral sentiment

# Function to parse user input
def parse_input(input_string):
    lines = input_string.strip().split("\n")
    data = []
    for line in lines:
        timestamp, message = line.split(",", 1)
        data.append({"timestamp": timestamp.strip(), "message": message.strip()})
    return data

# Function to make predictions and generate graphs
def process_and_predict_data(input_data, tokenizer):
    # Parse the user input
    data = parse_input(input_data)

    # Prepare data for predictions
    sample_texts = [entry['message'] for entry in data]
    sample_timestamps = [entry['timestamp'] for entry in data]

    # Tokenize and pad texts
    sample_seqs = tokenizer.texts_to_sequences(sample_texts)
    sample_pads = pad_sequences(sample_seqs, maxlen=100)

    # Predict sentiments
    predictions = model.predict(sample_pads)
    predicted_classes = np.argmax(predictions, axis=1)
    predicted_probabilities = np.max(predictions, axis=1)

    # Prepare results
    results = []
    for timestamp, sentiment, prob, text in zip(sample_timestamps, predicted_classes, predicted_probabilities, sample_texts):
        stock_movement = predict_stock_movement(sentiment)
        results.append({
            'timestamp': pd.to_datetime(timestamp),
            'message': text,
            'predicted_stock_movement': stock_movement,
            'stock_movement_label': 'Up' if stock_movement == 1 else 'Neutral' if stock_movement == 0 else 'Down',
            'predicted_sentiment': sentiment,
            'confidence': f"{prob * 100:.2f}%"  # Confidence as percentage
        })

    # Create DataFrame
    df = pd.DataFrame(results)

    # Plot the results (using Plotly and Matplotlib)
    return df

import streamlit as st
import pandas as pd
import plotly.express as px
from tensorflow.keras.preprocessing.text import Tokenizer
from telegram import scrape_messages
from pridiction import process_and_predict_data
import yfinance as yf
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from tensorflow.keras.metrics import AUC, Accuracy

# Main Page Title and Description
st.title('Stock Sentiment Analysis and Prediction')
st.write("Select a stock from the table or enter manually:")

# Table with predefined stocks and their tickers
stock_data = {
    "Stock Name": ["HDFC", "TATA", "Nifty", "SBI", "ICICI", "Airtel", "Infosys", "Reliance"],
    "Stock Ticker": ["HDFCBANK.NS", "TATAMOTORS.NS", "^NSEI", "SBIN.NS", "ICICIBANK.NS", "AIRTEL.NS", "INFY.NS", "RELIANCE.NS"]
}
stock_df = pd.DataFrame(stock_data)

# Sidebar for stock selection
selected_stock = st.sidebar.selectbox("Select a Stock", stock_df["Stock Name"])

# Set the corresponding stock ticker based on selection
stock_ticker = stock_df[stock_df["Stock Name"] == selected_stock]["Stock Ticker"].values[0]

# User input for stock name (editable)
stock_name = st.text_input('Enter Stock Name (e.g., nifty)', selected_stock)

# User input for stock ticker (editable)
stock_ticker_input = st.text_input('Enter Stock Ticker (e.g., ^NSEI)', stock_ticker)

# Load your model
model = load_model('model.h5')

# Manually compile the model with metrics if necessary
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=[Accuracy(), AUC()])

# Button to trigger data scraping and prediction
if st.button('Get Stock Prediction'):
    # Step 1: Scrape messages from Telegram
    st.write(f"Scraping Telegram data for {stock_name}...")
    messages = scrape_messages(stock_name)

    if not messages:
        st.write("No messages found for this stock in the last 7 days.")
    else:
        # Step 2: Process and predict sentiments
        st.write(f"Predicting stock movement for {stock_name}...")

        # Initialize a tokenizer
        tokenizer = Tokenizer()
        tokenizer.fit_on_texts([msg['text'] for msg in messages])  # Fit tokenizer on scraped data

        # Prepare input data as a string (you can choose another format based on how you want to display messages)
        input_data = "\n".join([f"{msg['date']},{msg['text']}" for msg in messages])

        # Process the data and make predictions
        df = process_and_predict_data(input_data, tokenizer)

        # Step 3: Display results
        st.write("Predicted Stock Movement Based on Sentiment:")
        st.dataframe(df)

        # Plot the predicted stock movement over time
        fig_scatter = px.scatter(
            df,
            x='timestamp',
            y='predicted_stock_movement',
            color='stock_movement_label',
            color_discrete_map={'Up': 'green', 'Neutral': 'gray', 'Down': 'red'},
            labels={'predicted_stock_movement': 'Stock Movement', 'timestamp': 'Date & Time'},
            title=f'Predicted Stock Movement for {stock_name} Over Time',
            hover_data=['confidence']
        )
        st.plotly_chart(fig_scatter)

        # Assuming `df` is the DataFrame containing the predictions
        sentiment_counts = df['predicted_sentiment'].value_counts()

        # Map numeric sentiment predictions to readable labels
        sentiment_labels = {0: 'Negative', 1: 'Neutral', 2: 'Positive'}

        # Create a pie chart of sentiment distribution
        fig_pie = px.pie(
            names=[sentiment_labels[s] for s in sentiment_counts.index],
            values=sentiment_counts.values,
            title="Sentiment Analysis Distribution",
            color_discrete_map={'Negative': 'red', 'Neutral': 'gray', 'Positive': 'green'}
        )

        # Display the pie chart in Streamlit
        st.plotly_chart(fig_pie)

        # Fetch and plot the stock price for the given stock ticker
        st.write(f"Fetching stock price data for {stock_ticker_input}...")
        stock_data = yf.download(stock_ticker_input, start=df['timestamp'].min(), end=df['timestamp'].max())
        st.write(stock_data.tail())

        # Matplotlib plot of predicted stock movement vs stock price
        fig, ax1 = plt.subplots(figsize=(10, 6))

        # Scatter plot for predicted stock movement
        movement_map = {1: 'Up', 0: 'Neutral', -1: 'Down'}
        df['stock_movement_label'] = df['predicted_stock_movement'].map(movement_map)
        colors = df['stock_movement_label'].map({'Up': 'green', 'Neutral': 'gray', 'Down': 'red'})
        ax1.scatter(df['timestamp'], df['predicted_stock_movement'], c=colors, label='Predicted Stock Movement', s=50)

        # Twin axis for stock price
        ax2 = ax1.twinx()
        ax2.plot(stock_data.index, stock_data['Close'], color='blue', label='Stock Price', linewidth=2)

        ax1.set_xlabel('Time')
        ax1.set_ylabel('Predicted Stock Movement')
        ax2.set_ylabel('Stock Price (USD)')

        ax1.legend(loc='upper left')
        ax2.legend(loc='upper right')
        st.pyplot(fig)

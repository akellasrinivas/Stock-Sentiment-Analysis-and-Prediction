# Stock-Sentiment-Analysis-and-Prediction

Stock Sentiment Analysis and Prediction This project enables users to
analyze stock sentiment based on messages from various Telegram channels
and predict stock movements using sentiment analysis. The system fetches
data, performs sentiment analysis on the messages, and provides visual
insights such as predicted stock movement and sentiment distribution. It
also integrates stock price data from Yahoo Finance for additional
insights.

Web UI (Insert your image here)

Features Stock Sentiment Analysis: Analyzes sentiment from messages
related to stocks found in predefined Telegram channels. Stock Movement
Prediction: Predicts stock price movement (Up, Neutral, or Down) based
on sentiment. Visualization: Interactive visualizations of sentiment
distribution and predicted stock movement over time. Stock Price Data:
Fetches and visualizes historical stock prices using Yahoo Finance API.
User-friendly Interface: Built using Streamlit for an interactive and
intuitive user experience. Technologies Used Streamlit: Used for
building the interactive web interface. TensorFlow/Keras: Utilized for
sentiment prediction using a pre-trained deep learning model. yfinance:
Used to fetch stock price data from Yahoo Finance. Plotly: Used for
interactive charts and visualizations (scatter plots and pie charts).
Matplotlib: Used for plotting stock price data against predicted stock
movements. Telegram API: Integrated with Telegram to fetch messages from
predefined channels related to stock discussions. Pandas: Used for data
manipulation and handling predictions. Installation Clone the
repository: bash Copy code git clone
https://github.com/akellasrinivas/Stock-Sentiment-Analysis-and-Prediction.git
Create a virtual environment: bash Copy code python -m venv venv
Activate the virtual environment: For Windows: bash Copy code
venv\\Scripts\\activate For macOS/Linux: bash Copy code source
venv/bin/activate Install the required dependencies: bash Copy code pip
install -r requirements.txt Set up environment variables: Obtain your
Telegram API credentials and set them in a .env file in the root
directory of the project. Add your Telegram API ID and API Hash: bash
Copy code TELEGRAM_API_ID=your_api_id_here
TELEGRAM_API_HASH=your_api_hash_here Start the application: bash Copy
code streamlit run app.py Open your web browser and visit
http://localhost:8501 to access the application. Functionality 1. Stock
Selection and Input Predefined Stock List: Select from a list of
predefined stocks or input your own stock name and ticker symbol.
Editable Inputs: Manually enter the stock name and ticker to perform
custom analysis. 2. Telegram Data Scraping Scrapes messages from
predefined Telegram channels related to stocks using the Telegram API.
Filters messages containing relevant stock discussions based on the
stock name. Cleans and processes the text to remove irrelevant content
like hashtags and URLs. 3. Sentiment Analysis and Prediction Sentiment
Classification: The system uses a pre-trained deep learning model to
predict the sentiment (positive, neutral, negative) of each message.
Stock Movement Prediction: The sentiment of each message is mapped to a
stock movement prediction (Up, Neutral, Down). Confidence Levels: The
sentiment predictions come with confidence levels, providing a measure
of how certain the model is about the sentiment. 4. Visualization
Predicted Stock Movement Plot: Interactive scatter plot showing the
predicted stock movement (Up, Neutral, Down) over time. Sentiment
Distribution: Pie chart visualizing the distribution of sentiments
(Negative, Neutral, Positive) for the messages analyzed. Stock Price
Data: Historical stock price data for the selected stock is fetched and
plotted alongside the predicted stock movements for comparison. 5. Stock
Price Data Fetching yfinance Integration: Fetches historical stock price
data for the selected stock ticker. Matplotlib Plot: Plots the predicted
stock movement against the actual stock price data. Supported File
Formats This project works with Telegram messages and integrates data
from Yahoo Finance. There is no file upload feature for this project, as
it focuses on real-time analysis of stock discussions and predictions.

Authors Akella Srinivas: Developer and Project Lead Contribution
Contributions are welcome! If you find any issues or have suggestions
for improvements, please feel free to create an issue or submit a pull
request.

License This project is licensed under the MIT License.

Contact For any inquiries or further information, please contact Akella
Srinivas.

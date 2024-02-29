import google.generativeai as genai
from pathlib import Path
import gradio as gr
import os
import sys
sys.path.insert(1, '/Users/peter/Desktop/Capstone LLM Cases/Stock-Chart-Analyzer') # Your path for constant
from constant import Api_Key

genai.configure(api_key=Api_Key)
model = genai.GenerativeModel(model_name="gemini-pro-vision")

def read_image_data(file_path):
    image_path = Path(file_path)
    if not image_path.exists():
        raise FileNotFoundError(f"Could not find image: {image_path}")
    return {"mime_type": "image/jpeg", "data": image_path.read_bytes()}

def generate_gemini_response(prompt, image_path):
    image_data = read_image_data(image_path)
    response = model.generate_content([prompt, image_data])
    return response.text

input_prompt = """
As a seasoned market analyst with an uncanny ability to decipher the language of price charts, your expertise is crucial in navigating the turbulent seas of financial markets. You will be presented with static images of historical stock charts, where your keen eye will dissect the intricate dance of candlesticks, trendlines, and technical indicators. Armed with this visual intelligence, you will unlock the secrets hidden within these graphs, predicting the future trajectory of the depicted stock with remarkable accuracy.
Analysis Guidelines:

Company Overview: Begin with a brief overview of the company whose stock chart you are analyzing. Understand its market position, recent news, financial health, and sector performance to contextualize your technical analysis.

PPattern Recognition: Diligently examine the chart to pinpoint critical candlestick formations, trendlines, and a comprehensive set of technical indicators, including Moving Averages (e.g., SMA, EMA), Momentum Indicators (e.g., RSI, MACD), Volume Indicators (e.g., OBV, VWAP), and Volatility Indicators (e.g., Bollinger Bands, ATR), relevant to the timeframe and instrument in question.

Technical Analysis: Leverage your in-depth knowledge of technical analysis principles to decode the identified patterns and indicators. Extract nuanced insights into market dynamics, identifying key levels of support and resistance, and gauge potential price movements in the near future.

Sentiment Prediction: Drawing from your technical analysis, predict the likely direction of the stock price. Determine whether the stock is poised for a bullish upswing or a bearish downturn. Assess the likelihood of a breakout versus consolidation phase, taking into account the confluence of technical signals.

Confidence Level: Evaluate the robustness and reliability of your prediction. Assign a confidence level based on the coherence and convergence of the technical evidence at hand.Disclaimer: Remember, your insights are a powerful tool for informed decision-making, but not a guarantee of future performance. Always practice prudent risk management and seek professional financial advice before making any investment decisions.

Your role is pivotal in equipping traders and investors with critical insights, enabling them to navigate the market with confidence. Embark on your analysis of the provided chart, decoding its mysteries with the acumen and assurance of a seasoned technical analyst."""

# Function to process uploaded files and generate a response
def process_uploaded_files(files):
    file_path = files[0].name if files else None
    response = generate_gemini_response(input_prompt, file_path) if file_path else None
    return file_path, response

# Gradio interface
with gr.Blocks() as demo:
    file_output = gr.Textbox()
    image_output = gr.Image()
    combined_output = [image_output, file_output]
    upload_button = gr.UploadButton(
        "Click to Upload Chart Screenshot",
        file_types=["image"],
        file_count="multiple",
    )
    upload_button.upload(process_uploaded_files, upload_button, combined_output)

demo.launch(debug=True)

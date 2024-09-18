---

# **StockBot: Your Real-Time Stock Market Companion**

![image](https://www.cxtoday.com/wp-content/uploads/2020/12/Twilio-WhatsApp-Partnership-to-Enhance-Developer-Experience.jpg)  
*"Get real-time stock market updates on WhatsApp with ease."*

## **Introduction**

StockBot is a real-time stock market information bot that allows users to easily check stock prices directly through WhatsApp. The application leverages the Twilio API for WhatsApp messaging and the MarketStack API for fetching stock data. Whether you're an active trader or an investor monitoring stocks, StockBot makes it easy to stay updated with real-time data in the simplest and most convenient way.

### **Deployed Link:**  
[StockBot Live](https://stockbot-ialm.onrender.com)

### **YouTube Live Demo:**  
[StockBot Live](https://youtu.be/U4Zgmqc1s9U)

### **Website:**  
[StockBot Website](https://stockbot.framer.ai/)


### **Final Project Blog Article:**  
[Read my journey behind StockBot](https://medium.com/@ebukaharrison6/building-stockbot-bringing-real-time-stock-market-data-to-whatsapp-users-a7465798cf9b)

### **Author: Harrison Eze**  
[LinkedIn](https://www.linkedin.com/in/harrison-eze)

---

## **Table of Contents**

1. [Installation](#installation)
2. [Usage](#usage)
3. [Contributing](#contributing)
4. [Related Projects](#related-projects)
5. [Technical Details](#technical-details)
6. [Challenges & Inspiration](#challenges--inspiration)
7. [Licensing](#licensing)

---

## **Installation**

### **Prerequisites**

- Python 3.8+
- A Twilio Account with WhatsApp API setup
- A MarketStack API key for fetching real-time stock data
- Ngrok (Optional, but recommended for local development)

### **Steps**

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/harrisoneze/stockbot.git
   cd stockbot
   ```

2. **Install Dependencies:**
   Create and activate a virtual environment, then install the required dependencies:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables:**
   Create a `.env` file in the root directory with your credentials:

   ```bash
   TWILIO_ACCOUNT_SID=your_twilio_sid
   TWILIO_AUTH_TOKEN=your_twilio_token
   TWILIO_PHONE_NUMBER=whatsapp:+14155238886
   MARKETSTACK_KEY=your_marketstack_key
   ```

4. **Run the Flask App:**

   ```bash
   python app.py
   ```

5. **Expose Local Server Using Ngrok (Optional for Testing):**
   ```bash
   ngrok http 5001
   ```
   Update the webhook URL in your Twilio Dashboard with the Ngrok URL (`https://<your-ngrok-url>/webhook`).

---

## **Usage**

### **How It Works:**

Before sending a message, you can activate the sandbox by sending "positive-fairly" to the Twilio WhatsApp number +14155238886.

1. **Send "Hi"** to start interacting with the bot via WhatsApp.

   - **Example**: `Hi`
   - **Response**: "Hello, welcome to the Stock Market bot! Type sym:<stock_symbol> to know the price of the latest stock."

2. **Request a Stock Price**:

   - **Example**: `sym:AAPL`
   - **Response**: "The stock price of AAPL is: $150.23"

3. **Handle Invalid Inputs**:
   - If you provide an incorrect format, the bot will guide you to use the correct format.

---

## **Contributing**

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. **Fork the repository**
2. **Create a new branch** for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature
   ```
3. **Make your changes**
4. **Commit your changes**:
   ```bash
   git commit -m 'Add feature/your-feature'
   ```
5. **Push to your branch**:
   ```bash
   git push origin feature/your-feature
   ```
6. **Submit a pull request**

Please ensure your code follows best practices and includes necessary tests.

---

## **Related Projects**

Here are some related projects/documentations you might find interesting:

- [Twilio WhatsApp Integration Documentation](https://www.twilio.com/docs/whatsapp)
- [MarketStack API Documentation](https://marketstack.com/documentation)
- [Flask - Web Development Framework](https://flask.palletsprojects.com/)

---

## **Technical Details**

### **Architecture Overview:**

1. **Flask Backend**:
   - Handles incoming requests via the `/webhook` route. It processes WhatsApp messages and responds with the appropriate stock data.
2. **Twilio API Integration**:

   - Used for sending and receiving WhatsApp messages. The bot can respond to user messages, guiding them through the process and providing real-time stock data.

3. **MarketStack API**:

   - Provides real-time stock data. The bot fetches the latest intraday price for any stock symbol requested by the user.

4. **Ngrok (For Local Testing)**:
   - Ngrok is used to expose the Flask app running locally so that it can be accessed by Twilio's webhooks during development.

### **Code Highlights**:

- **Message Processing**:

  ```python
  def process_msg(msg):
      if msg.strip() == "Hi":
          return "Hello, type sym:<stock_symbol> to get stock price."
      elif msg.lower().startswith('sym:'):
          stock_symbol = msg.split(':')[1].strip()
          stock_price = get_stock_price(stock_symbol)
          return f"The stock price of {stock_symbol} is: ${stock_price['last_price']}"
      else:
          return "Invalid input. Please type 'Hi' or 'sym:<stock_symbol>'."
  ```

- **Stock Price Fetching**:

  ```python
  def get_stock_price(stock_symbol):
      if not API_KEY:
          raise ValueError("API_KEY is not set in environment variables")

      params = {"access_key": API_KEY}
      end_point = f"{BASE_URL}/tickers/{stock_symbol}/intraday/latest"
      api_result = requests.get(end_point, params=params)

      if api_result.status_code != 200:
          raise ValueError(f"Error fetching data: {api_result.status_code} - {api_result.text}")

      json_result = api_result.json()

      if "last" not in json_result:
          raise KeyError("Stock price not available")

      return {"last_price": json_result["last"]}
  ```

---

## **Challenges & Inspiration**

### **Inspiration**:

I created StockBot out of a personal need for a quick and straightforward way to access real-time stock prices. As someone who actively follows the stock market, I found it inconvenient to continuously check multiple websites and apps to get this information. I wanted to make the process as simple as sending a WhatsApp message, which is an app most people use daily.

### **Challenges**:

1. **Twilio API Misconfiguration**:
   Initially, I mistakenly used `client.message.create` instead of `client.messages.create`, which led to errors. Debugging this taught me a valuable lesson in reading API documentation thoroughly.

2. **Environment Setup**:
   Running Flask in the wrong environment (Anaconda) caused several dependency issues. I realized the importance of using virtual environments and ensuring that the correct environment is activated.

3. **Handling API Errors**:
   I encountered cases where stock symbols were invalid or the MarketStack API did not return data as expected. To address this, I added comprehensive error handling in the `get_stock_price` function.

### **What's Next**:

- **Improved Error Handling**:
  I plan to implement more user-friendly error messages when stock symbols are incorrect or unavailable.
- **Stock Alerts**:
  In future iterations, users will be able to subscribe to stock alerts to receive notifications when a stock's price reaches a certain threshold.

---

## **Licensing**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

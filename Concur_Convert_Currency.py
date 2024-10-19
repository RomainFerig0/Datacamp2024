import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
import requests
import sqlite3
import bcrypt
import datetime

#%% Define database

if "show_evol_news_coverage" not in st.session_state:
    st.session_state.show_evol_news_coverage = False

# Function to get the connection
def get_connection():
    conn = sqlite3.connect('users.db')
    return conn

# Create users table
def create_users_table():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password BLOB NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Register a new user with a hashed password
def register_user(username, password):
    conn = get_connection()
    c = conn.cursor()
    # Hash the password (store it as bytes, no decoding here)
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    try:
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed))
        conn.commit()
        st.success("Registration successful!")
    except sqlite3.IntegrityError:
        st.error("Username already exists.")
    conn.close()

# Authenticate a user by verifying their password
def authenticate_user(username, password):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT password FROM users WHERE username = ?', (username,))
    result = c.fetchone()
    conn.close()
    
    if result:
        # Retrieve the stored password hash as bytes (no need to encode)
        stored_password = result[0]
        return bcrypt.checkpw(password.encode('utf-8'), stored_password)
    
    return False

# Initialize the database and create users table
create_users_table()

#%%

# API key
api_key = 'fca_live_SIpowqnwKbsiYX3qqN5yKFy2odNcimYFTfhNHQJJ'
base_url = 'https://api.freecurrencyapi.com/v1/'
cache = {}

@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_data(base_currency, target_currency):
        
    url = "https://api.freecurrencyapi.com/v1/latest"

    # Setting the parameters
    params = {
        'currencies': f'{target_currency}',
        'base_currency': f'{base_currency}',
        'apikey': api_key,
    }
    
    # Adding the API key to the headers
    headers = {
        'apikey': api_key
    }
        
    try:
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code in [200, 201, 202, 203]:
            return response.json()
        else:
            st.write(base_currency, target_currency, url)
            st.error(f"Failed to retrieve data. Status code: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error occurred: {e}")
        return None

@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_historical_data(base_currency, target_currency, date):

    url = "https://api.freecurrencyapi.com/v1/historical"

    # Setting the parameters
    params = {
        'date' : f'{date}',
        'currencies': f'{target_currency}',
        'base_currency': f'{base_currency}',
        'apikey': api_key,
    }
    
    # Adding the API key to the headers
    headers = {
        'apikey': api_key
    }
        
    try:
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code in [200, 201, 202, 203]:
            return response.json()
        else:
            st.error(f"Failed to retrieve data. Status code: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error occurred: {e}")
        return None
    
@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_currency_info(target_currency):
            
    url = "https://api.freecurrencyapi.com/v1/currencies"
    
    # Setting the parameters
    params = {
        'currencies': f'{target_currency}',
    }
    
    # Adding the API key to the headers
    headers = {
        'apikey': api_key
    }
        
    try:
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code in [200, 201, 202, 203]:
            return response.json()
        else:
            st.error(f"Failed to retrieve data. Status code: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error occurred: {e}")
        return None

#%%

# Dropdowns for base and target currencies
country = ['USD', 'EUR', 'AUD', 'CAD', 'GBP', 'JPY', 'CHF', 'AFN', 'ALL', 'DZD', 'AOA', 'ARS', 
           'AMD', 'AWG', 'AZN', 'BSD', 'BHD', 'BDT', 'BBD', 'BYR', 'BZD', 'BMD', 'BTN', 'BOB', 'BAM', 
           'BWP', 'BRL', 'BND', 'BGN', 'KHR', 'INR', 'CNY', 'MXN']

if "show_converter" not in st.session_state:
    st.session_state.show_converter = False

if "show_historical" not in st.session_state:
    st.session_state.show_historical = False

st.set_page_config(page_title="Currency Converter", page_icon="💱")

if "open_session" not in st.session_state:
    st.session_state.open_session = False
    
if st.session_state.open_session :
    
    st.title("Welcome to ConCur !")    
    st.write("### Currency info")
    st.sidebar.header("Sections: ")
    st.sidebar.title("""
                                                                   
    [Currency converter](#currency-conversion)  
    Use the main section to select currencies and convert amounts.

    [Currency information](#currency-info)  

    [Historical exchange rate](#historical-exchange-rate-trend)
                     """)

    target_currency_info = st.selectbox("Select currency", country)
    if st.button("Search"):
        currency_data = get_currency_info(target_currency_info)
        if currency_data:
            symbol = currency_data['data'][target_currency_info]['symbol']
            name = currency_data['data'][target_currency_info]['name']
            name_plural = currency_data['data'][target_currency_info]['name_plural']
            st.write(f"""
                     Currency : {name}   
                     Currency (plural) : {name_plural}  
                     Symbol : {symbol}  
                     """)
    if st.button("Confirm"):
        st.session_state.show_converter = not st.session_state.show_converter
       
    if st.session_state.show_converter:
         
        st.write("### Currency Conversion")
            
        base_currency = st.selectbox("Select base currency", country, index = country.index(target_currency_info))
        target_currency = st.selectbox("Select target currency", country)
    
        # Input field for the amount to convert
        amount = st.number_input("Enter amount to convert", min_value=0.0, step=1.0)
    
        # Perform the conversion based on selected currencies (for today's rate)
        if st.button("Convert"):
            today = datetime.date.today().strftime('%Y-%m-%d')
            latest_data = get_data(base_currency, target_currency)
            if latest_data:
                rate = latest_data['data'][target_currency]
                converted_amount = amount * rate
                st.session_state.show_historical = not st.session_state.show_historical
                st.write(f"{amount} {base_currency} is equal to {converted_amount:.2f} {target_currency}")
       
    if st.session_state.show_historical:

        # Historical exchange rate plot
        st.write(f"### Historical Exchange Rate Trend : {base_currency} to {target_currency}")
    
        # Select date range for historical data
        start_date = st.date_input("Start date", datetime.date.today() - datetime.timedelta(days=30))
        end_date = st.date_input("End date", datetime.date.today())
    
        # Fetch and plot historical data
        dates = pd.date_range(start=start_date, end=end_date)
        exchange_rates = []
        valid_dates = []  # To track the dates where we successfully fetch data
    
        if st.button("Generate evolution"):
        
            for date in dates:
                date_str = date.strftime('%Y-%m-%d')
                historical_data = get_historical_data(base_currency, target_currency, date_str)
                if historical_data:
                    try:
                        rate = historical_data['data'][date_str][target_currency]
                        exchange_rates.append(rate)
                        valid_dates.append(date)  # Only append dates where data is valid
                    except KeyError:
                        st.warning(f"No data available for {date_str}")
    
        # Create a DataFrame for easier manipulation, ensuring both lists have the same length
        if exchange_rates and valid_dates:
            df = pd.DataFrame({
                'Date': valid_dates,
                'Exchange Rate': exchange_rates
            })
    
            # Plot the data using Matplotlib
            fig, ax = plt.subplots()
            ax.plot(df['Date'], df['Exchange Rate'], label=f'{base_currency} to {target_currency}')
            ax.set_xlabel('Date')
            ax.set_ylabel('Exchange Rate')
            ax.set_title(f'Exchange Rate Trend: {base_currency} to {target_currency}')
            plt.xticks(rotation=45)
            plt.tight_layout()
    
            # Display the plot in Streamlit
            st.pyplot(fig)

else :
    # Streamlit UI for user authentication
    st.title("User Authentication Example")
    
    menu = ["Login", "Sign Up"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    if choice == "Sign Up":
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type='password')
    
        if st.button("Sign Up"):
            if new_user and new_password:
                register_user(new_user, new_password)
            else:
                st.error("Please provide both username and password.")
    
    elif choice == "Login":
        st.subheader("Login to Your Account")
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
    
        if st.button("Login"):
            if authenticate_user(username, password):
                st.success(f"Welcome {username}!")
                st.session_state.open_session = True
                # Add more authenticated content here if needed
            else:
                st.error("Invalid username or password.")
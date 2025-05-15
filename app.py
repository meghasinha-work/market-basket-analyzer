import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO

# -------------------------------
# Minimalist color palette
BG_COLOR = "#f7f1e1"         # Beige background
ACCENT_COLOR = "#f7c59f"     # Apricot accent
TEXT_COLOR = "#3e3e3e"       # Dark grey text
BUTTON_COLOR = "#f7a072"     # Stronger apricot for buttons

# -------------------------------
# Hardcoded users for demo login
USERS = {
    "admin": "password123",
    "user": "market2025"
}

# -------------------------------
def login():
    st.markdown(
        f"""
        <style>
            .login-container {{
                max-width: 400px;
                margin: 80px auto;
                padding: 30px;
                background: white;
                border-radius: 12px;
                box-shadow: 0 2px 10px rgb(0 0 0 / 0.1);
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }}
            .login-container h2 {{
                color: {ACCENT_COLOR};
                text-align: center;
                margin-bottom: 25px;
            }}
            .stTextInput>div>div>input {{
                border-radius: 8px;
                border: 1px solid #ddd;
                padding: 10px;
                font-size: 16px;
            }}
            .stButton>button {{
                background-color: {BUTTON_COLOR};
                color: white;
                font-weight: bold;
                border-radius: 10px;
                padding: 10px 20px;
                margin-top: 15px;
            }}
            .stButton>button:hover {{
                background-color: #ec7e4f;
                cursor: pointer;
            }}
        </style>
        <div class="login-container">
            <h2>Market Basket Analyzer - Login</h2>
        </div>
        """, unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_btn = st.button("Login")

    if login_btn:
        if username in USERS and USERS[username] == password:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")

def logout():
    st.session_state["logged_in"] = False
    st.session_state["username"] = None
    st.experimental_rerun()

def main_app():
    st.markdown(
        f"""
        <style>
            .main-container {{
                background-color: {BG_COLOR};
                color: {TEXT_COLOR};
                padding: 20px 40px;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                border-radius: 10px;
            }}
            .title {{
                color: {ACCENT_COLOR};
                font-size: 2.4rem;
                font-weight: 700;
                margin-bottom: 15px;
            }}
            .section-header {{
                color: {BUTTON_COLOR};
                font-size: 1.5rem;
                font-weight: 600;
                margin-top: 25px;
                margin-bottom: 10px;
            }}
            .footer {{
                font-size: 0.9rem;
                color: #666;
                margin-top: 40px;
                text-align: center;
            }}
            .stButton>button {{
                background-color: {BUTTON_COLOR};
                color: white;
                font-weight: 600;
                border-radius: 8px;
                padding: 8px 18px;
                margin-top: 12px;
            }}
            .stButton>button:hover {{
                background-color: #ec7e4f;
                cursor: pointer;
            }}
            .tooltip {{
                border-bottom: 1px dotted #999;
                cursor: help;
                color: {ACCENT_COLOR};
                font-weight: 600;
            }}
        </style>
        <div class="main-container">
            <div class="title">Market Basket Analyzer</div>
            <div>Welcome, <b>{st.session_state["username"]}</b>! &nbsp;&nbsp; 
            <button onclick="window.location.reload()">🔄 Refresh</button>
            <button onclick="document.dispatchEvent(new CustomEvent('streamlit:rerun'))" style="background:none;border:none;color:{BUTTON_COLOR};cursor:pointer;font-size:1.2rem;" title="Logout" id="logout-btn">🚪 Logout</button>
            </div>
        </div>
        """, unsafe_allow_html=True
    )

    # Logout button workaround
    if st.button("Logout"):
        logout()

    # Sidebar
    st.sidebar.markdown(f"""
        <h3 style="color:{ACCENT_COLOR}; font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">Navigation</h3>
        Upload your transactional data (CSV) below.
        <span style="font-size:0.85rem; color:#666;">
            <b>Tip:</b> Your CSV should have transactions grouped in rows, items separated by commas.
        </span>
        """, unsafe_allow_html=True)

    uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.sidebar.success("Data loaded!")

        st.markdown("### Uploaded Data Preview")
        st.dataframe(df.head(), use_container_width=True)

        # Example: Basic Market Basket Analysis placeholder
        st.markdown('<div class="section-header">Market Basket Analysis Results</div>', unsafe_allow_html=True)
        
        # For demo, just count unique items and show a bar chart
        all_items = df.astype(str).values.flatten()
        items_series = pd.Series(all_items)
        items_count = items_series.value_counts().head(10)

        fig, ax = plt.subplots()
        items_count.plot(kind='bar', color=BUTTON_COLOR, ax=ax)
        ax.set_title('Top 10 Items Frequency')
        ax.set_ylabel('Count')
        ax.set_xlabel('Item')
        st.pyplot(fig)

        # Download button for results (example CSV export of item counts)
        csv_buffer = StringIO()
        items_count.to_csv(csv_buffer)
        csv_bytes = csv_buffer.getvalue().encode()

        st.download_button(
            label="Download Item Counts CSV",
            data=csv_bytes,
            file_name="item_counts.csv",
            mime="text/csv",
            key="download-item-counts"
        )
    else:
        st.info("Upload a CSV file from the sidebar to get started.")

# -------------------------------
def main():
    st.set_page_config(
        page_title="Market Basket Analyzer",
        page_icon="🛒",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    # Initialize session state
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
        st.session_state["username"] = None

    st.markdown(
        f"""
        <style>
            .block-container {{
                padding-top: 1rem;
                padding-left: 3rem;
                padding-right: 3rem;
                background-color: {BG_COLOR};
                min-height: 90vh;
            }}
        </style>
        """, unsafe_allow_html=True
    )

    if not st.session_state["logged_in"]:
        login()
    else:
        main_app()

if __name__ == "__main__":
    main()

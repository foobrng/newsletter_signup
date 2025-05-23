import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import re
from datetime import datetime

# Clean minimalist CSS with fast upward rockets
minimalist_css = """
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
  
  .stApp {
    background-color: #000000;
    font-family: 'Inter', sans-serif;
  }
  
  /* Fast moving rockets */
  .rocket {
    position: fixed;
    font-size: 24px;
    animation: rocket-up 2s linear infinite;
    z-index: 1000;
  }
  
  .rocket:nth-child(1) {
    left: 15%;
    animation-delay: 0s;
  }
  
  .rocket:nth-child(2) {
    left: 30%;
    animation-delay: 0.4s;
  }
  
  .rocket:nth-child(3) {
    left: 50%;
    animation-delay: 0.8s;
  }
  
  .rocket:nth-child(4) {
    left: 70%;
    animation-delay: 1.2s;
  }
  
  .rocket:nth-child(5) {
    left: 85%;
    animation-delay: 1.6s;
  }
  
  @keyframes rocket-up {
    0% {
      bottom: -50px;
      opacity: 0;
    }
    10% {
      opacity: 1;
    }
    90% {
      opacity: 1;
    }
    100% {
      bottom: 100vh;
      opacity: 0;
    }
  }
  
  /* Clean form container */
  .form-container {
    background-color: #ffffff;
    border-radius: 12px;
    padding: 3rem;
    max-width: 500px;
    margin: 5rem auto;
    box-shadow: 0 4px 20px rgba(255, 255, 255, 0.1);
    position: relative;
    z-index: 100;
  }
  
  .main-title {
    color: #000000;
    font-size: 2rem;
    font-weight: 600;
    text-align: center;
    margin-bottom: 0.5rem;
  }
  
  .subtitle {
    color: #666666;
    font-size: 1rem;
    text-align: center;
    margin-bottom: 2rem;
    font-weight: 300;
  }
  
  /* Success message */
  .success-message {
    background-color: #f0f9ff;
    border: 1px solid #0ea5e9;
    border-radius: 8px;
    padding: 1rem;
    text-align: center;
    color: #0c4a6e;
    margin: 2rem 0;
  }
  
  .success-icon {
    font-size: 2rem;
    margin-bottom: 0.5rem;
  }
</style>

<!-- 5 Fast Rockets -->
<div class="rocket">🚀</div>
<div class="rocket">🚀</div>
<div class="rocket">🚀</div>
<div class="rocket">🚀</div>
<div class="rocket">🚀</div>
"""

def validate_email(email):
    """Simple email validation"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def connect_to_sheets():
    """Connect to Google Sheets"""
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        service_account_info = st.secrets["gcp_service_account"]
        credentials = Credentials.from_service_account_info(service_account_info, scopes=scope)
        client = gspread.authorize(credentials)
        sheet = client.open("Newsletter Subscribers").sheet1
        return sheet, None
    except Exception as e:
        return None, str(e)

def main():
    # Apply CSS
    st.markdown(minimalist_css, unsafe_allow_html=True)
    
    # Form container
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    
    # Title
    st.markdown("""
    <h1 class="main-title">Newsletter</h1>
    <p class="subtitle">Subscribe for updates</p>
    """, unsafe_allow_html=True)
    
    # Session state for success
    if 'subscribed' not in st.session_state:
        st.session_state.subscribed = False
    if 'subscriber_name' not in st.session_state:
        st.session_state.subscriber_name = ""
    
    # Success message
    if st.session_state.subscribed:
        st.markdown(f"""
        <div class="success-message">
            <div class="success-icon">✓</div>
            <strong>Thanks, {st.session_state.subscriber_name}!</strong><br>
            You're subscribed.
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Subscribe another", type="secondary"):
            st.session_state.subscribed = False
            st.session_state.subscriber_name = ""
            st.rerun()
    else:
        # Simple form
        with st.form("subscribe_form", clear_on_submit=True):
            name = st.text_input("Name", placeholder="Your name")
            email = st.text_input("Email", placeholder="your@email.com")
            
            submitted = st.form_submit_button("Subscribe", type="primary", use_container_width=True)
            
            if submitted:
                # Validation
                if not name.strip():
                    st.error("Please enter your name")
                elif not validate_email(email):
                    st.error("Please enter a valid email")
                else:
                    # Connect to sheets
                    with st.spinner("Subscribing..."):
                        sheet, error = connect_to_sheets()
                        
                        if error:
                            st.error("Connection error. Please try again.")
                        else:
                            try:
                                # Check if email exists
                                existing_emails = sheet.col_values(2) if sheet.row_count > 0 else []
                                
                                if email.lower() in [e.lower() for e in existing_emails]:
                                    st.info("This email is already subscribed")
                                else:
                                    # Add subscriber
                                    sheet.append_row([name.strip(), email.lower().strip()])
                                    
                                    st.session_state.subscribed = True
                                    st.session_state.subscriber_name = name.strip()
                                    st.rerun()
                                    
                            except Exception as e:
                                st.error("Error subscribing. Please try again.")
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()

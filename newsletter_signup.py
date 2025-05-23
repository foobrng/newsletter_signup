import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import re
from datetime import datetime

# Realistic rocket launch CSS with smoke trails
rocket_launch_css = """
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
  
  .stApp {
    background-color: #000000;
    font-family: 'Inter', sans-serif;
  }
  
  /* Hide Streamlit header */
  header[data-testid="stHeader"] {
    display: none;
  }
  
  /* Rocket with smoke trail */
  .rocket-container {
    position: fixed;
    z-index: 1000;
    pointer-events: none;
  }
  
  .rocket {
    position: relative;
    font-size: 28px;
    filter: drop-shadow(0 0 8px rgba(255, 150, 0, 0.8));
  }
  
  .smoke-trail {
    position: absolute;
    top: 35px;
    left: 50%;
    transform: translateX(-50%);
    width: 4px;
    background: linear-gradient(to bottom, 
      rgba(255, 100, 0, 0.9) 0%,
      rgba(255, 150, 0, 0.7) 20%,
      rgba(200, 200, 200, 0.5) 40%,
      rgba(150, 150, 150, 0.3) 60%,
      rgba(100, 100, 100, 0.1) 80%,
      transparent 100%);
    border-radius: 2px;
    animation: trail-flicker 0.15s ease-in-out infinite alternate;
  }
  
  @keyframes trail-flicker {
    0% { 
      height: 60px; 
      opacity: 0.8;
      width: 4px;
    }
    100% { 
      height: 80px; 
      opacity: 1;
      width: 6px;
    }
  }
  
  /* Individual rocket animations with natural movement */
  .rocket-1 {
    left: 12%;
    animation: launch-1 4.2s ease-out infinite;
  }
  
  .rocket-2 {
    left: 28%;
    animation: launch-2 3.8s ease-out infinite;
  }
  
  .rocket-3 {
    left: 48%;
    animation: launch-3 4.5s ease-out infinite;
  }
  
  .rocket-4 {
    left: 68%;
    animation: launch-4 3.9s ease-out infinite;
  }
  
  .rocket-5 {
    left: 84%;
    animation: launch-5 4.1s ease-out infinite;
  }
  
  @keyframes launch-1 {
    0% { bottom: -80px; opacity: 0; transform: rotate(-5deg) scale(0.8); }
    8% { opacity: 1; transform: rotate(0deg) scale(1); }
    15% { transform: rotate(2deg); }
    30% { transform: rotate(-1deg); }
    45% { transform: rotate(1deg); }
    70% { opacity: 1; }
    100% { bottom: 100vh; opacity: 0; transform: rotate(0deg) scale(0.9); }
  }
  
  @keyframes launch-2 {
    0% { bottom: -80px; opacity: 0; transform: rotate(3deg) scale(0.9); }
    12% { opacity: 1; transform: rotate(0deg) scale(1); }
    25% { transform: rotate(-2deg); }
    40% { transform: rotate(1deg); }
    60% { transform: rotate(-1deg); }
    85% { opacity: 1; }
    100% { bottom: 100vh; opacity: 0; transform: rotate(2deg) scale(0.8); }
  }
  
  @keyframes launch-3 {
    0% { bottom: -80px; opacity: 0; transform: rotate(-2deg) scale(1.1); }
    6% { opacity: 1; transform: rotate(1deg) scale(1); }
    20% { transform: rotate(-1deg); }
    35% { transform: rotate(2deg); }
    55% { transform: rotate(0deg); }
    80% { opacity: 1; }
    100% { bottom: 100vh; opacity: 0; transform: rotate(-1deg) scale(0.9); }
  }
  
  @keyframes launch-4 {
    0% { bottom: -80px; opacity: 0; transform: rotate(4deg) scale(0.7); }
    10% { opacity: 1; transform: rotate(0deg) scale(1); }
    18% { transform: rotate(-3deg); }
    32% { transform: rotate(1deg); }
    48% { transform: rotate(-1deg); }
    75% { opacity: 1; }
    100% { bottom: 100vh; opacity: 0; transform: rotate(2deg) scale(1.1); }
  }
  
  @keyframes launch-5 {
    0% { bottom: -80px; opacity: 0; transform: rotate(-3deg) scale(0.9); }
    14% { opacity: 1; transform: rotate(1deg) scale(1); }
    28% { transform: rotate(2deg); }
    42% { transform: rotate(-2deg); }
    65% { transform: rotate(0deg); }
    90% { opacity: 1; }
    100% { bottom: 100vh; opacity: 0; transform: rotate(-1deg) scale(0.8); }
  }
  
  /* Glitch effect for title */
  .glitch-title {
    color: #ffffff;
    font-size: 2.5rem;
    font-weight: 600;
    text-align: center;
    margin-bottom: 0.5rem;
    position: relative;
    animation: glitch-skew 2s infinite linear alternate-reverse;
  }
  
  .glitch-title::before,
  .glitch-title::after {
    content: attr(data-text);
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
  }
  
  .glitch-title::before {
    animation: glitch-anim 2s infinite linear alternate-reverse;
    color: #ff0040;
    z-index: -1;
  }
  
  .glitch-title::after {
    animation: glitch-anim2 1s infinite linear alternate-reverse;
    color: #00ff41;
    z-index: -2;
  }
  
  @keyframes glitch-anim {
    0% { clip: rect(64px, 9999px, 66px, 0); }
    5% { clip: rect(30px, 9999px, 36px, 0); }
    10% { clip: rect(87px, 9999px, 91px, 0); }
    15% { clip: rect(42px, 9999px, 43px, 0); }
    20% { clip: rect(17px, 9999px, 18px, 0); }
    25% { clip: rect(68px, 9999px, 72px, 0); }
    30% { clip: rect(23px, 9999px, 24px, 0); }
    35% { clip: rect(54px, 9999px, 58px, 0); }
    40% { clip: rect(12px, 9999px, 15px, 0); }
    45% { clip: rect(37px, 9999px, 41px, 0); }
    50% { clip: rect(82px, 9999px, 86px, 0); }
    55% { clip: rect(29px, 9999px, 33px, 0); }
    60% { clip: rect(71px, 9999px, 75px, 0); }
    65% { clip: rect(48px, 9999px, 52px, 0); }
    70% { clip: rect(19px, 9999px, 23px, 0); }
    75% { clip: rect(63px, 9999px, 67px, 0); }
    80% { clip: rect(34px, 9999px, 38px, 0); }
    85% { clip: rect(76px, 9999px, 80px, 0); }
    90% { clip: rect(15px, 9999px, 19px, 0); }
    95% { clip: rect(59px, 9999px, 63px, 0); }
    100% { clip: rect(26px, 9999px, 30px, 0); }
  }
  
  @keyframes glitch-anim2 {
    0% { clip: rect(25px, 9999px, 28px, 0); }
    5% { clip: rect(73px, 9999px, 77px, 0); }
    10% { clip: rect(46px, 9999px, 50px, 0); }
    15% { clip: rect(11px, 9999px, 15px, 0); }
    20% { clip: rect(81px, 9999px, 85px, 0); }
    25% { clip: rect(38px, 9999px, 42px, 0); }
    30% { clip: rect(65px, 9999px, 69px, 0); }
    35% { clip: rect(22px, 9999px, 26px, 0); }
    40% { clip: rect(58px, 9999px, 62px, 0); }
    45% { clip: rect(33px, 9999px, 37px, 0); }
    50% { clip: rect(79px, 9999px, 83px, 0); }
    55% { clip: rect(14px, 9999px, 18px, 0); }
    60% { clip: rect(52px, 9999px, 56px, 0); }
    65% { clip: rect(27px, 9999px, 31px, 0); }
    70% { clip: rect(74px, 9999px, 78px, 0); }
    75% { clip: rect(41px, 9999px, 45px, 0); }
    80% { clip: rect(69px, 9999px, 73px, 0); }
    85% { clip: rect(16px, 9999px, 20px, 0); }
    90% { clip: rect(85px, 9999px, 89px, 0); }
    95% { clip: rect(31px, 9999px, 35px, 0); }
    100% { clip: rect(57px, 9999px, 61px, 0); }
  }
  
  @keyframes glitch-skew {
    0% { transform: skew(0deg); }
    10% { transform: skew(-1deg); }
    20% { transform: skew(0.5deg); }
    30% { transform: skew(-0.5deg); }
    40% { transform: skew(0deg); }
    50% { transform: skew(1deg); }
    60% { transform: skew(-0.8deg); }
    70% { transform: skew(0.3deg); }
    80% { transform: skew(-0.2deg); }
    90% { transform: skew(0.1deg); }
    100% { transform: skew(0deg); }
  }
  
  /* Form container */
  .form-container {
    background-color: #ffffff;
    border-radius: 12px;
    padding: 3rem;
    max-width: 500px;
    margin: 3rem auto;
    box-shadow: 0 8px 32px rgba(255, 255, 255, 0.1);
    position: relative;
    z-index: 100;
  }
  
  .subtitle {
    color: #666666;
    font-size: 1rem;
    text-align: center;
    margin-bottom: 2rem;
    font-weight: 300;
  }
  
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

<!-- 5 Rockets with smoke trails and random delays -->
<div class="rocket-container rocket-1">
  <div class="rocket">🚀</div>
  <div class="smoke-trail"></div>
</div>

<div class="rocket-container rocket-2">
  <div class="rocket">🚀</div>
  <div class="smoke-trail"></div>
</div>

<div class="rocket-container rocket-3">
  <div class="rocket">🚀</div>
  <div class="smoke-trail"></div>
</div>

<div class="rocket-container rocket-4">
  <div class="rocket">🚀</div>
  <div class="smoke-trail"></div>
</div>

<div class="rocket-container rocket-5">
  <div class="rocket">🚀</div>
  <div class="smoke-trail"></div>
</div>
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
    st.markdown(rocket_launch_css, unsafe_allow_html=True)
    
    # Glitch title
    st.markdown("""
    <h1 class="glitch-title" data-text="T̶h̴o̴u̷g̸h̸t̵s̵ & O̵t̴h̸e̴r̸ G̸l̵i̶t̵c̴h̶e̷s̸">T̶h̴o̴u̷g̸h̸t̵s̵ & O̵t̴h̸e̴r̸ G̸l̵i̶t̵c̴h̶e̷s̸</h1>
    """, unsafe_allow_html=True)
    
    # Form container
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    
    st.markdown('<p class="subtitle">Subscribe for updates</p>', unsafe_allow_html=True)
    
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

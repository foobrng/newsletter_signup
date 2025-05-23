import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import re
from datetime import datetime
import time

# Enhanced CSS with Streamlit-compatible animations
animations_css = """
<style>
  @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
  
  .stApp {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    font-family: 'Poppins', sans-serif;
  }
  
  /* Simple floating animation that works in Streamlit */
  .floating-element {
    position: relative;
    animation: gentle-float 4s ease-in-out infinite;
  }
  
  @keyframes gentle-float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
  }
  
  /* Simple rocket that moves across screen */
  .rocket-animation {
    position: fixed;
    top: 20px;
    left: -60px;
    z-index: 1000;
    animation: simple-fly 8s linear infinite;
    font-size: 30px;
  }
  
  @keyframes simple-fly {
    0% { 
      left: -60px; 
      transform: rotate(0deg);
      opacity: 0;
    }
    10% {
      opacity: 1;
    }
    90% {
      opacity: 1;
    }
    100% { 
      left: calc(100vw + 60px); 
      transform: rotate(15deg);
      opacity: 0;
    }
  }
  
  /* Pulsing background elements */
  .pulse-bg {
    position: fixed;
    width: 100px;
    height: 100px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.1);
    animation: pulse-fade 6s ease-in-out infinite;
    pointer-events: none;
  }
  
  .pulse-bg:nth-child(1) {
    top: 10%;
    left: 80%;
    animation-delay: 0s;
  }
  
  .pulse-bg:nth-child(2) {
    top: 70%;
    left: 10%;
    animation-delay: 2s;
  }
  
  .pulse-bg:nth-child(3) {
    top: 40%;
    left: 70%;
    animation-delay: 4s;
  }
  
  @keyframes pulse-fade {
    0%, 100% { 
      transform: scale(0.8);
      opacity: 0.1;
    }
    50% { 
      transform: scale(1.2);
      opacity: 0.3;
    }
  }
  
  /* Enhanced form styling */
  .main-container {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 20px;
    padding: 2rem;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(10px);
    margin: 2rem 0;
    position: relative;
    z-index: 3;
  }
  
  .title-container {
    text-align: center;
    margin-bottom: 2rem;
  }
  
  .main-title {
    background: linear-gradient(135deg, #667eea, #764ba2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    animation: title-glow 3s ease-in-out infinite alternate;
  }
  
  @keyframes title-glow {
    0% { filter: drop-shadow(0 0 5px rgba(102, 126, 234, 0.3)); }
    100% { filter: drop-shadow(0 0 15px rgba(118, 75, 162, 0.6)); }
  }
  
  .subtitle {
    color: #666;
    font-size: 1.1rem;
    font-weight: 300;
  }
  
  /* Success animation */
  .success-animation {
    text-align: center;
    animation: bounce-in 0.6s ease-out;
  }
  
  @keyframes bounce-in {
    0% { transform: scale(0.3); opacity: 0; }
    50% { transform: scale(1.05); }
    70% { transform: scale(0.9); }
    100% { transform: scale(1); opacity: 1; }
  }
  
  .success-icon {
    font-size: 4rem;
    color: #27ae60;
    margin-bottom: 1rem;
    animation: rotate-success 2s ease-in-out;
  }
  
  @keyframes rotate-success {
    0% { transform: rotate(0deg) scale(0); }
    50% { transform: rotate(180deg) scale(1.2); }
    100% { transform: rotate(360deg) scale(1); }
  }
</style>

<!-- Simple background animations -->
<div class="pulse-bg"></div>
<div class="pulse-bg"></div>
<div class="pulse-bg"></div>

<!-- Simple rocket animation -->
<div class="rocket-animation">🚀</div>
"""

def validate_email(email):
    """Enhanced email validation using regex"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_name(name):
    """Validate name - check for reasonable length and characters"""
    if len(name.strip()) < 2:
        return False, "Name must be at least 2 characters long"
    if len(name.strip()) > 50:
        return False, "Name must be less than 50 characters"
    if not re.match(r'^[a-zA-Z\s\'-]+$', name.strip()):
        return False, "Name can only contain letters, spaces, hyphens, and apostrophes"
    return True, ""

def connect_to_sheets():
    """Connect to Google Sheets with error handling"""
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
    # Apply custom CSS
    st.markdown(animations_css, unsafe_allow_html=True)
    
    # Main container
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Title section with floating animation
    st.markdown("""
    <div class="title-container floating-element">
        <h1 class="main-title">🚀 Join Our Newsletter</h1>
        <p class="subtitle">Stay updated with the latest news, tips, and exclusive content!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state for success message
    if 'subscription_success' not in st.session_state:
        st.session_state.subscription_success = False
    if 'success_name' not in st.session_state:
        st.session_state.success_name = ""
    
    # Show success animation if subscription was successful
    if st.session_state.subscription_success:
        st.markdown("""
        <div class="success-animation">
            <div class="success-icon">✅</div>
            <h2 style="color: #27ae60;">Welcome aboard!</h2>
            <p style="color: #666;">Thanks for subscribing, {}! Check your email for a confirmation.</p>
        </div>
        """.format(st.session_state.success_name), unsafe_allow_html=True)
        
        # Reset success state after showing
        if st.button("Subscribe Another Email", type="secondary"):
            st.session_state.subscription_success = False
            st.session_state.success_name = ""
            st.rerun()
    else:
        # Subscription form
        with st.form("newsletter_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Full Name", placeholder="Enter your full name")
            
            with col2:
                email = st.text_input("Email Address", placeholder="your.email@example.com")
            
            # Optional preferences
            st.markdown("### 📧 Email Preferences (Optional)")
            col3, col4 = st.columns(2)
            
            with col3:
                frequency = st.selectbox("Email Frequency", 
                                       ["Weekly", "Bi-weekly", "Monthly"], 
                                       index=0)
            
            with col4:
                topics = st.multiselect("Interested Topics", 
                                      ["Technology", "Business", "Health", "Lifestyle", "News"],
                                      default=["Technology"])
            
            # Marketing consent
            marketing_consent = st.checkbox("I agree to receive marketing emails and can unsubscribe at any time")
            
            submitted = st.form_submit_button("🚀 Subscribe Now", type="primary", use_container_width=True)
            
            if submitted:
                # Validation
                name_valid, name_error = validate_name(name)
                
                if not name_valid:
                    st.error(f"❌ {name_error}")
                elif not validate_email(email):
                    st.error("❌ Please enter a valid email address (e.g., user@example.com)")
                elif not marketing_consent:
                    st.warning("⚠️ Please agree to receive marketing emails to subscribe")
                else:
                    # Try to connect to Google Sheets
                    with st.spinner("🔄 Processing your subscription..."):
                        sheet, error = connect_to_sheets()
                        
                        if error:
                            st.error(f"❌ Connection error: {error}")
                            st.info("💡 Please try again in a moment or contact support if the problem persists")
                        else:
                            try:
                                # Check for existing subscription
                                existing_emails = sheet.col_values(2) if sheet.row_count > 0 else []
                                
                                if email.lower() in [e.lower() for e in existing_emails]:
                                    st.info("ℹ️ This email is already subscribed to our newsletter!")
                                else:
                                    # Add new subscriber with timestamp and preferences
                                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                    topics_str = ", ".join(topics) if topics else "None selected"
                                    
                                    sheet.append_row([
                                        name.strip(),
                                        email.lower().strip(),
                                        current_time,
                                        frequency,
                                        topics_str,
                                        "Yes" if marketing_consent else "No"
                                    ])
                                    
                                    # Set success state
                                    st.session_state.subscription_success = True
                                    st.session_state.success_name = name.strip()
                                    st.rerun()
                                    
                            except Exception as e:
                                st.error(f"❌ Error saving subscription: {str(e)}")
                                st.info("💡 Please try again or contact support if the problem persists")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; color: rgba(255,255,255,0.7); padding: 1rem;">
            <p>🔒 Your privacy is important to us. We'll never share your information.</p>
            <p style="font-size: 0.8rem;">Made with ❤️ using Streamlit</p>
        </div>
        """, 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()

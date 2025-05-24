import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import re

# Clean CSS with smoke trails only
clean_css = """
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
  
  .stApp {
    background-color: #000000;
    color: #ffffff;
    font-family: 'Inter', sans-serif;
  }
  
  /* Hide empty containers - enhanced */
  .block-container {
    padding-top: 0.5rem !important;
  }
  
  /* Aggressive empty container hiding */
  .element-container:empty,
  div[data-testid="element-container"]:empty,
  .block-container > div:empty,
  .stApp > div:empty,
  .main > div:empty,
  div[class*="css"]:empty,
  div[class*="st-"]:empty {
    display: none !important;
  }
  
  /* Hide containers with minimal content */
  .element-container:not(:has(input)):not(:has(button)):not(:has(form)):not(:has(h1)):not(:has(p)):not(:has(div[class*="success"])) {
    min-height: 0 !important;
    height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
    display: none !important;
  }
  
  /* Target specific Streamlit containers that might be empty */
  div[data-testid="column"],
  div[data-testid="block-container"] > div:first-child:empty,
  div[class*="css"][class*="e1f1d6gn"] {
    display: none !important;
  }
  
  /* Hide any div that's taking up space but has no visible content */
  div:not([class*="form"]):not([class*="trail"]):not([class*="smoke"]):empty {
    display: none !important;
  }
  
  /* Moving smoke trails */
  .trail-container {
    position: fixed;
    z-index: 1000;
    pointer-events: none;
  }
  
  .smoke-trail {
    position: absolute;
    width: 4px;
    height: 60px;
    background: linear-gradient(to bottom, 
      rgba(150, 150, 150, 0.8) 0%,
      rgba(100, 100, 100, 0.6) 40%,
      rgba(50, 50, 50, 0.3) 80%,
      transparent 100%);
    border-radius: 2px;
  }
  
  @keyframes trail-move {
    0% { 
      bottom: -80px; 
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
  
  @keyframes trail-flicker {
    0% { 
      width: 3px;
      opacity: 0.6;
    }
    100% { 
      width: 5px;
      opacity: 0.9;
    }
  }
  
  /* Trail positions with independent timing */
  .trail-1 {
    left: 15%;
    animation: trail-move 3.2s linear infinite, trail-flicker 0.3s ease-in-out infinite alternate;
    animation-delay: 0s;
  }
  
  .trail-2 {
    left: 30%;
    animation: trail-move 2.8s linear infinite, trail-flicker 0.4s ease-in-out infinite alternate;
    animation-delay: 0.8s;
  }
  
  .trail-3 {
    left: 50%;
    animation: trail-move 3.5s linear infinite, trail-flicker 0.25s ease-in-out infinite alternate;
    animation-delay: 1.6s;
  }
  
  .trail-4 {
    left: 70%;
    animation: trail-move 2.9s linear infinite, trail-flicker 0.35s ease-in-out infinite alternate;
    animation-delay: 0.4s;
  }
  
  .trail-5 {
    left: 85%;
    animation: trail-move 3.1s linear infinite, trail-flicker 0.3s ease-in-out infinite alternate;
    animation-delay: 2.2s;
  }
  
  /* Clean title - adjusted positioning */
  .clean-title {
    color: #ffffff;
    font-size: 2.5rem;
    font-weight: 600;
    text-align: center;
    margin: 1.5rem 0 1rem 0;
  }
  
  .subtitle {
    color: #888888;
    font-size: 1rem;
    text-align: center;
    margin-bottom: 5rem;
    font-weight: 300;
  }
  
  /* Form container and styling */
  .form-container {
    max-width: 600px;
    margin: 2rem auto;
    padding: 3rem;
    background-color: #111111;
    border: 1px solid #333333;
    border-radius: 12px;
  }
  
  .stForm {
    max-width: 100%;
  }
  
  .success-message {
    background-color: #222222;
    border: 1px solid #555555;
    border-radius: 8px;
    padding: 2rem;
    text-align: center;
    color: #ffffff;
    margin: 2rem auto;
    max-width: 600px;
  }
  
  .success-icon {
    font-size: 2rem;
    margin-bottom: 0.5rem;
    color: #ffffff;
  }
  
  /* Input styling */
  .stTextInput > div > div > input {
    background-color: #222222;
    color: #ffffff;
    border: 1px solid #444444;
  }
  
  .stTextInput > div > div > input:focus {
    border-color: #666666;
    box-shadow: 0 0 0 1px #666666;
  }
  
  /* Button styling */
  .stButton > button {
    background-color: #ffffff;
    color: #000000;
    border: none;
    font-weight: 500;
  }
  
  .stButton > button:hover {
    background-color: #e5e5e5;
    color: #000000;
  }
</style>

<!-- Smoke trails -->
<div class="trail-container trail-1">
  <div class="smoke-trail"></div>
</div>

<div class="trail-container trail-2">
  <div class="smoke-trail"></div>
</div>

<div class="trail-container trail-3">
  <div class="smoke-trail"></div>
</div>

<div class="trail-container trail-4">
  <div class="smoke-trail"></div>
</div>

<div class="trail-container trail-5">
  <div class="smoke-trail"></div>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    // More aggressive empty div removal
    function hideEmptyElements() {
        // Target all potential empty containers
        const selectors = [
            'div:empty',
            'div[class*="css"]:empty',
            'div[data-testid="element-container"]:empty',
            'div[data-testid="column"]',
            '.block-container > div:first-child:empty'
        ];
        
        selectors.forEach(selector => {
            const elements = document.querySelectorAll(selector);
            elements.forEach(el => {
                if (el.textContent.trim() === '' && !el.querySelector('input, button, form, h1, p')) {
                    el.style.display = 'none';
                    el.style.height = '0';
                    el.style.margin = '0';
                    el.style.padding = '0';
                }
            });
        });
        
        // Also hide any div that's taking up vertical space but appears empty
        const allDivs = document.querySelectorAll('div');
        allDivs.forEach(div => {
            const rect = div.getBoundingClientRect();
            const hasContent = div.textContent.trim() !== '' || 
                             div.querySelector('input, button, form, h1, p, img, svg') ||
                             div.classList.contains('trail-container') ||
                             div.classList.contains('smoke-trail');
            
            if (rect.height > 20 && !hasContent && 
                !div.closest('.form-container') && 
                !div.closest('.success-message')) {
                div.style.display = 'none';
            }
        });
    }
    
    // Run immediately and after a delay
    hideEmptyElements();
    setTimeout(hideEmptyElements, 100);
    setTimeout(hideEmptyElements, 500);
});
</script>
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
    st.markdown(clean_css, unsafe_allow_html=True)
    
    # Clean title
    st.markdown('<h1 class="clean-title">Thoughts & Other Glitches</h1>', unsafe_allow_html=True)
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
        # Form container
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        
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

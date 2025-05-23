import streamlit as st

rocket_animation_svg = """
<style>
  #rocket-bg {
    position: fixed;
    top: 0; left: 0;
    width: 100vw;
    height: 100vh;
    pointer-events: none;
    overflow: hidden;
    z-index: -1;
    background: #0b0c10;
  }

  .rocket {
    position: absolute;
    width: 30px;
    height: 60px;
    fill: white;
    animation-name: fly-across;
    animation-timing-function: linear;
    animation-iteration-count: infinite;
  }

  /* Flame container below rocket */
  .flame {
    position: absolute;
    bottom: -12px;
    left: 50%;
    transform: translateX(-50%);
    width: 12px;
    height: 20px;
    filter: drop-shadow(0 0 3px orange);
    animation-name: flame-flicker;
    animation-duration: 0.6s;
    animation-iteration-count: infinite;
    animation-direction: alternate;
  }

  /* Flame flicker animation */
  @keyframes flame-flicker {
    0%   { transform: translateX(-50%) scaleY(1) scaleX(1); opacity: 1; }
    50%  { transform: translateX(-50%) scaleY(1.2) scaleX(0.9); opacity: 0.8; }
    100% { transform: translateX(-50%) scaleY(1) scaleX(1); opacity: 1; }
  }

  @keyframes fly-across {
    0% {
      left: -40px;
      top: var(--start-top);
      opacity: 0;
      transform: translateY(0) rotate(0deg);
    }
    10% {
      opacity: 1;
    }
    100% {
      left: 100vw;
      top: var(--start-top);
      opacity: 0;
      transform: translateY(-30px) rotate(360deg);
    }
  }
</style>

<div id="rocket-bg">
  <div class="rocket" style="--start-top:10vh; animation-duration: 12s; animation-delay: 0s;">
    <svg viewBox="0 0 64 128" xmlns="http://www.w3.org/2000/svg" width="30" height="60" fill="white" stroke="white" stroke-width="1" stroke-linejoin="round">
      <path d="M32 0 L20 48 L32 40 L44 48 Z" />
      <rect x="24" y="48" width="16" height="40" rx="6" ry="6" />
      <circle cx="32" cy="96" r="10" />
    </svg>
    <svg class="flame" viewBox="0 0 32 64" xmlns="http://www.w3.org/2000/svg" fill="orange" stroke="orangered" stroke-width="1" stroke-linejoin="round">
      <path d="M16 0 C10 20, 6 40, 16 64 C26 40, 22 20, 16 0 Z"/>
    </svg>
  </div>

  <div class="rocket" style="--start-top:30vh; animation-duration: 15s; animation-delay: 5s;">
    <svg viewBox="0 0 64 128" xmlns="http://www.w3.org/2000/svg" width="30" height="60" fill="white" stroke="white" stroke-width="1" stroke-linejoin="round">
      <path d="M32 0 L20 48 L32 40 L44 48 Z" />
      <rect x="24" y="48" width="16" height="40" rx="6" ry="6" />
      <circle cx="32" cy="96" r="10" />
    </svg>
    <svg class="flame" viewBox="0 0 32 64" xmlns="http://www.w3.org/2000/svg" fill="orange" stroke="orangered" stroke-width="1" stroke-linejoin="round">
      <path d="M16 0 C10 20, 6 40, 16 64 C26 40, 22 20, 16 0 Z"/>
    </svg>
  </div>

  <div class="rocket" style="--start-top:50vh; animation-duration: 18s; animation-delay: 2s;">
    <svg viewBox="0 0 64 128" xmlns="http://www.w3.org/2000/svg" width="30" height="60" fill="white" stroke="white" stroke-width="1" stroke-linejoin="round">
      <path d="M32 0 L20 48 L32 40 L44 48 Z" />
      <rect x="24" y="48" width="16" height="40" rx="6" ry="6" />
      <circle cx="32" cy="96" r="10" />
    </svg>
    <svg class="flame" viewBox="0 0 32 64" xmlns="http://www.w3.org/2000/svg" fill="orange" stroke="orangered" stroke-width="1" stroke-linejoin="round">
      <path d="M16 0 C10 20, 6 40, 16 64 C26 40, 22 20, 16 0 Z"/>
    </svg>
  </div>

  <div class="rocket" style="--start-top:70vh; animation-duration: 20s; animation-delay: 7s;">
    <svg viewBox="0 0 64 128" xmlns="http://www.w3.org/2000/svg" width="30" height="60" fill="white" stroke="white" stroke-width="1" stroke-linejoin="round">
      <path d="M32 0 L20 48 L32 40 L44 48 Z" />
      <rect x="24" y="48" width="16" height="40" rx="6" ry="6" />
      <circle cx="32" cy="96" r="10" />
    </svg>
    <svg class="flame" viewBox="0 0 32 64" xmlns="http://www.w3.org/2000/svg" fill="orange" stroke="orangered" stroke-width="1" stroke-linejoin="round">
      <path d="M16 0 C10 20, 6 40, 16 64 C26 40, 22 20, 16 0 Z"/>
    </svg>
  </div>

  <div class="rocket" style="--start-top:85vh; animation-duration: 14s; animation-delay: 3s;">
    <svg viewBox="0 0 64 128" xmlns="http://www.w3.org/2000/svg" width="30" height="60" fill="white" stroke="white" stroke-width="1" stroke-linejoin="round">
      <path d="M32 0 L20 48 L32 40 L44 48 Z" />
      <rect x="24" y="48" width="16" height="40" rx="6" ry="6" />
      <circle cx="32" cy="96" r="10" />
    </svg>
    <svg class="flame" viewBox="0 0 32 64" xmlns="http://www.w3.org/2000/svg" fill="orange" stroke="orangered" stroke-width="1" stroke-linejoin="round">
      <path d="M16 0 C10 20, 6 40, 16 64 C26 40, 22 20, 16 0 Z"/>
    </svg>
  </div>
</div>
"""

st.markdown(rocket_animation_svg, unsafe_allow_html=True)

import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.title("Newsletter Signup")

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("email-collector-460721-110f16bcb9c7.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Newsletter Subscribers").sheet1

name = st.text_input("Enter your name")
email = st.text_input("Enter your email")

if st.button("Subscribe"):
    if not name.strip():
        st.error("Please enter your name.")
    elif "@" not in email or "." not in email:
        st.error("Please enter a valid email address.")
    else:
        # Check if email already exists
        existing_emails = sheet.col_values(2)  # emails are now in column 2
        if email not in existing_emails:
            # Append both name and email
            sheet.append_row([name, email])
            st.success(f"Thanks for subscribing, {name}!")
        else:
            st.info("This email is already subscribed.")

import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Join Our Newsletter", page_icon="📬")

st.title("📬 Stay in the Loop!")
st.write("Subscribe to our newsletter and get updates straight to your inbox.")

email = st.text_input("Enter your email address")

if st.button("Subscribe"):
    if "@" in email and "." in email:
        # Load existing data or create new
        filename = "emails.csv"
        if os.path.exists(filename):
            df = pd.read_csv(filename)
        else:
            df = pd.DataFrame(columns=["email"])

        if email not in df["email"].values:
            df = pd.concat([df, pd.DataFrame([{"email": email}])], ignore_index=True)
            df.to_csv(filename, index=False)
            st.success("Thanks for subscribing!")
        else:
            st.info("You're already subscribed.")
    else:
        st.error("Please enter a valid email address.")

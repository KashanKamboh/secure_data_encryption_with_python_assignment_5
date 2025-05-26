# import streamlit as st
# import hashlib
# from cryptography.fernet import Fernet

# # 🔐 Setup: Key & Cipher
# KEY = Fernet.generate_key()
# cipher = Fernet(KEY)


# # 📦 Memory Storage
# stored_data = {}  # {"encrypted_text": {"encrypted_text": ..., "passkey": hashed_passkey}}
# failed_attempts = 0  # Track failed attempts


# # 🔑 Utility: Hash Passkey
# def hash_passkey(passkey):
#     return hashlib.sha256(passkey.encode()).hexdigest()


# # 🔐 Utility: Encrypt Data
# def encrypt_data(text):
#     return cipher.encrypt(text.encode()).decode()


# # 🔓 Utility: Decrypt Data
# def decrypt_data(encrypted_text, passkey):
#     global failed_attempts
#     hashed = hash_passkey(passkey)

#     if encrypted_text in stored_data:
#         entry = stored_data[encrypted_text]
#         if entry["passkey"] == hashed:
#             failed_attempts = 0  # reset after successful login
#             return cipher.decrypt(encrypted_text.encode()).decode()

#     # If not found or wrong passkey
#     failed_attempts += 1
#     return None


# # 🌐 Streamlit App
# st.set_page_config(page_title="Secure Data App", layout="centered")
# st.title("🛡️ Secure Data Encryption System")

# # 🚥 Navigation Menu
# menu = ["Home", "Store Data", "Retrieve Data", "Login"]
# choice = st.sidebar.selectbox("Choose Page", menu)


# # 🏠 HOME PAGE
# if choice == "Home":
#     st.subheader("🏠 Welcome")
#     st.write("Use this app to **securely store and retrieve your data** using encryption and passkeys.")


# # 💾 STORE DATA PAGE
# elif choice == "Store Data":
#     st.subheader("📂 Store New Data")
#     data = st.text_area("Enter Text to Encrypt:")
#     passkey = st.text_input("Set Your Passkey:", type="password")

#     if st.button("Encrypt & Save"):
#         if data and passkey:
#             hashed = hash_passkey(passkey)
#             encrypted = encrypt_data(data)
#             stored_data[encrypted] = {"encrypted_text": encrypted, "passkey": hashed}
#             st.success("✅ Data encrypted and saved successfully!")
#             st.code(encrypted, language="text")
#         else:
#             st.error("⚠️ Both fields are required!")

# # 🔓 RETRIEVE DATA PAGE
# elif choice == "Retrieve Data":
#     st.subheader("🔍 Retrieve Your Data")
#     encrypted_input = st.text_area("Paste Encrypted Data:")
#     passkey = st.text_input("Enter Your Passkey:", type="password")

#     if st.button("Decrypt"):
#         if encrypted_input and passkey:
#             result = decrypt_data(encrypted_input, passkey)
#             if result:
#                 st.success("✅ Decrypted Data:")
#                 st.code(result)
#             else:
#                 remaining = max(0, 3 - failed_attempts)
#                 st.error(f"❌ Incorrect passkey! Attempts left: {remaining}")
#                 if failed_attempts >= 3:
#                     st.warning("🔒 Too many failed attempts! Please reauthorize.")
#                     st.experimental_rerun()
#         else:
#             st.error("⚠️ Both fields are required!")


# # 🔐 LOGIN PAGE
# elif choice == "Login":
#     st.subheader("🔑 Reauthorization Required")
#     login_pass = st.text_input("Enter Admin Password:", type="password")

#     if st.button("Login"):
#         if login_pass == "admin123":  # Hardcoded admin password
#             failed_attempts = 0
#             st.success("✅ Reauthorized successfully! You can now try again.")
#         else:
#             st.error("❌ Incorrect password!")


import streamlit as st
import hashlib
import json
import os
from cryptography.fernet import Fernet

# ---------- File Paths ----------
KEY_FILE = "secret.key"
DATA_FILE = "data.json"

# ---------- Load or Generate Fernet Key ----------
def load_or_create_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            return f.read()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
        return key

# ---------- Load or Create Data File ----------
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    else:
        return {}

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(stored_data, f)

# ---------- Setup Encryption ----------
KEY = load_or_create_key()
cipher = Fernet(KEY)

# ---------- Load Stored Data ----------
stored_data = load_data()
failed_attempts = 0

# ---------- Utility Functions ----------
def hash_passkey(passkey):
    return hashlib.sha256(passkey.encode()).hexdigest()

def encrypt_data(text):
    return cipher.encrypt(text.encode()).decode()

def decrypt_data(encrypted_text, passkey):
    global failed_attempts
    hashed = hash_passkey(passkey)

    if encrypted_text in stored_data:
        entry = stored_data[encrypted_text]
        if entry["passkey"] == hashed:
            failed_attempts = 0
            return cipher.decrypt(encrypted_text.encode()).decode()

    failed_attempts += 1
    return None

# ---------- Streamlit UI ----------
st.set_page_config(page_title="Secure Data App", layout="centered")
# ---------- Custom Styling ----------
# st.markdown("""
#     <style>
#         /* Whole app background and text */
#         .stApp {
#             background-color: #f3e5f5 !important;  /* light purple */
#             color: black !important;
#         }

#         /* Sidebar background and text */
#         section[data-testid="stSidebar"] {
#             background-color: #f3e5f5 !important;
#             color: black !important;
#         }

#         /* Input fields and text areas */
#         input, textarea, .stTextInput input, .stTextArea textarea {
#             background-color: #f3e5f5 !important;
#             color: black !important;
#             border: 1px solid #ab47bc !important;
#         }

#         /* Strong placeholder color override for inputs and textareas */
#         input::placeholder,
#         textarea::placeholder,
#         .stTextInput input::placeholder,
#         .stTextArea textarea::placeholder {
#             color: black !important;
#             opacity: 1 !important;  /* force visibility */
#         }

#         /* Button styling */
#         .stButton > button {
#             background-color: #ce93d8 !important;
#             color: black !important;
#             border: none !important;
#         }

#         /* Code block styling */
#         code {
#             background-color: #e1bee7 !important;
#             color: black !important;
#         }
#     </style>
# """, unsafe_allow_html=True)




st.title("🛡️ Secure Data Encryption System")

menu = ["Home", "Store Data", "Retrieve Data", "Login"]
choice = st.sidebar.selectbox("Choose Page", menu)

# 🏠 Home Page
if choice == "Home":
    st.subheader("🏠 Welcome")
    st.write("Use this app to **securely store and retrieve your data** using encryption and passkeys.")

# 💾 Store Data Page
elif choice == "Store Data":
    st.subheader("📂 Store New Data")
    data = st.text_area("Enter Text to Encrypt:")
    passkey = st.text_input("Set Your Passkey:", type="password")

    if st.button("Encrypt & Save"):
        if data and passkey:
            hashed = hash_passkey(passkey)
            encrypted = encrypt_data(data)
            stored_data[encrypted] = {"encrypted_text": encrypted, "passkey": hashed}
            save_data()  # Save to JSON
            st.success("✅ Data encrypted and saved successfully!")
            st.code(encrypted)
        else:
            st.error("⚠️ Both fields are required!")

# 🔓 Retrieve Data Page
elif choice == "Retrieve Data":
    st.subheader("🔍 Retrieve Your Data")
    encrypted_input = st.text_area("Paste Encrypted Data:")
    passkey = st.text_input("Enter Your Passkey:", type="password")

    if st.button("Decrypt"):
        if encrypted_input and passkey:
            result = decrypt_data(encrypted_input, passkey)
            if result:
                st.success("✅ Decrypted Data:")
                st.code(result)
            else:
                remaining = max(0, 3 - failed_attempts)
                st.error(f"❌ Incorrect passkey! Attempts left: {remaining}")
                if failed_attempts >= 3:
                    st.warning("🔒 Too many failed attempts! Please reauthorize.")
                    st.experimental_rerun()
        else:
            st.error("⚠️ Both fields are required!")

# 🔐 Login Page
elif choice == "Login":
    st.subheader("🔑 Reauthorization Required")
    login_pass = st.text_input("Enter Admin Password:", type="password")

    if st.button("Login"):
        if login_pass == "admin123":  # Simple admin password
            failed_attempts = 0
            st.success("✅ Reauthorized successfully! You can now try again.")
        else:
            st.error("❌ Incorrect password!")

import streamlit as st
import streamlit_authenticator as stauth
import datetime
import re
from deta import Deta

DETA_KEY = 'c0ydauhuktx_jNQcXQ4YC6nA8K5wG3xvQCMLkPNRdJKg'

deta = Deta(DETA_KEY)

db = deta.Base('StreamlitAuth')


def insert_user(email, username, password):

    date_joined = str(datetime.datetime.now())

    return db.put({'key': email, 'username': username, 'password': password, 'date_joined': date_joined})


def fetch_users():

    users = db.fetch()
    return users.items


def get_user_emails():

    users = db.fetch()
    emails = []
    for user in users.items:
        emails.append(user['key'])
    return emails


def get_usernames():

    users = db.fetch()
    usernames = []
    for user in users.items:
        usernames.append(user['key'])
    return usernames


def validate_email(email):

    pattern = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$" #tesQQ12@gmail.com

    if re.match(pattern, email):
        return True
    return False


def validate_username(username):

    pattern = "^[a-zA-Z0-9]*$"
    if re.match(pattern, username):
        return True
    return False

def sign_up():
    with st.form(key='signup', clear_on_submit=True):
        st.subheader(':green[Sign Up]')
        email = st.text_input(':blue[Email]', placeholder='Enter Your Email')
        username = st.text_input(':blue[Username]', placeholder='Enter Your Username')
        password1 = st.text_input(':blue[Password]', placeholder='Enter Your Password', type='password')
        password2 = st.text_input(':blue[Confirm Password]', placeholder='Confirm Your Password', type='password')

        if not email:
            st.warning('Email is required')
        elif not validate_email(email):
            st.warning('Invalid Email')
        elif email in get_user_emails():
            st.warning('Email Already exists!!')
        elif not username:
            st.warning('Username is required')
        elif not validate_username(username):
            st.warning('Invalid Username')
        elif username in get_usernames():
            st.warning('Username Already Exists')
        elif len(username) < 2:
            st.warning('Username Too short')
        elif len(password1) < 6:
            st.warning('Password is too Short')
        elif password1 != password2:
            st.warning('Passwords Do Not Match')
        else:
            # Add User to DB
            hashed_password = stauth.Hasher([password2]).generate()
            insert_user(email, username, hashed_password[0])
            st.success('Account created successfully!!')
            st.balloons()

        btn1, bt2, btn3, btn4, btn5 = st.columns(5)

        with btn3:
            st.form_submit_button('Sign Up')
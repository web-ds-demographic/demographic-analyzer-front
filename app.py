
import streamlit as st
import streamlit_authenticator as stauth
from dependancies import sign_up, fetch_users
import pandas as pd


st.set_page_config(page_title="DemografiX", page_icon=":bar_chart:", layout="wide")



try:
    users = fetch_users()
    emails = []
    usernames = []
    passwords = []

    for user in users:
        emails.append(user['key'])
        usernames.append(user['username'])
        passwords.append(user['password'])

    credentials = {'usernames': {}}
    for index in range(len(emails)):
        credentials['usernames'][usernames[index]] = {'name': emails[index], 'password': passwords[index]}

    Authenticator = stauth.Authenticate(credentials, cookie_name='Streamlit', key='abcdef', cookie_expiry_days=4)

    email, authentication_status, username = Authenticator.login(':green[Login]', 'main')

    info, info1 = st.columns(2)

    if not authentication_status:
        sign_up()

    if username:
        if username in usernames:
            if authentication_status:
                # let User see app
                st.sidebar.subheader(f'Welcome {username}')
                Authenticator.logout('Log Out', 'sidebar')

                st.subheader('This is the home page')
                st.markdown(
                    """
                    ---
                    Created by DemografiX team 
                    
                    """
                )


                data = pd.read_csv("data_rostat.csv", skiprows=2, encoding="cp1251")

                data.columns = ["Region", "Code", "2016", "2017", "2018", "2019", "2020", "2021", "2022"]

                columns_to_plot = ["2016", "2017", "2018", "2019", "2020", "2021", "2022"]

                st.title("Отображение данных из data_rostat.csv")

                st.dataframe(data)

                st.line_chart(data[columns_to_plot])


            elif not authentication_status:
                with info:
                    st.error('Incorrect Password or username')
            else:
                with info:
                    st.warning('Please feed in your credentials')
        else:
            with info:
                st.warning('Username does not exist, Please Sign up')


except:
    st.success('Refresh Page')



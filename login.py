import streamlit as st
import pandas as pd
import app
import SessionState


# Security
#passlib,hashlib,bcrypt,scrypt
import hashlib
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False
# DB Management
import sqlite3
conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username,password):
    c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
    conn.commit()

def login_user(username,password):
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
    data = c.fetchall()
    return data


def view_all_users():
    c.execute('SELECT * FROM userstable')
    data = c.fetchall()
    return data



def main():
    """Simple Login App"""

    st.title("Welcome to Twitter Analyzer Web Application")

    menu = ["Home","Login","SignUp"]
    choice = st.sidebar.selectbox("Menu",menu)

    if choice == "Home":
        st.subheader("Home")

    elif choice == "Login":
        with st.form(key='form1'):
            username = st.sidebar.text_input("User Name")
            password = st.sidebar.text_input("Password",type='password')
        if st.sidebar.checkbox("Login"):
            # if password == '12345':
            create_usertable()
            hashed_pswd = make_hashes(password)

            result = login_user(username,check_hashes(password,hashed_pswd))
            if result:
                st.success("Logged In as {}".format(username))
                if st.sidebar.checkbox("Logout"):
                    st.write("Logged out,login back to proceed")
                activities=["Tweet Analyzer","Generate Twitter Data","Watch trending"]
                choice = st.selectbox("Select Your Activity",activities)
                app.app(choice)




            else:
                st.warning("Incorrect Username/Password")





    elif choice == "SignUp":
        st.subheader("Create New Account")
        with st.form(key='form2'):
            new_user = st.text_input("Username")
            new_password = st.text_input("Password",type='password')
            submit_button=st.form_submit_button(label='Sign Up')

        if submit_button:
            create_usertable()
            add_userdata(new_user,make_hashes(new_password))
            st.success("You have successfully created a valid Account")
            st.info("Go to Login Menu to login")




if __name__ == '__main__':
    main()

import streamlit as st
import base64
from datetime import datetime, timedelta

# Set the title of the app
st.title("LinkUp")

# Sidebar menu options
menu = st.sidebar.radio("LinkMenu", ["Register", "Login", "Create", "View", "Connect", "Logout"])

# Initialize session state variables for tracking login status
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None

# Register screen where new users can create an account
if menu == "Register":
    st.write("Register for a new account")
    # Collecting user input for registration
    username = st.text_input("Username:")
    password = st.text_input("Password:", type='password')
    birth_date = st.date_input("Enter birthdate:")
    profile_pic = st.file_uploader("Upload profile picture", type=["png", "jpg", "jpeg"])
    occupation = st.text_input("Enter occupation:")
    email_add = st.text_input("Enter email address:")
    phone = st.text_input("Enter phone number:")

    if st.button("Register"):
        try:
            # If user uploads a profile picture, encode it as base64
            if profile_pic is not None:
                image_bytes = profile_pic.read()
                encoded_image = base64.b64encode(image_bytes).decode("utf-8")
            else:
                encoded_image = ""

            # Check if users.txt file exists and read the existing users
            with open("users.txt", "r") as file:
                users = file.readlines()
            # Check if username already exists
            if any(f"Username: {username}" in line for line in users):
                st.error("Username already exists")
            else:
                # Add new user data to users.txt file
                with open("users.txt", "a") as file:
                    file.write(
                        f"Username: {username} Password: {password} "
                        f"Birthdate: {birth_date} Profile Picture: {encoded_image} "
                        f"Occupation: {occupation} Email Address: {email_add} Phone: {phone}\n"
                    )
                st.success("Registration successful!")
        except FileNotFoundError:
            # If users.txt doesn't exist, create it and save the new user data
            with open("users.txt", "w") as file:
                file.write(
                    f"Username: {username} Password: {password} "
                    f"Birthdate: {birth_date} Profile Picture: {encoded_image} "
                    f"Occupation: {occupation} Email Address: {email_add} Phone: {phone}\n"
                )
            st.success("Registration successful!")

# Login screen where users can log into their account
elif menu == "Login":
    st.write("Login to your account")
    username = st.text_input("Username:")
    password = st.text_input("Password:", type='password')
    if st.button("Login"):
        try:
            # Read the user data from the file
            with open("users.txt", "r") as file:
                users = file.readlines()
            # Check if the username and password match any record
            if any(f"Username: {username} Password: {password}" in line for line in users):
                st.success("Login successful!")
                st.session_state.logged_in = True  # Set logged_in to True
                st.session_state.logged_in_user = username  # Store logged-in user
            else:
                st.error("Invalid username or password")
        except FileNotFoundError:
            st.error("No users registered yet. Please register first!")

# Logout screen where users can log out from their account
elif menu == "Logout":
    if not st.session_state.logged_in:
        st.error("You are not logged in")  # Display error if user is not logged in
    else:
        st.session_state.logged_in = False  # Set logged_in to False
        st.session_state.logged_in_user = None  # Clear the logged-in user data
        st.success("Successfully logged out")

# Create a post screen where logged-in users can create posts
elif menu == "Create":
    if not st.session_state.logged_in:
        st.error("You must be logged in to post.")  # User needs to be logged in to post
    else:
        st.write("Create a Post")
        post = st.text_area("Enter your post:")  # Input text for the post
        uploaded_files = st.file_uploader("Upload images (optional):", accept_multiple_files=True, type=["png", "jpg", "jpeg"])

        if st.button("Post"):
            try:
                # Prepare post data
                post_data = f"Username: {st.session_state.logged_in_user}\nPost: {post}\n"
                images_data = ""

                # If any images are uploaded, encode them as base64
                if uploaded_files:
                    for uploaded_file in uploaded_files:
                        image_bytes = uploaded_file.read()
                        encoded_image = base64.b64encode(image_bytes).decode("utf-8")
                        images_data += f"Image: {encoded_image}\n"

                # Append post data to the messages file
                with open("messages.txt", "a") as file:
                    file.write(post_data + images_data + "\n---\n")

                st.success("Post successfully submitted!")
            except Exception as e:
                st.error(f"An error occurred: {e}")

# View posts screen to display all posts
elif menu == "View":
    st.write("View Posts")
    try:
        # Read the existing posts from the messages file
        with open("messages.txt", "r") as file:
            posts = file.read().split("\n---\n")  # Split posts by delimiter

        updated_posts = []  # To store updated posts
        moved_posts = []    # To move marked posts to the bottom

        # Iterate over the posts to display them
        for post in posts:
            if post.strip():  # Skip empty posts
                lines = post.split("\n")
                username = lines[0] if len(lines) > 0 else ""
                content = lines[1] if len(lines) > 1 else ""
                images = [line for line in lines[2:] if line.startswith("Image: ")]

                # Display the post content
                st.write(f"**{username}**")
                st.write(content)

                # Display associated images
                for image in images:
                    encoded_image = image.split("Image: ")[1]
                    decoded_image = base64.b64decode(encoded_image)
                    st.image(decoded_image, use_column_width=True)

                # Add a checkbox to mark the post as read
                if st.checkbox(f"Mark '{username}' post as read", key=post):
                    moved_posts.append(post)  # Move this post to the bottom
                else:
                    updated_posts.append(post)  # Keep this post in the current order

        # Append moved posts at the end of the updated posts
        updated_posts.extend(moved_posts)

        # Save the updated order of posts back to the file
        with open("messages.txt", "w") as file:
            file.write("\n---\n".join(updated_posts))

        st.success("Posts updated successfully!")

    except FileNotFoundError:
        st.error("No posts found. Create a post first!")

# Connect screen for users to search for others
elif menu == "Connect":
    st.write("Connect with other users")
    search = st.text_input("Who are you looking for:")
    if st.button("Search"):
        if not st.session_state.logged_in:
            st.error("You must be logged in to search for users.")  # User needs to be logged in to search
        else:
            # Search for users in the users.txt file
            with open("users.txt", "r") as file:
                users = file.readlines()
                found_users = [line for line in users if search.lower() in line.lower()]
                if found_users:
                    st.write("Found Users:")
                    for user in found_users:
                        user_data = user.split()
                        st.write(user_data[0])  # Display username
                        if "Profile Picture:" in user:
                            encoded_image = user.split("Profile Picture: ")[1].split()[0]
                            decoded_image = base64.b64decode(encoded_image)
                            st.image(decoded_image, width=100)
                else:
                    st.error("No matching users found!")

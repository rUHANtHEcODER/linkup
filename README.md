# LinkUp - Social Media Platform

**LinkUp** is a simple social media platform built with Streamlit. The app allows users to register, log in, create posts, view posts, connect with other users, and manage their personal profiles. It offers features such as profile picture uploads, text-based posts with image attachments, and a user search function. 

This platform is designed to demonstrate the basic functionalities of a social media application, focusing on user management, content creation, and social interaction.

## Features

### User Registration
- Users can create a new account by providing basic information such as:
  - Username
  - Password
  - Birthdate
  - Profile picture (optional)
  - Occupation
  - Email address
  - Phone number

### User Login
- Registered users can log in using their username and password. Upon successful login, the user can access all available features such as creating posts, viewing posts, and connecting with other users.

### Create Posts
- Logged-in users can create posts by writing text and optionally uploading images. These posts are then saved to the platform and displayed to other users.

### View Posts
- Users can view posts created by others. Each post includes:
  - Username of the poster
  - Content of the post
  - Any images uploaded with the post

### Connect with Other Users
- Users can search for other users by entering a search term (e.g., username or any part of their profile details).
- The app will display a list of users whose details match the search term.

### Logout
- Users can log out of the platform, which will reset their session and require them to log in again to access their account.

## Requirements

To run the app, you'll need to install Python and some libraries. Specifically:

- **Streamlit**: A library for building interactive web applications.
- **Base64**: For encoding and decoding images.
- **datetime**: For handling date-related tasks.
  
You can install the necessary dependencies using `pip`. The following command will install all the required libraries:

```bash
pip install streamlit

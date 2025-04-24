# SignUp Bot

## Overview
signUp_Bot is a Django-based automation tool designed to perform automated signups on a specific website. With some modifications, it can be adapted to work with other websites as well. The bot provides a simple UI where users can input the signup URL of the target website, a test username (e.g., test01@gmail.com), and specify the number of signups (limit) to perform.
Note: This bot is tailored for a specific website and serves as a proof-of-concept. It is not a fully generalized solution for all websites and is currently a work in progress.
Features

Automates signup on a target website using Selenium.
Simple UI to input:
Website signup URL.
Test username (e.g., test01@gmail.com).
Signup limit (number of accounts to create).

Can be modified to support other websites with adjustments to the form-filling logic.

## Usage

Open your browser and navigate to http://127.0.0.1:8000/ (or the port shown in the terminal).
Access the bot’s UI (e.g., at /bot/create/ if following your project structure).
Enter the following details:
Signup URL: The URL of the website’s signup page.
Test Username: A base username (e.g., test). The bot will append numbers (e.g., test01@gmail.com).
Limit: The number of signup attempts to perform.


Submit the form to start the signup process.
The bot will attempt to create accounts and redirect to a success page (/bot/success/) upon completion.

## Limitations

This bot is designed for a specific website and may not work out-of-the-box for others without modifying the form-filling logic (e.g., adjusting field selectors, dropdown values).
It’s a basic flow and not a production-ready solution for all websites.
Work in progress: Additional features, error handling, and generalization are still being developed.

Ensure these dependencies are installed (typically via requirements.txt).
Contributing
This project is a work in progress. Contributions, suggestions, and improvements are welcome! Feel free to open issues or submit pull requests.

## Project Setup
```bash
git clone https://github.com/mabdullah136/signUp_bot.git
python3 -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py runserver



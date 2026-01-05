# News-Scoops-App
A Python-based News Application built with Tkinter GUI and MySQL backend. Designed for users to get effective news feed and equip them with the latest news updates.
NEWS SCOOPS – NEWS APPLICATION

News Scoops is a desktop-based news application developed using Python, Tkinter, and SQLite.
The application provides real-time news updates from multiple categories along with live weather and time information. It is designed with a clean, user-friendly interface and includes features such as user authentication, article previews, and PDF generation of top headlines.

FEATURES

• User Authentication

Login and create account functionality

User details stored securely using SQLite database

• Live News Updates

Fetches real-time news using NewsAPI

Available categories:

Top Headlines

Business

Technology

Science

Sports

Health

Entertainment

• News Preview

View a detailed preview of news articles

Redirects to the original news source for full reading

• Weather and Time Panel

Displays current temperature, weather condition, humidity, and wind speed

Shows live date, day, and time

• PDF Generation

Generate and save a PDF containing the current top headlines

• Navigation Controls

Reload news content

Go back to previously viewed category

Slide-in menu navigation

TECHNOLOGIES USED

Programming Language
• Python 3.10

GUI Framework
• Tkinter
• TkinterWeb
• TkHTMLView

Database
• SQLite3

APIs
• NewsAPI – for live news updates
• OpenWeatherMap API – for weather data

Libraries and Modules
• requests
• PIL (Pillow)
• pandas
• fpdf
• textwrap
• itertools
• unicodedata
• datetime
• time

SYSTEM REQUIREMENTS

Software Requirements
• Windows 10 / 11
• Python 3.10 or higher
• VS Code (recommended)

Hardware Requirements
• Minimum 8 GB RAM
• Stable internet connection

PROJECT STRUCTURE

News-Scoops-App
│
├── main.py
├── news_scoops_user_accounts.db
├── news_scoops_news_gen.db
├── pics
│ ├── UI images and icons
├── README.md

HOW TO RUN THE PROJECT

Clone the repository

git clone https://github.com/simeon-suchir/News-Scoops-App.git

Navigate to the project folder

cd News-Scoops-App

Install the required libraries

pip install requests pillow pandas fpdf tkhtmlview tkinterweb

Run the application

python main.py

FUTURE ENHANCEMENTS

• Search feature for news articles
• Multi-country news support
• Password encryption for better security
• Notification system for breaking news
• Mobile version of the application
• Cloud database integration

PROJECT INFORMATION

Project Name : News Scoops – News Application
Developed By : Simeon Suchir S
Purpose : Academic and learning project
Domain : Python Desktop Application

LICENSE

This project is developed for educational purposes.
You are free to use, modify, and improve the project.

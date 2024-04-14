# TazaKhabre

---

Welcome to TazaKhabre, your one-stop destination for the latest news updates across India. Designed to keep you informed and engaged, TazaKhabre offers real-time news updates, providing users with the ability to search for news up to a month old using keywords. Stay informed with our daily newsletter featuring the top 10 news stories every morning.

## Features

---

- **Live News Updates**: Get real-time updates on the latest happenings in India.
- **Categorized News**: News articles are organized into categories, making it easy to find information on specific topics.
- **Search Functionality**: Search for news articles up to a month old using specific keywords.
- **Daily Newsletter Subscription**: Subscribe to receive a daily email every morning that includes the top 10 fresh news stories of the day.
- **User-Friendly Interface**: The project is designed with a clean and intuitive interface, ensuring a smooth user experience.

## Tech Stack

---

- **Backend**: Django, requests
- **Frontend**: Django template engine, HTML, Bootstrap, CSS
- **Task Scheduling**: Integrated Celery to schedule task for sending emails to a list of subscribers through Celery Beat
- **API**: News API for fetching news data (https://newsapi.org/)
- **Email Delivery**: Implemented multithreading by creating a thread pool to send the email to subscribers using individual worker thread

## API Integration

---

TazaKhabre relies on the [News API] to fetch real-time news data. To use this project, you'll need to obtain an API key from [News API] and replace the placeholder in the code with your actual API key.

## Note

---

This project is only made for learning purposes. And after 100 request the application will be throttled down. But you can enjoy the next day with a complete renewed quota.
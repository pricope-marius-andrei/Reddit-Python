"""
A Flask application for interacting with Reddit subreddits.

This application provides functionality to fetch and display information about subreddits,
including flair frequencies, posts from the last 24 hours, and other metadata.

Modules:
    - flask: For creating the web application.
    - render_template: To render HTML templates.
    - dotenv.load_dotenv: For loading environment variables from a .env file.
    - Reddit: Custom module for interacting with the Reddit API.
    - SubredditManager: Custom module for managing subreddit data.

Routes:
    - /: Displays a simple search instruction message.
    - /<path:subreddit>: Displays information about the specified subreddit.

Author: Pricope Marius-Andrei
"""

from dotenv import load_dotenv
from flask import Flask, render_template
from reddit import Reddit
from subreddit_manager import SubredditManager

# Initialize Flask application
app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Initialize Reddit and SubredditManager instances
reddit = Reddit()
subreddit_manager = SubredditManager(reddit)

@app.route('/')
def home():
    """Homepage route.

    Returns:
        str: A simple instruction message for using the application.
    """
    return "Search in the search bar a subreddit. Eg: /amd"

@app.route('/<path:subreddit>')
def info(subreddit):
    """Subreddit information route.

    Fetches and displays data about the specified subreddit, including:
        - Metadata (about data)
        - Flair frequencies
        - Posts from the last 24 hours
        - A list of posts

    Args:
        subreddit (str): The name of the subreddit to fetch information about.

    Returns:
        str or Response: Rendered HTML template or an error message if the subreddit is not found.
    """
    subreddit_name = subreddit
    threads_limit = 100

    # Fetch metadata about the subreddit
    about_data = subreddit_manager.about_subreddit(subreddit_name)
    if about_data is None:
        return "The subreddit is not found!"

    # Fetch flair frequency data
    flairs_freq = subreddit_manager.flairs_freq(subreddit_name, threads_limit)
    if flairs_freq is None:
        return "The subreddit is not found!"

    # Fetch posts from the last 24 hours
    last_24_hours_posts = subreddit_manager.last_24h_posts(subreddit_name)
    if last_24_hours_posts is None:
        return "The subreddit is not found!"

    # Fetch a list of some posts from the subreddit
    posts = subreddit_manager.get_some_posts(subreddit_name)
    if posts is None:
        return "The subreddit is not found!"

    # Render the index.html template with the fetched data
    return render_template(
        'index.html',
        about_data=about_data,
        threads_limit=threads_limit,
        flair_freq_list=flairs_freq.items(),
        last_24_hours_posts=last_24_hours_posts,
        threads_list=posts
    )

if __name__ == '__main__':
    # Run the Flask application in debug mode
    app.run(debug=True)

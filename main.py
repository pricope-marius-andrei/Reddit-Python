from dotenv import load_dotenv
from flask import Flask, render_template
from reddit import Reddit
from subreddit_manager import SubredditManager

app = Flask(__name__)

load_dotenv()

reddit = Reddit()
subreddit_manager = SubredditManager(reddit)

@app.route('/')
def home():
    return "Search in the search bar a subreddit. Eg: /amd"

@app.route('/<path:subreddit>')
def info(subreddit):
    subreddit_name = subreddit
    threads_limit = 100

    about_data = subreddit_manager.about_subreddit(subreddit_name)

    if about_data is None:
        return "The subreddit is not found!"

    flairs_freq = subreddit_manager.flairs_freq(subreddit_name, threads_limit)

    if flairs_freq is None:
        return "The subreddit is not found!"

    last_24_hours_posts = subreddit_manager.last_24h_posts(subreddit_name)

    if last_24_hours_posts is None:
        return "The subreddit is not found!"

    posts = subreddit_manager.get_some_posts(subreddit_name)

    if posts is None:
        return "The subreddit is not found!"

    return render_template('index.html',
                           about_data=about_data,
                           threads_limit=threads_limit,
                           flair_freq_list=flairs_freq.items(),
                           last_24_hours_posts=last_24_hours_posts,
                           threads_list=posts)


if __name__ == '__main__':
    app.run(debug=True)
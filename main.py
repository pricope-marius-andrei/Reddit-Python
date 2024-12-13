from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

from flask import Flask, render_template

from reddit import Reddit

app = Flask(__name__)


load_dotenv()

subreddit_name = "Amd"
threads_limit = 100

reddit = Reddit()

reddit.generate_token()


about = reddit.get_call(f"/r/{subreddit_name}/about", "")

about_data = about["data"]

data = reddit.get_call(f"/r/{subreddit_name}/hot", f"?g=GLOBAL&count=0&limit={threads_limit}")["data"]["children"]

flairs_freq = {}

for subreddit in data:
    flair = subreddit["data"]["author_flair_text"]
    if flair is not None:
        if flair in flairs_freq:
            flairs_freq[flair] += 1
        else:
            flairs_freq[flair] = 1

flairs_freq = dict(sorted(flairs_freq.items(), key=lambda x: x[1], reverse=True))

new_posts = reddit.get_call(f"/r/{subreddit_name}/new", "?count=0&limit=100")["data"]["children"]

last_24_hours_posts = 0
for new_post in new_posts:
    created_time = new_post["data"]["created_utc"]
    if created_time > (datetime.now(timezone.utc) - timedelta(days=1)).timestamp():
        last_24_hours_posts += 1

print(last_24_hours_posts)


posts = reddit.get_call(f"/r/{subreddit_name}/hot", "?count=0&limit=10")["data"]["children"]

print(posts)

for post in posts:
    print(post["data"]["title"])
@app.route('/')
def home():
    return render_template('index.html',
                           display_name=about_data["display_name"],
                           accounts_active=about_data["accounts_active"],
                           subscribers=about_data["subscribers"],
                           description=about_data["public_description"],
                           threads_limit=threads_limit,
                           flair_freq_list=flairs_freq.items(),
                           last_24_hours_posts=last_24_hours_posts,
                           threads_list=posts)


if __name__ == '__main__':
    app.run(debug=True)
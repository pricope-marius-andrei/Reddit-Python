from datetime import datetime, timedelta, timezone

from requests import HTTPError


class SubredditManager:
    def __init__(self, reddit):
        self.data = []
        self.reddit = reddit

    def set_data(self, data):
        self.data = data

    def about_subreddit(self, subreddit_name):
        try:
            about = self.reddit.get_call(f"/r/{subreddit_name}/about", "")
            about_data = about["data"]
            return about_data
        except Exception as e:
            print(f"Error: {e}")
            return None




    def flairs_freq(self, subreddit_name, threads_limit):
        try:
            self.data = self.reddit.get_call(f"/r/{subreddit_name}/hot", f"?g=GLOBAL&count=0&limit={threads_limit}")["data"][
                "children"]

            flairs_freq = {}

            for subreddit in self.data:
                flair = subreddit["data"]["author_flair_text"]
                if flair is not None:
                    if flair in flairs_freq:
                        flairs_freq[flair] += 1
                    else:
                        flairs_freq[flair] = 1

            flairs_freq = dict(sorted(flairs_freq.items(), key=lambda x: x[1], reverse=True))

            return flairs_freq
        except Exception as e:
            print(f"Error: {e}")
            return None

    def last_24h_posts(self, subreddit_name):
        try:
            self.data = self.reddit.get_call(f"/r/{subreddit_name}/new", "?count=0&limit=100")["data"]["children"]

            last_24_hours_posts = 0
            for new_post in self.data:
                created_time = new_post["data"]["created_utc"]
                if created_time > (datetime.now(timezone.utc) - timedelta(days=1)).timestamp():
                    last_24_hours_posts += 1

            return last_24_hours_posts
        except Exception as e:
            print(f"Error: {e}")
            return None

    def get_some_posts(self, subreddit_name):
        try:
            return self.reddit.get_call(f"/r/{subreddit_name}/hot", "?count=0&limit=10")["data"]["children"]
        except Exception as e:
            print(f"Error: {e}")
            return None
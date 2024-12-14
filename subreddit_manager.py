from datetime import datetime, timedelta, timezone

class SubredditManager:
    """
    A class to manage subreddit-related actions, such as fetching subreddit information,
    calculating flair frequencies, and counting posts in the last 24 hours.

    Attributes:
        reddit (Reddit): An instance of the Reddit class used for making API calls.

    Methods:
        about_subreddit(subreddit_name):
            Retrieves information about a subreddit.
        flairs_freq(subreddit_name, threads_limit):
            Calculates the frequency of author flairs in a subreddit.
        last_24h_posts(subreddit_name):
            Counts the number of posts made in the last 24 hours in a subreddit.
        get_some_posts(subreddit_name):
            Retrieves a list of hot posts from a subreddit.
    """

    def __init__(self, reddit):
        """
        Initializes the SubredditManager instance.

        Args:
            reddit (Reddit): An instance of the Reddit class to interact with Reddit's API.

        Sets:
            self.data: An empty list to store subreddit data.
            self.reddit: The provided Reddit instance to interact with the Reddit API.
        """
        self.reddit = reddit

    def about_subreddit(self, subreddit_name):
        """
        Retrieves information about a subreddit.

        Args:
            subreddit_name (str): The name of the subreddit to retrieve information about.

        Returns:
            dict: A dictionary containing subreddit information if successful.
            None: If an error occurs during the API call.

        Raises:
            Exception: If the API request fails.
        """
        try:
            about = self.reddit.get_call(f"/r/{subreddit_name}/about", "")
            about_data = about["data"]
            return about_data
        except Exception as e:
            print(f"Error: {e}")
            return None

    def flairs_freq(self, subreddit_name, threads_limit):
        """
        Calculates the frequency of author flairs in the hot posts of a subreddit.

        Args:
            subreddit_name (str): The name of the subreddit to analyze.
            threads_limit (int): The maximum number of threads to analyze.

        Returns:
            dict: A dictionary where keys are flairs and values are the frequency of each flair.
            None: If an error occurs during the API call or no data is available.

        Raises:
            Exception: If the API request fails.
        """
        try:
            data = self.reddit.get_call(f"/r/{subreddit_name}/hot", f"?g=GLOBAL&count=0&limit={threads_limit}")["data"]["children"]

            flairs_freq = {}

            for subreddit in data:
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
        """
        Counts the number of posts made in the last 24 hours in a subreddit.

        Args:
            subreddit_name (str): The name of the subreddit to analyze.

        Returns:
            int: The number of posts made in the last 24 hours.
            None: If an error occurs during the API call.

        Raises:
            Exception: If the API request fails.
        """
        try:
            data = self.reddit.get_call(f"/r/{subreddit_name}/new", "?count=0&limit=100")["data"]["children"]

            last_24_hours_posts = 0
            for new_post in data:
                created_time = new_post["data"]["created_utc"]
                if created_time > (datetime.now(timezone.utc) - timedelta(days=1)).timestamp():
                    last_24_hours_posts += 1

            return last_24_hours_posts
        except Exception as e:
            print(f"Error: {e}")
            return None

    def get_some_posts(self, subreddit_name):
        """
        Retrieves a list of hot posts from a subreddit.

        Args:
            subreddit_name (str): The name of the subreddit to retrieve hot posts from.

        Returns:
            list: A list of hot posts from the subreddit.
            None: If an error occurs during the API call.

        Raises:
            Exception: If the API request fails.
        """
        try:
            return self.reddit.get_call(f"/r/{subreddit_name}/hot", "?count=0&limit=10")["data"]["children"]
        except Exception as e:
            print(f"Error: {e}")
            return None

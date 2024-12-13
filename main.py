from dotenv import load_dotenv

from flask import Flask, render_template

from reddit import Reddit

app = Flask(__name__)


load_dotenv()

reddit = Reddit()

reddit.generate_token()

about = reddit.get_call("/r/EASportsFC/about", "")

about_data = about["data"]


# data = reddit.get_call("/r/EASportsFC/top", "?g=GLOBAL&count=0&limit=25")["data"]

data = reddit.get_call("/r/EASportsFC/top", "?t=day&count=0&limit=26")

print(data)

# for post in data["children"]:
#     print(post["data"]["url"])

@app.route('/')
def home():
    return render_template('index.html',
                           display_name=about_data["display_name"],
                           accounts_active=about_data["accounts_active"],
                           subscribers=about_data["subscribers"],
                           description=about_data["public_description"])


if __name__ == '__main__':
    app.run(debug=True)
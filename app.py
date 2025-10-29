from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
from flask_cors import CORS
import requests
app = Flask(__name__)
CORS(app)



def fetch_news(keyword):
    """Fetch news from Google RSS by keyword."""
    url = f"https://news.google.com/rss/search?q={keyword}"
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
    except Exception as e:
        return {"error": str(e)}

    soup = BeautifulSoup(res.text, "xml")
    articles = []

    for item in soup.find_all("item")[:10]:  # limit to top 10
        articles.append({
            "title": item.title.text,
            "link": item.link.text,
            "published": item.pubDate.text
        })

    return {"keyword": keyword, "count": len(articles), "articles": articles}

@app.route("/api/news", methods=["GET"])
def get_news():
    """API endpoint: /api/news?keyword=sui"""
    keyword = request.args.get("keyword")
    if not keyword:
        return jsonify({"error": "Missing 'keyword' parameter"}), 400

    data = fetch_news(keyword)
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True, port=8000)

import requests
import datetime

def get_cybersecurity_news():
    """Fetch latest cybersecurity and vulnerability news from NewsAPI"""
    api_key = "52e31aac2a7240cf8dd4ce64e48cc86d"  # Free tier NewsAPI key
    url = "https://newsapi.org/v2/everything"
    
    params = {
        "q": "cybersecurity OR cyber security OR data breach OR malware OR ransomware OR vulnerability OR CVE OR exploit OR security patch OR zero-day",
        "sortBy": "publishedAt",
        "language": "en",
        "apiKey": api_key,
        "pageSize": 10
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            articles = data.get("articles", [])
            if articles:
                return articles
        return []
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []

def get_tldr_summary(text):
    """Create a TLDR from article description"""
    if not text:
        return "N/A"
    # Truncate to first 150 chars if too long
    if len(text) > 150:
        return text[:150] + "..."
    return text

def update_readme(articles):
    # Get current date and time
    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M:%S")
    
    # Build news section
    news_section = ""
    if articles:
        news_section = "## 🛡️ Latest Cybersecurity News\n\n"
        for i, article in enumerate(articles[:5], 1):
            title = article.get("title", "Untitled")
            description = article.get("description", "")
            url = article.get("url", "#")
            source = article.get("source", {}).get("name", "Unknown")
            pub_date = article.get("publishedAt", "")[:10]
            
            tldr = get_tldr_summary(description)
            
            news_section += f"{i}. **[{title}]({url})**\n"
            news_section += f"   - **TLDR:** {tldr}\n"
            news_section += f"   - Source: {source} | {pub_date}\n\n"
    else:
        news_section = "## 🛡️ Latest Cybersecurity News\n\nNo news available at the moment.\n\n"
    
    # Define the content of the README
    readme_content = f"""# 🚀 Daily Streak Keeper

This repository automatically updates itself to keep my GitHub contribution streak alive while sharing cybersecurity insights.

## 📅 Updated: {date_str} {current_time}

{news_section}

---
*Last updated automatically by GitHub Actions.*
"""
    
    with open("README.md", "w", encoding="utf-8") as file:
        file.write(readme_content)

if __name__ == "__main__":
    articles = get_cybersecurity_news()
    update_readme(articles)
    print("README updated with latest cybersecurity news.")

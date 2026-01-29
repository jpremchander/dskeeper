import requests
import datetime

def get_quote():
    # Using dummyjson for stability (quotable.io can be flaky)
    url = "https://dummyjson.com/quotes/random"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return f"\"{data['quote']}\" — **{data['author']}**"
        else:
            return "Could not fetch a quote today. Keep coding!"
    except Exception as e:
        return f"Error fetching quote: {e}"

def update_readme(quote):
    # Get current date
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # Define the content of the README
    readme_content = f"""
# 🚀 Daily Streak Keeper

This repository automatically updates itself to keep my GitHub contribution streak alive.

## 📅 Quote for {date_str}

> {quote}

---
*Last updated automatically by GitHub Actions.*
"""
    
    with open("README.md", "w", encoding="utf-8") as file:
        file.write(readme_content)

if __name__ == "__main__":
    quote = get_quote()
    update_readme(quote)
    print("README updated successfully.")

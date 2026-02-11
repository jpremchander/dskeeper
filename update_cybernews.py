import feedparser
import datetime
import os
import re
import requests
import json

FEED_URLS = [
    "https://thehackernews.com/feeds/posts/default",
    "https://feeds2.feedburner.com/TheHackersNews"
]
README_FILE = "README.md"
ARCHIVE_DIR = "archive"

CVE_REGEX = r"(CVE-\d{4}-\d{4,7})"
CISA_KEV_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"

def get_cisa_kev():
    try:
        resp = requests.get(CISA_KEV_URL, timeout=10)
        data = resp.json()
        return {v["cveID"] for v in data["vulnerabilities"]}
    except Exception:
        return set()

def get_cvss(cve_id):
    try:
        url = f"https://services.nvd.nist.gov/rest/json/cve/2.0?cveId={cve_id}"
        resp = requests.get(url, timeout=10).json()
        metrics = resp["vulnerabilities"][0]["cve"]["metrics"]
        cvss = metrics.get("cvssMetricV31") or metrics.get("cvssMetricV30")
        if cvss:
            score = cvss[0]["cvssData"]["baseScore"]
            return score
    except Exception:
        pass
    return None

def cvss_severity(score):
    if score is None:
        return "Unknown"
    if score >= 9.0:
        return "Critical"
    if score >= 7.0:
        return "High"
    if score >= 4.0:
        return "Medium"
    return "Low"

def get_entry_image(entry):
    """Extract image URL from feed entry"""
    # Try media:content first
    if hasattr(entry, 'media_content') and entry.media_content:
        for media in entry.media_content:
            if 'url' in media:
                return media['url']
    
    # Try media:thumbnail
    if hasattr(entry, 'media_thumbnail') and entry.media_thumbnail:
        for thumbnail in entry.media_thumbnail:
            if 'url' in thumbnail:
                return thumbnail['url']
    
    # Try to extract from summary HTML
    if hasattr(entry, 'summary') and entry.summary:
        img_match = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', entry.summary)
        if img_match:
            return img_match.group(1)
    
    # Try image field
    if hasattr(entry, 'image') and entry.image:
        return entry.image.get('href') or entry.image
    
    return None

def fetch_news():
    # Try each feed URL in order until one works
    feed = None
    for url in FEED_URLS:
        print(f"Trying feed URL: {url}")
        feed = feedparser.parse(url)
        if feed.entries:
            print(f"Successfully fetched feed from {url}")
            break
    
    if not feed or not feed.entries:
        print("No entries found from any feed source")
        return []

    news_items = []
    today = datetime.datetime.utcnow().date()
    
    for entry in feed.entries[:10]:  # Get up to 10 latest entries
        # Parse entry date
        entry_date = None
        if hasattr(entry, 'published_parsed') and entry.published_parsed:
            entry_date = datetime.datetime(*entry.published_parsed[:6]).date()
        
        # Only include today's news or if date parsing failed (include recent items)
        if entry_date is None or entry_date == today:
            text = entry.title + " " + entry.summary
            cve_matches = re.findall(CVE_REGEX, text)
            
            # Categorize based on keywords
            categories = []
            text_lower = text.lower()
            if any(word in text_lower for word in ["vulnerability", "exploit", "cve", "zero-day", "patch"]):
                categories.append("🔴 Vulnerability")
            if any(word in text_lower for word in ["webinar", "conference", "summit", "event"]):
                categories.append("📅 Webinar/Event")
            if any(word in text_lower for word in ["analysis", "insight", "expert", "opinion", "guide"]):
                categories.append("💡 Expert Insight")
            if not categories:
                categories.append("📰 News")
            
            image_url = get_entry_image(entry)
            
            news_items.append({
                "title": entry.title.strip(),
                "summary": entry.summary.replace("\n", " ").strip(),
                "link": entry.link,
                "cves": cve_matches if cve_matches else [],
                "categories": categories,
                "published": entry_date,
                "image": image_url
            })
    
    return news_items

def read_readme():
    if not os.path.exists(README_FILE):
        return ""
    return open(README_FILE, "r", encoding="utf-8").read()

def write_readme(content):
    open(README_FILE, "w", encoding="utf-8").write(content)

def archive_previous_day():
    """Archive previous day's content at midnight and start fresh"""
    existing = read_readme()
    if not existing.strip() or "# 🛡️" not in existing:
        return
    
    # Create archive directory if it doesn't exist
    if not os.path.exists(ARCHIVE_DIR):
        os.makedirs(ARCHIVE_DIR)
    
    # Get yesterday's date
    yesterday = (datetime.datetime.utcnow() - datetime.timedelta(days=1)).date()
    yesterday_str = yesterday.strftime("%Y-%m-%d")
    
    # Check if there's content from yesterday to archive
    if f"## 📅 {yesterday_str}" in existing:
        # Extract yesterday's section
        parts = existing.split(f"## 📅 {yesterday_str}")
        if len(parts) > 1:
            # Find where yesterday's section ends (next date or end of file)
            yesterday_content = parts[1]
            next_date_pos = yesterday_content.find("## 📅")
            if next_date_pos > 0:
                yesterday_content = yesterday_content[:next_date_pos]
            
            # Save to archive
            archive_file = os.path.join(ARCHIVE_DIR, f"{yesterday_str}.md")
            with open(archive_file, "w", encoding="utf-8") as f:
                f.write(f"# 🛡️ Cybersecurity Threat Intelligence - {yesterday_str}\n\n")
                f.write(yesterday_content)
            
            print(f"Archived {yesterday_str} to {archive_file}")
            
            # Remove yesterday's section from main README
            remaining = parts[0]
            if next_date_pos > 0:
                remaining += yesterday_content[next_date_pos:]
            write_readme(remaining)

def update_readme(news_items, kev_set):
    now = datetime.datetime.utcnow()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M UTC")

    # Filter out news items already in README
    existing = read_readme()
    new_items = [item for item in news_items if item["link"] not in existing]
    if not new_items:
        print("No new items to add.")
        return

    header = """# 🛡️ Cybersecurity Threat Intelligence Log

This repository tracks real-world cybersecurity threats,
vulnerabilities, and exploitation activity for continuous learning.

---
"""

    daily_section = f"## 📅 {date_str}\n\n"
    
    entries = ""
    for news in new_items:
        time_str = now.strftime("%H:%M UTC")
        
        # Process all CVEs
        cve_info = []
        for cve in news["cves"]:
            cvss_score = get_cvss(cve)
            severity = cvss_severity(cvss_score)
            kev_status = "⚠️ YES" if cve in kev_set else "No"
            cve_info.append({
                "id": cve,
                "cvss": cvss_score,
                "severity": severity,
                "kev": kev_status
            })
        
        # Build content
        content = f"""### 📰 {news['title']}
**Category:** {', '.join(news['categories'])}
**Time:** {time_str}

**Summary:**  
{news['summary']}

🔗 [Read Full Article]({news['link']})
"""
        
        # Create table entry with image on left (250px medium size)
        if news["image"]:
            entry = f"""<table><tr><td width="250"><img src="{news['image']}" width="250" alt="Article"></td><td>{content}

---</td></tr></table>

"""
        else:
            entry = f"""{content}

---

"""
        entries += entry

    # Always keep only today's data - start fresh with today's section
    content = header + daily_section + entries
    write_readme(content)
    
    print(f"Added {len(new_items)} new items to README.")

if __name__ == "__main__":
    print("Fetching CISA Known Exploited Vulnerabilities...")
    kev = get_cisa_kev()
    print(f"Found {len(kev)} KEV entries.")
    
    print("Archiving previous day's data...")
    archive_previous_day()
    
    print("Fetching latest cybersecurity news...")
    news_items = fetch_news()
    print(f"Found {len(news_items)} news items.")
    
    if news_items:
        update_readme(news_items, kev)
        print("README updated successfully!")
    else:
        print("No news items found.")

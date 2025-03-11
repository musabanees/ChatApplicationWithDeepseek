import requests
from bs4 import BeautifulSoup
import os

# Replace with your 5-6 web sources
WEB_SOURCES = [
    "https://maternityaction.org.uk/advice/maternity-pay-questions/#Where_to_go_for_more_help",
    "https://www.gov.uk/employee-rights-when-on-leave",
    "https://sybhealthiertogether.nhs.uk/pregnant-women/maternal-mental-health/worried-about-giving-birth",
    "https://sybhealthiertogether.nhs.uk/pregnant-women/maternal-mental-health/i-cant-stop-thinking-about-my-birth-experience",
    "https://sybhealthiertogether.nhs.uk/pregnant-women/maternal-mental-health/my-relationship",
    "https://sybhealthiertogether.nhs.uk/pregnant-women/maternal-mental-health/i-dont-feel-way-i-thought-i-would-about-my-baby",
    "https://sybhealthiertogether.nhs.uk/pregnant-women/perinatal-mental-health/sheffield",
    "https://sybhealthiertogether.nhs.uk/pregnant-women/perinatal-mental-health/barnsley-south-west-yorkshire-partnership"

]

def scrape_website(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"} 
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extract main content (adjust based on site structure)
        paragraphs = soup.find_all('p')
        text = ' '.join([p.get_text() for p in paragraphs])
        return text.strip()
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return ""

def save_content():
    if not os.path.exists("data"):
        os.makedirs("data")
    
    for i, url in enumerate(WEB_SOURCES):
        content = scrape_website(url)
        print(content)
        if content:
            with open(f"data/source_{i}.txt", "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Saved content from {url}")

if __name__ == "__main__":
    save_content()
# Facebook Profile Scraper

A Python-based web scraper that extracts posts from Facebook profiles using Selenium and BeautifulSoup. The scraper mimics human behavior to avoid detection and exports data to CSV format.

## ⚠️ Disclaimer

This tool is for educational purposes only. Web scraping may violate Facebook's Terms of Service. Use at your own risk and ensure you have proper authorization before scraping any content. The author is not responsible for any misuse of this tool.

## ✨ Features

- **Human-like behavior simulation**: Random typing speeds and mouse movements
- **Stealth mode**: Bypasses basic bot detection mechanisms
- **Intelligent content detection**: Automatically identifies text, image, and video posts
- **Duplicate removal**: Ensures unique posts in the final dataset
- **CSV export**: Saves scraped data in a structured format
- **Robust data extraction**: Captures post text, likes, comments, shares, timestamps, and links

## 📊 Data Collected

For each post, the scraper extracts:
- Post text content
- Number of likes
- Number of comments
- Number of shares
- Time posted
- Content type (text/image/video)
- Direct link to the post

## 🛠️ Requirements

```bash
Python 3.7+
selenium
beautifulsoup4
pandas
msedge-selenium-tools (or appropriate webdriver)
```

## 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/facebook-scraper.git
cd facebook-scraper
```

2. Install required packages:
```bash
pip install selenium beautifulsoup4 pandas
```

3. Download Microsoft Edge WebDriver:
   - Visit [Microsoft Edge WebDriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)
   - Download the version matching your Edge browser
   - Add it to your system PATH

## 🚀 Usage

### Basic Usage

```python
from facebook_scraper import FacebookScraper

# Initialize scraper with credentials
scraper = FacebookScraper("your_email@example.com", "your_password")

try:
    # Setup and login
    scraper.initialize_driver()
    scraper.login()
    
    # Navigate to target profile
    scraper.navigate_to_profile("https://www.facebook.com/profile_username")
    
    # Scrape posts
    posts_data = scraper.scrape_posts(max_posts=600)
    
    # Save to CSV
    df = scraper.save_to_csv(posts_data, filename="output.csv")
    
finally:
    scraper.close()
```

### Configuration

Modify the main execution block in `facebook_scraper.py`:

```python
if __name__ == "__main__":
    scraper = FacebookScraper("your_email", "your_password")
    
    try:
        scraper.initialize_driver()
        scraper.login()
        scraper.navigate_to_profile("https://www.facebook.com/target_profile")
        
        posts_data = scraper.scrape_posts(max_posts=600)
        df = scraper.save_to_csv(posts_data, filename="custom_name.csv") 
        
    finally:
        scraper.close()
```

## 🔧 Key Functions

### `initialize_driver()`
Sets up the Edge WebDriver with anti-detection configurations.

### `login()`
Authenticates with Facebook using provided credentials.

### `navigate_to_profile(profile_url)`
Navigates to the specified Facebook profile.

### `scrape_posts(max_posts)`
Scrapes the specified number of posts from the profile.

### `save_to_csv(posts_data, filename)`
Exports scraped data to a CSV file.

### `detect_content_type(post)`
Intelligently determines if a post contains text, images, or videos.

## 📝 Output Format

The CSV file includes the following columns:

| Column | Description |
|--------|-------------|
| post_text | The text content of the post |
| likes | Number of likes (or reaction count) |
| comments | Number of comments |
| shares | Number of shares |
| post_time | When the post was published |
| content_type | Type of content (text/image/video) |
| post_link | Direct URL to the post |

## ⚙️ Customization

### Adjust Scroll Speed
Modify the `step` parameter in `slow_scroll()`:
```python
scraper.slow_scroll(step=300)  # Slower scrolling
```

### Change Typing Speed
Edit the timing in `simulate_human_typing()`:
```python
time.sleep(random.uniform(0.05, 0.15))  # Faster typing
```

## 🐛 Troubleshooting

**Login fails:**
- Verify your credentials are correct
- Check if Facebook requires additional verification
- Increase wait time after login

**No posts extracted:**
- Ensure the profile is public or accessible
- Check CSS selectors (Facebook frequently updates their HTML structure)
- Increase scroll wait times

**WebDriver errors:**
- Ensure Edge WebDriver version matches your browser version
- Check if WebDriver is in system PATH

## 📄 License

MIT License - see LICENSE file for details

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## ⚖️ Legal Notice

This tool should only be used for:
- Personal data backup
- Research with proper authorization
- Educational purposes

**Do not use this tool to:**
- Violate Facebook's Terms of Service
- Scrape private or protected content without permission
- Collect personal data without consent
- Engage in any illegal activities

## 📧 Contact
adediran.yemite@yahoo.com

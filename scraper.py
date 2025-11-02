from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import random
import pandas as pd  # ✅ Added for DataFrame and CSV handling


class FacebookScraper:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.driver = None
        
    def initialize_driver(self):
        """Initialize the Edge webdriver with custom options"""
        options = webdriver.EdgeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        
        self.driver = webdriver.Edge(options=options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
    def simulate_human_typing(self, element, text):
        """Simulate human-like typing patterns"""
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.1, 0.3))
            if random.random() < 0.1:
                time.sleep(random.uniform(0.3, 0.7))
                
    def login(self):
        """Login to Facebook"""
        self.driver.get("https://www.facebook.com/login")
        
        # Enter email
        email_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "email"))
        )
        self.simulate_human_typing(email_input, self.email)
        
        # Enter password
        password_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "pass"))
        )
        self.simulate_human_typing(password_input, self.password)
        
        # Click login button
        login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
        ActionChains(self.driver)\
            .move_to_element(login_button)\
            .pause(random.uniform(0.2, 0.4))\
            .click()\
            .perform()
            
        time.sleep(15)
        
    def navigate_to_profile(self, profile_url):
        """Navigate to a specific Facebook profile"""
        self.driver.get(profile_url)
        time.sleep(4)
        
    def slow_scroll(self, step=500):
        """Scroll the page slowly"""
        self.driver.execute_script(f"window.scrollBy(0, {step});")
        time.sleep(2)

    def _element_has_play_text(self, tag):
        """Helper: check if a tag's textual attributes indicate a play button/overlay"""
        for attr_name in ('aria-label', 'title', 'alt', 'data-testid', 'role'):
            val = tag.get(attr_name)
            if isinstance(val, str) and 'play' in val.lower():
                return True
        classes = tag.get("class", [])
        if isinstance(classes, (list, tuple)):
            for c in classes:
                if 'play' in c.lower():
                    return True
        return False

    def detect_content_type(self, post):
        """
        Robust content detector:
        - First check direct <video> tags
        - Then look for play overlays / data-testid indicators
        - Then fallback to <img>
        - Else text
        """
        if post.find("video"):
            return "video"
        
        for tag in post.find_all(attrs=True):
            for attr_k, attr_v in tag.attrs.items():
                if isinstance(attr_v, str) and ('video' in attr_v.lower() or 'playable' in attr_v.lower()):
                    return "video"
                if isinstance(attr_v, (list, tuple)):
                    for item in attr_v:
                        if isinstance(item, str) and ('video' in item.lower() or 'playable' in item.lower()):
                            return "video"

        play_candidates = post.find_all(['button', 'a', 'div', 'span', 'svg'])
        for cand in play_candidates:
            if self._element_has_play_text(cand):
                return "video"

        role_pres = post.find_all(attrs={"role": "presentation"})
        if role_pres:
            for rp in role_pres:
                if rp.find("video"):
                    return "video"
                if rp.find("img"):
                    for cand in rp.find_all(['button', 'svg', 'a', 'div', 'span']):
                        if self._element_has_play_text(cand):
                            return "video"
                else:
                    return "video"

        if post.find("img"):
            return "image"
        return "text"
        
    def extract_posts_with_bs(self):
        """Extract posts data using BeautifulSoup"""
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")
        posts_data = []
        
        posts = soup.find_all("div", {"class": "x1n2onr6 x1ja2u2z"})
        
        for post in posts:
            try:
                # --- POST TEXT ---
                message_elements = post.find_all("div", {"data-ad-preview": "message"})
                post_text = " ".join([msg.get_text(strip=True) for msg in message_elements])
                
                # Fallback for plain-text posts
                if not post_text:
                    fallback_divs = post.find_all("div", class_="xdj266r")
                    post_texts = []
                    for div in fallback_divs:
                        text = div.get_text(" ", strip=True)
                        if text and len(text.split()) > 2:
                            post_texts.append(text)
                    post_text = " ".join(post_texts).strip() if post_texts else None
                
                # --- LIKES, COMMENTS, SHARES ---
                likes_element = post.select_one("span.xt0b8zv.x1jx94hy.xrbpyxo.xl423tq > span > span")
                likes = likes_element.get_text(strip=True) if likes_element else None
                
                comments_element = post.select("div > div > span > div > div > div > span > span.html-span ")
                comments = comments_element[0].text if comments_element else None
                
                shares_element = post.select("div > div > span > div > div > div > span > span.html-span ")
                shares = shares_element[1].text if len(shares_element) > 1 else None

                # --- TIME POSTED ---
                timeelement = post.select_one("div.xu06os2.x1ok221b > span > div > span > span > a > span")
                post_time = timeelement.get_text(strip=True) if timeelement else None

                # --- CONTENT TYPE ---
                content_type = self.detect_content_type(post)

                # --- POST LINK ---
                post_link = None
                for a_tag in post.find_all("a", href=True):
                    href = a_tag["href"]
                    if any(pattern in href for pattern in ["/posts/", "/videos/", "/reel/", "/photo/", "/story/"]):
                        if href.startswith("/"):
                            href = "https://www.facebook.com" + href
                        post_link = href.split("?")[0]
                        break

                posts_data.append({
                    "post_text": post_text,
                    "likes": likes,
                    "comments": comments,
                    "shares": shares,
                    "post_time": post_time,
                    "content_type": content_type,
                    "post_link": post_link
                })
            except Exception as e:
                print("Error extracting post data:", e)
                
        return posts_data
        
    def remove_duplicates(self, data_list):
        """Remove duplicate posts"""
        seen = set()
        unique_data = []
        for data in data_list:
            data_tuple = tuple(data.items())
            if data_tuple not in seen:
                seen.add(data_tuple)
                unique_data.append(data)
        return unique_data
        
    def scrape_posts(self, max_posts):
        """Scrape a specified number of posts"""
        all_posts = []
        
        while len(all_posts) < max_posts:
            posts = self.extract_posts_with_bs()
            all_posts.extend(posts)
            all_posts = self.remove_duplicates(all_posts)
            print(f"Extracted {len(all_posts)} unique posts so far.")
            self.slow_scroll()
            
            if len(all_posts) >= max_posts:
                break
                
        return all_posts[:max_posts]

    def save_to_csv(self, posts_data, filename="facebook_posts.csv"):
        """Save posts data to CSV"""
        df = pd.DataFrame(posts_data)
        df.to_csv(filename, index=False, encoding="utf-8-sig")
        print(f"✅ Saved {len(df)} posts to {filename}")
        return df

    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()


# Example usage
if __name__ == "__main__":
    scraper = FacebookScraper("mail", "password")
    
    try:
        scraper.initialize_driver()
        scraper.login()
        scraper.navigate_to_profile("https://www.facebook.com/accountpage")
        
        posts_data = scraper.scrape_posts(max_posts=600)
        df = scraper.save_to_csv(posts_data) 
        
    finally:
        scraper.close()

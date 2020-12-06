from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd 
from webdriver_manager.chrome import ChromeDriverManager


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)

def scrape_info():
    browser = init_browser()

    # Visit https://mars.nasa.gov/news/
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get the latest title and paragraph text(teaser)
    latest_item = soup.select_one('ul.item_list li.slide')
    latest_title=latest_item.find('div',class_='content_title').get_text()
    latest_teaser=latest_item.find('div',class_='article_teaser_body').get_text()

    
    # Store data in a dictionary
    article_data = {
        "latest_title": latest_title,
        "latest_teaser": latest_teaser
    }

    browser.quit()

    return article_data



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

    # Visit https://space-facts.com/mars/
    url = 'https://space-facts.com/mars/'
    browser.visit(url)

    # Get the facts about Mars and put them in an html table
    mars_facts_df= pd.read_html(url)
    mars_facts_only = mars_facts_df[0]
    mars_facts_html = mars_facts_only.to_html(index=False)


    browser.quit()

    return mars_facts_html


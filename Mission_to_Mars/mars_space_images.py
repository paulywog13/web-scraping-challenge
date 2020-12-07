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

    # Visit https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    full_image = browser.find_by_id("full_image")
    full_image.click()

    browser.click_link_by_partial_text("more info")
    
    # Scrape page into Soup
    html_url2=browser.html
    soup = bs(html_url2, 'html.parser')

    # Get the Featured Mars Image
    mars_image=soup.find_all("figure", class_="lede")
    image_result=mars_image[0].a['href']
    featured_image_url="https://www.jpl.nasa.gov"+image_result
    

    
    # Store data in a dictionary
    featured_image = {
        "featured_image": featured_image_url
    }

    browser.quit()

    return featured_image
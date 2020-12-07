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

    # Visit https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get the hemisphere descriptions
    hemisphere_descriptions=soup.find_all('div', class_='item')
    
    # Save both the image url string for the full resolution hemisphere image, 
    # and the hemisphere title containing the hemisphere name. 
    # Use a Python dictionary to store the data using the keys: img_url and title.

    hemisphere_image_urls=[]
    for hemi in hemisphere_descriptions:
        title=hemi.find('h3').text
        image=hemi.find('a', class_='itemLink product-item')["href"]
        final_url='https://astrogeology.usgs.gov'+image
        browser.visit(final_url)
        html=browser.html
        soup=bs(html, 'html.parser')
        full_image_url='https://astrogeology.usgs.gov'+soup.find("img", class_="wide-image")['src']
        hemisphere_image_urls.append({"title":title, 
                      "image_url":full_image_url})
    

    browser.quit()

    return hemisphere_image_urls


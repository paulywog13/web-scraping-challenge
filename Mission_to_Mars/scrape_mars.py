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
    url1 = 'https://mars.nasa.gov/news/'
    url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    url3 = 'https://space-facts.com/mars/'
    browser.visit(url1)

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

    # browser.quit()

    return article_data

    # browser = init_browser()

    # url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url2)

    full_image = browser.find_by_id("full_image")
    full_image.click()

    browser.click_link_by_partial_text("more info")
    
    # Scrape page into Soup
    html=browser.html
    soup = bs(html, 'html.parser')

    # Get the Featured Mars Image
    mars_image=soup.find_all("figure", class_="lede")
    image_result=mars_image[0].a['href']
    featured_image_url="https://www.jpl.nasa.gov"+image_result
    

    
    # Store data in a dictionary
    featured_image = {
        "featured_image": featured_image_url
    }

    # browser.quit()

    return featured_image

    # browser = init_browser()

    # Visit https://space-facts.com/mars/
    # url3 = 'https://space-facts.com/mars/'
    browser.visit(url3)

    # Get the facts about Mars and put them in an html table
    mars_facts_df= pd.read_html(url3)
    mars_facts_only = mars_facts_df[0]
    mars_facts_html = mars_facts_only.to_html(index=False)

    # Store data in a dictionary
    # mars_facts = {
    #     "mars_facts_table": mars_facts_html
    # }

    # browser.quit()

    return mars_facts_html

    # browser = init_browser()

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
        url4='https://astrogeology.usgs.gov'+image
        browser.visit(url4)
        html=browser.html
        soup=bs(html, 'html.parser')
        full_image_url='https://astrogeology.usgs.gov'+soup.find("img", class_="wide-image")['src']
        hemisphere_image_urls.append({"title":title, 
                      "image_url":full_image_url})
    

    # Store data in a dictionary

    
    browser.quit()

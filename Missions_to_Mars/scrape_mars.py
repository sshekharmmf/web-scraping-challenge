
# Dependencies
import time
from bs4 import BeautifulSoup  as bs
import requests
from splinter import Browser
from selenium import webdriver
import pandas as pd





def init_browser():
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()

    # Create a dictionary for all of the scraped data
    mars_dat = {}

    # Visit the Mars news page. 
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)
 

    # Search for news
    # Scrape page into soup
    html = browser.html
    soup = bs(html, 'html.parser')

    # Find the latest Mars news.
    article = soup.find("div", class_="list_text")
    news_content = article.find("div", class_="article_teaser_body").text
    news_title = article.find("div", class_="content_title").text
    news_date = article.find("div", class_="list_date").text
   
  
    # Add the news date, title and summary to the dictionary
    mars_dat["news_date"] = news_date
    mars_dat["news_title"] = news_title
    mars_dat["summary"] = news_content

   

    # While chromedriver is open go to JPL's Featured Space Image page. 
    JPL_url = "https://jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(JPL_url)

    # Scrape the browser into soup and use soup to find the full resolution image of mars
    # Save the image url to a variable called `featured_image_url`
    html = browser.html
    soup = bs(html, 'html.parser')
    image = soup.find("img", class_="thumb")["src"]
    img_url = "https://jpl.nasa.gov"+image
    featured_image_url = img_url
    # Add the featured image url to the dictionary
    mars_dat["featured_image_url"] = featured_image_url


    # ## Mars Weather 
    twitter_url = "https://twitter.com/marswxreport?lang=en"

    browser.visit(twitter_url)
    tweets=browser.html
    tweets_soup = bs(tweets, 'html.parser')
    Marsweather = tweets_soup.find("div", class_="js-tweet-text-container")
    Mars_weat=Marsweather.text
    marswed2=Mars_weat.replace('\n', ' ')
    # Add the weather to the dictionary
    mars_dat["marswed2"] = marswed2

    # ## Mars Facts
    


    mars_facts = "http://space-facts.com/mars/"
    browser.visit(mars_facts)

    import pandas as pd 
    mars_facts_todf=pd.read_html(mars_facts)
    mars_data=pd.DataFrame(mars_facts_todf[0])
    mars_data.columns=['Mars','Data']
    mars_table=mars_data.set_index("Mars")
    marsdata = mars_table.to_html(classes='marsdata')
    marsdata=marsdata.replace('\n', ' ')


    # Add the Mars facts table to the dictionary
    mars_dat["marsdata"] = marsdata


    # Visit the USGS Astogeology site and scrape pictures of the hemispheres
    USGS_link = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(USGS_link)
    import time 
    html = browser.html
    soup = bs(html, 'html.parser')
    mars_pictures=[]

    for i in range (4):
        time.sleep(5)
        images = browser.find_by_tag('h3')
        images[i].click()
        html = browser.html
        soup = bs(html, 'html.parser')
        partial = soup.find("img", class_="wide-image")["src"]
        img_title = soup.find("h2",class_="title").text
        img_url = 'https://astrogeology.usgs.gov'+ partial
        dictionary={"title":img_title,"img_url":img_url}
        mars_pictures.append(dictionary)
        browser.back()    

    mars_dat["mars_pictures"] =mars_pictures
   
    print(mars_dat)
    print("this is the type: ", type(mars_dat))
    # Return the dictionary
    return mars_dat
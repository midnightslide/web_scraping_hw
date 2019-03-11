#!/usr/bin/env python
# coding: utf-8

# Imports
from bs4 import BeautifulSoup as bs
from splinter import Browser
import time
import pandas as pd 


# In[3]:


# BROWSER MAGIC
def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():

    browser = init_browser()

    # DICTIONARY FOR DATA
    mars_data = {}

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    #SLEEP TIMER - ALLOW THE HTML TO LOAD/POPULATE
    time.sleep(3)

    # BROWSER/SOUP INFO
    html = browser.html
    soup = bs(html, "html.parser")

    # SCRAPE IT UP!
    article = soup.find("div", class_="list_text")
    news_p = article.find("div", class_="article_teaser_body").text
    news_title = article.find("div", class_="content_title").text
    news_date = article.find("div", class_="list_date").text

    mars_data["news_date"] = news_date
    mars_data["news_title"] = news_title
    mars_data["summary"] = news_p

    url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url2)

    # SLEEP TIMER - ALLOW THE HTML TO LOAD/POPULATE
    time.sleep(3)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    image = soup.find("a", class_="button fancybox")["data-fancybox-href"]
    featured_image_url = "https://jpl.nasa.gov"+ image

    mars_data["featured_image_url"] = featured_image_url

    url3 = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url3)

    # SLEEP TIMER - ALLOW THE HTML TO LOAD/POPULATE
    time.sleep(3)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    marsWeather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text

    mars_data["mars_weather"] = marsWeather

    url4 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url4)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    mars_hemis = []

    for i in range (4):
        time.sleep(5)
        images = browser.find_by_tag('h3')
        images[i].click()
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        partial = soup.find("img", class_="wide-image")["src"]
        img_title = soup.find("h2",class_="title").text
        img_url = 'https://astrogeology.usgs.gov'+ partial
        dictionary={"title":img_title,"img_url":img_url}
        mars_hemis.append(dictionary)
        browser.back()

    mars_data['mars_hemis'] = mars_hemis

    url5 = "https://space-facts.com/mars/"
    browser.visit(url5)

    grab = pd.read_html(url5)
    mars_info = pd.DataFrame(grab[0])
    mars_info.columns = ['Mars', 'Data']
    mars_table = mars_info.set_index("Mars")
    marsInfo = mars_table.to_html(classes='marsInfo')
    marsInfo = marsInfo.replace('\n', ' ')

    mars_data["mars_table"] = marsInfo

    return mars_data


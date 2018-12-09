#Dependencies
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
from flask import Flask, render_template, redirect
import pymongo


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)


def scrape():
    browser = init_browser()
    

    #Nasa Mars News
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    #Scraping for title and paragraph
    #title
    big_title = soup.find('div', class_="content_title")
    news_title = big_title.text

    #paragraph
    p_class = soup.find('div', class_="article_teaser_body")
    news_p = p_class.text


    #JPL Mars Space image
    featured_image= "https://www.jpl.nasa.gov/spaceimages/images/wallpaper/PIA19964-1920x1200.jpg"


    #Mars Weather
    #scraping the twitter page
    url3 = "https://twitter.com/marswxreport?lang=en"
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(url3)
    html3 = browser.html
    soup3 = BeautifulSoup(html3, 'html.parser')
    #looking for most current info
    tweet = soup3.find("div", class_="js-tweet-text-container")
    #mars weather
    current_tweet = tweet.text

    #Mars Facts
    #getting the info from the url
    facts_url = "https://space-facts.com/mars/"
    mars_tables = pd.read_html(facts_url)
    mars_tables
    #mars tables is a list

    #renaming as a dataframe
    marsdf = mars_tables[0]
    marsdf.columns = ["", "Values"]
    marsdf
    #gonna convert to HTML
    html_mars = marsdf.to_html()
    html_mars

    #strip unwanted lines
    html_mars = html_mars.replace('\n', '')

    #Mara Hemisphere
    hemisphere_image_urls = [
                            {"title": "Valles Marineris Hemisphere", "img_url": "https://astrogeology.usgs.gov/cache/images/7cf2da4bf549ed01c17f206327be4db7_valles_marineris_enhanced.tif_full.jpg"},
                            {"title": "Cerberus Hemisphere", "img_url": "https://astrogeology.usgs.gov/cache/images/cfa62af2557222a02478f1fcd781d445_cerberus_enhanced.tif_full.jpg"},
                            {"title": "Schiaparelli Hemisphere", "img_url": "https://astrogeology.usgs.gov/cache/images/3cdd1cbf5e0813bba925c9030d13b62e_schiaparelli_enhanced.tif_full.jpg"},
                            {"title": "Syrtis Major Hemisphere", "img_url": "https://astrogeology.usgs.gov/cache/images/ae209b4e408bb6c3e67b6af38168cf28_syrtis_major_enhanced.tif_full.jpg"},
                            ]

    data_mars={ "news_title": news_title,
                "news_paragraph": news_p,
                "featured_image": featured_image,
                "twitter": current_tweet,
                "mars_info": html_mars,
                "hemisphere_images": hemisphere_image_urls
                }


    #quit the browser
    browser.quit()
    return data_mars


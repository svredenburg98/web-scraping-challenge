import os
from bs4 import BeautifulSoup
import requests
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
import pandas as pd

#scrape nasa articles
def scrape():
    url = 'https://mars.nasa.gov/news/'

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    titles = soup.find_all(class_="content_title")


    teasers = soup.find_all(class_="article_teaser_body")

    title1 = titles[1].find('a').text

    teaser1 = teasers[0].text

    #scrape JPL

    # jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    # browser.visit(jpl_url)

    # browser.click_link_by_partial_text('FULL IMAGE')

    # html2 = browser.html
    # soup2 = BeautifulSoup(html2, 'html.parser')

    # images = soup2.find_all(class_="fancybox-image")


    # image = images[0]
    # link = image.get('src')
    # featured_image_url = 'https://www.jpl.nasa.gov' + link

    #scrape mars table

    mars_table = 'https://space-facts.com/mars/'

    tables = pd.read_html(mars_table)


    mars_df = tables[0]

    html_mars_table = mars_df.to_html()

    #scrape hemispheres

    pic_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(pic_url)

    hemispheres=['Cerberus', 'Schiaparelli', 'Syrtis Major', 'Valles Marineris']
    img_list = []

    for hemisphere in hemispheres:
        browser.click_link_by_partial_text(hemisphere)
        html3 = browser.html
        soup3 = BeautifulSoup(html3, 'html.parser')
        hemi = soup3.find_all("img")
        img_list.append(hemi[5])
        browser.back()

    url_list=[]
    for img in img_list:
        link = img.get('src')
        url = 'https://astrogeology.usgs.gov' + link
        url_list.append(url)

    hemisphere_image_urls = []
    for hemisphere, url in zip(hemispheres, url_list):
        hemisphere_image_urls.append({"title": hemisphere + " Hemisphere", "img_url": url})

    final_dict = {"news_title": title1, 
                  "news_p": teaser1,
                  #"featured_image": featured_image_url,
                  "mars_table": html_mars_table,
                  "hemisphere_pics": hemisphere_image_urls}

    return final_dict

    









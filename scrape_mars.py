import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
import time

def scrape():
    #get from the mars.nasa website an article title and teaser text
    executable_path = {'executable_path': '/chromedriver'}
    browser = Browser('chrome',  headless=False)
    browser.visit('https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest')
    time.sleep(2)
    soup = BeautifulSoup(browser.html, 'html.parser')
    soup2=soup.find('div',class_='image_and_description_container')
    title=soup2.find('a')['href']
    title=title.split('/')
    title=title[3].split('-')
    seperator = ' '
    mars_title = seperator.join(title)
    mars_para=soup2.find('div', class_='rollover_description_inner').text

    #get the featured image off the nasa webpage
    browser.visit('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')
    time.sleep(2)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(2)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    img = soup.find('img',class_='fancybox-image')
    featured_image_url = img['src']

    #get mars weather from twitter
    browser.visit('https://twitter.com/marswxreport?lang=en')
    time.sleep(2)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    soup2 = soup.find('div', class_="css-901oao r-jwli3a r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0")
    mars_weather = soup2.find('span',class_="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0").text

    #get the  table of mars facts from space facts
    browser.visit('https://space-facts.com/mars/')
    time.sleep(2)
    mars_fact = browser.html

    #get the 4 hemisphere pictures
    partial=['Cerberus','Schiaparelli','Syrtis','Valles Marineris']
    mars_hemispheres = []
    for i in range(4):
        browser.visit('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars')
        time.sleep(2)
        browser.click_link_by_partial_text(partial[i])
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        soup2 = soup.find('section',class_='block metadata')
        img_url = soup2.find('a')['href']
        title = soup2.find('h2').text
        hemis = {title:img_url}
        mars_hemispheres.append(hemis)
    browser.quit()
    return(mars_title,mars_para,featured_image_url,mars_weather,mars_fact,mars_hemispheres)
{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "#Description:  012-Web_Scraping_Homework\n",
    "#\n",
    "#\n",
    "#   Modification Summary:\n",
    "#   DD-MMM-YYYY    Author          Description\n",
    "#   16-Aug-2019    Stacey Smith     Initial Creation\n",
    "#\n",
    "#"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import requests\n",
    "import pymongo\n",
    "import os\n",
    "\n",
    "from splinter import Browser\n",
    "from splinter.exceptions import ElementDoesNotExist\n",
    "from bs4 import BeautifulSoup as bs"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Step 1 - Scraping"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Set the URL and pull the html from the page\n",
    "mars_url = 'https://mars.nasa.gov/news/'\n",
    "mars_html = requests.get(mars_url)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Use bs to parse the page and return the source contents\n",
    "mars_soup = bs(mars_html.text, 'html.parser')\n",
    "#print(mars_soup.prettify())"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "NASA Mars News"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text.\n",
    "# Assign the text to variables that you can reference later.\n",
    "nasa_titles = mars_soup.body.find('div', class_='content_title')\n",
    "latest_title = nasa_titles.text.strip()\n",
    "latest_title\n",
    "\n",
    "\n",
    "nasa_p = mars_soup.body.find('div', class_='rollover_description_inner')\n",
    "p_text = nasa_p.text.strip()\n",
    "p_text"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "JPL Mars Space Images - Featured Image"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Visit the url for JPL Featured Space Image https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars\n",
    "# Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called featured_image_url.\n",
    "# Make sure to find the image url to the full size .jpg image.\n",
    "# Make sure to save a complete url string for this image.\n",
    "\n",
    "executable_path = {'executable_path': 'chromedriver.exe'}\n",
    "browser = Browser('chrome', **executable_path, headless=False)\n",
    "\n",
    "jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'\n",
    "jpl_browser.visit(jpl_url)\n",
    "\n",
    "jpl_full_image = jpl_browser.find_by_id('full_image')\n",
    "jpl_image_url = jpl_full_image['data-fancybox-href']\n",
    "\n",
    "featured_image_url = 'https://www.jpl.nasa.gov' + jpl_image_url\n",
    "featured_image_url"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Mars Weather"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Visit the Mars Weather twitter account @ https://twitter.com/marswxreport?lang=en \n",
    "# scrape the latest Mars weather tweet from the page. \n",
    "\n",
    "# Set the URL and pull the html from the page\n",
    "twitter_url = 'https://twitter.com/marswxreport?lang=en'\n",
    "twitter_html = requests.get(twitter_url)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Use bs to parse the page and return the source contents\n",
    "twitter_soup = bs(twitter_html.text, 'html.parser')\n",
    "#print(twitter_soup.prettify())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Save the tweet text for the weather report as a variable called mars_weather.\n",
    "tweets = twitter_soup.find('div', class_='js-tweet-text-container')\n",
    "tweets_p = tweets.find('p')\n",
    "\n",
    "mars_weather = tweets_p.text.strip()\n",
    "mars_weather"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Mars Facts"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Visit the Mars Facts webpage @ https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars\n",
    "\n",
    "mars_facts = 'https://space-facts.com/mars/'\n",
    "tables = pd.read_html(mars_facts)\n",
    "tables"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.\n",
    "mars_facts_df = tables[0]\n",
    "mars_facts_df.columns = ['Fact','Mars', 'Earth']\n",
    "mars_facts_df.set_index('Fact', inplace=True)\n",
    "\n",
    "del mars_facts_df['Earth']\n",
    "\n",
    "mars_facts_df.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Use Pandas to convert the data to a HTML table string.\n",
    "html_table = mars_facts_df.to_html()\n",
    "mars_facts_html = html_table.replace('\\n', '')\n",
    "\n",
    "mars_facts_html"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Mars Hemispheres"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Visit the USGS Astrogeology site @ https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars\n",
    "executable_path = {'executable_path': 'chromedriver.exe'}\n",
    "usgs_browser = Browser('chrome', **executable_path, headless=False)\n",
    "\n",
    "usgs_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'\n",
    "usgs_browser.visit(usgs_url)\n",
    "usgs_soup = bs(usgs_browser.html, 'html.parser')\n",
    "#print(usgs_soup.body.prettify())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 119,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced\n",
      "https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced\n",
      "https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced\n",
      "https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "[{'title': 'Cerberus Hemisphere',\n",
       "  'url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif'},\n",
       " {'title': 'Schiaparelli Hemisphere',\n",
       "  'url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif'},\n",
       " {'title': 'Syrtis Major Hemisphere',\n",
       "  'url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif'},\n",
       " {'title': 'Valles Marineris Hemisphere',\n",
       "  'url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif'}]"
      ]
     },
     "execution_count": 119,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# obtain high resolution images for each of Mar's hemispheres.\n",
    "# You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.\n",
    "# Save both the image url string for the full resolution hemisphere image, and the Hemisphere title \n",
    "# containing the hemisphere name. \n",
    "# Use a Python dictionary to store the data using the keys img_url and title.\n",
    "# Append the dictionary with the image url string and the hemisphere title to a list. \n",
    "# This list will contain one dictionary for each hemisphere.\n",
    "\n",
    "hem_items = usgs_soup.find_all('div', class_='description')\n",
    "\n",
    "highres_images = []\n",
    "\n",
    "for item in hem_items:\n",
    "    hem_image = item.find('a', class_='itemLink product-item')\n",
    "    hem = hem_image.get('href')\n",
    "    hem_url = 'https://astrogeology.usgs.gov' + hem\n",
    "    print(hem_url)\n",
    "    usgs_browser.visit(hem_url)\n",
    "    \n",
    "    h_dict = {}\n",
    "    \n",
    "    hem_soup = bs(usgs_browser.html, 'html.parser')\n",
    "    hs_url = hem_soup.find('a', text='Original').get('href')\n",
    "    hs_title = hem_soup.find('h2', class_='title').text.replace(' Enhanced', '')\n",
    "    \n",
    "    h_dict['title'] = hs_title\n",
    "    h_dict['url'] = hs_url\n",
    "    \n",
    "    highres_images.append(h_dict)\n",
    "    \n",
    "highres_images"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}

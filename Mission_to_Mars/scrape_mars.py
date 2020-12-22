# Import Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

def init_browser():
    executable_path = {'executable_path': "chromedriver.exe"}
    browser = Browser('chrome', **executable_path, headless=False)


# ## Nasa Mars News
# * Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. 
# * Assign the text to variables that you can reference later.

def scrape_info():
    browser = init_browser()

    # Visit the webpage to scrape the required data
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    # Use time.sleep to load the webpage
    time.sleep(2)
    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')

    content = soup.find("div", class_='content_page')

    titles = content.find_all("div", class_='content_title')
    news_title = titles[0].text.strip()

    article_text = content.find("div", class_='article_teaser_body')
    news_p = article_text.text.strip()


    # ## JPL Mars Space Images - Featured Image
    # * Visit the url, https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars, for JPL Featured Space Image.
    # * Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called `featured_image_url`.
    # * Make sure to find the image url to the full size `.jpg` image.
    # * Make sure to save a complete url string for this image.

    # Visit the webpage to scrape the required data
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    # Use time.sleep to load the webpage
    time.sleep(2)
    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')

    base_url = url.split('/spaceimages')[0]
    img_url = soup.find("li", class_='slide').a['data-fancybox-href']
    featured_image_url = base_url + img_url


    # ## Mars Facts
    # * Visit the Mars Facts webpage, [https://space-facts.com/mars/](https://space-facts.com/mars/) and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    # * Use Pandas to convert the data to a HTML table string.

    # Visit the webpage to scrape the required data
    url = 'https://space-facts.com/mars/'
    browser.visit(url)
    # Use time.sleep to load the webpage
    time.sleep(2)
    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')
    # Use Panda's `read_html` to parse the url
    tables = pd.read_html(url)

    mars_df = tables[0]
    mars_df.columns = ['Description', 'Value']
    mars_df.set_index('Description', inplace=True)

    # Use Pandas to convert the data to a HTML table string
    mars_facts = mars_df.to_html()
    mars_facts.replace("\n", "")

    mars_df.to_html('mars_facts.html')


    # ## Mars Hemispheres
    # * Visit the USGS Astrogeology site, https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars, to obtain high resolution images for each of Mar's hemispheres.
    # * Click each of the links to the hemispheres in order to find the image url to the full resolution image.
    # * Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys `img_url` and `title`.
    # * Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.

    # Visit the webpage to scrape the required data
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    # Use time.sleep to load the webpage
    time.sleep(2)
    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')

    base_url = url.split('/search')[0]

    # Create a list to hold all the hemispheres information
    hemisphere_image_urls = []

    # Retrieve all elements that contain hemispheres images
    results = soup.find_all('div', class_='item')

    # Iterate through each hemisphere
    for result in results:

        hemisphere_dict = {}

        # Scrape hemisphere title
        title = result.find('h3').text
        
        # url to obtain high resolution images each hemisphere
        img_page_url = base_url + result.find('a', class_='itemLink')['href']
        
        # visit the page
        browser.visit(img_page_url)
        # HTML object
        page_html = browser.html
        # Parse html with Beautiful Soup
        soup = bs(page_html, 'html.parser')
        
        # url where the high resolution image is
        downloads = soup.find('div', class_='downloads')
        img_url = downloads.find('a')['href']

        # Save the title and img_url in the dictionary
        hemisphere_dict['title'] = title
        hemisphere_dict['img_url'] = img_url

        # Add the hemisphere dictionary to the list
        hemisphere_image_urls.append(hemisphere_dict)


    # Store scraped data in a dictionary
    scraped_mars_data = {
            "news_title" : news_title,
            "news_p" : news_p,
            "featured_image_url" : featured_image_url,
            "mars_facts" : mars_facts,
            "hemisphere_image_urls" : hemisphere_image_urls
    }
    # Close the browser after scraping
    browser.quit()
    # Return scraped_data
    return scraped_mars_data





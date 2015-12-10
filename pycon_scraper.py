# Pycon Abstract Scraper
from lxml import html
import requests
import json

# Define the function to return JSON of information from year of pycon
def get_pycon_info(year):
    pycon_base = 'https://us.pycon.org'
    pycon_contents = '/' + str(year) + '/schedule/talks/list'

    # Get links for pycon
    pycon_page = requests.get(pycon_base + pycon_contents)
    pycon_content_tree = html.fromstring(pycon_page.text)

    # Create links to individual talks
    pycon_links = pycon_content_tree.xpath('/html/body/div/div/div[2]/div/div/div/div/h3/a/@href|'+\
                                           '//*[@id="content"]/div[2]/div/div/div/div/div/div/div/h3/a/@href')

    talk_title = []
    talk_speaker = []
    talk_level = []
    talk_category = []
    talk_description = []

    counter = 1 # For printing purposes, probably better to use 'enumerate()' in loop

    print('Found ' + str(len(pycon_links)) + ' talks.') # Print off how many talks found.
    
    # Loop through links, get all information.
    for link in pycon_links:
        print('Getting link ' + str(counter) + ' out of ' + str(len(pycon_links)))
        talk_html = pycon_base + link
        talk_page = requests.get(talk_html)
        talk_tree = html.fromstring(talk_page.text)
        # Annoying XPath below (credit due to Chrome's 'inspect' function)
        talk_title1 = talk_tree.xpath('/html/body/div/div/div[2]/div/div/h2/text()|'+\
                                      '//*[@id="content"]/div[2]/div/div/div/div/div/h2/text()')
        talk_speaker1 = talk_tree.xpath('/html/body/div/div/div[2]/div/div/h4[2]/a/text()|'+\
                                        '//*[@id="content"]/div[2]/div/div/div/div/div/h4[2]/a/text()')
        talk_level1 = talk_tree.xpath('/html/body/div/div/div[2]/div/div/dl/dt[1]/text()|'+\
                                      '//*[@id="content"]/div[2]/div/div/div/div/div/dl/dd[1]/text()')
        talk_category1 = talk_tree.xpath('/html/body/div/div/div[2]/div/div/dl/dd[2]/text()|'+\
                                         '//*[@id="content"]/div[2]/div/div/div/div/div/dl/dd[2]/text()')
        talk_description1 = talk_tree.xpath('/html/body/div/div/div[2]/div/div/div/p/text()|' +\
                                            '/html/body/div/div/div[2]/div/div/div[2]/p[2]/a/text()|' +\
                                            '/html/body/div/div/div[2]/div/div/div[2]/ul/li/text()|' +\
                                            '/html/body/div/div/div[2]/div/div/div[2]/ol/li/ul/li/text()|'+\
                                            '//*[@id="content"]/div[2]/div/div/div/div/div/div[2]/p/text()|'+\
                                            '//*[@id="content"]/div[2]/div/div/div/div/div/div/text()|'+\
                                            '//*[@id="content"]/div[2]/div/div/div/div/div/div/ul/li/text()')
        talk_title.append(talk_title1)
        talk_speaker.append(talk_speaker1)
        talk_level.append(talk_level1)
        talk_category.append(talk_category1)
        talk_description.append(talk_description1)
        counter +=1

    talk_data = {}
    talk_data['title'] = talk_title
    talk_data['speaker'] = talk_speaker
    talk_data['level'] = talk_level
    talk_data['category'] = talk_category
    talk_data['description'] = talk_description
    return(json.dumps(talk_data)) # Convert to JSON

if __name__ == "__main__":
    year = 2014
    talk14_data = get_pycon_info(year)
    # Probably need to add some way to write to file (SQL? CSV?)...

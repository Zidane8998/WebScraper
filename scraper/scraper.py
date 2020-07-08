from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            return resp.content

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None)


def log_error(e):
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    """
    print(e)


def read_scrape_list():
    """
    Reads scrape_list.txt for article links, returns a list of URLs.
    """
    url_list = []

    scrape_list = open('scrape_list/scrape-list.txt', 'r')

    # Read and print the entire file line by line
    for line in scrape_list:
        url_list.append(line)

    return url_list


def parse_content(raw_html):
    """
    Parse raw HTML and return a BeautifulSoup object.
    """
    return BeautifulSoup(raw_html, 'html.parser')


def scrape(url):
    """
    Initiates the web scrape, parses file and writes the result to disk.
    """

    # get raw HTML from URL
    raw_html = simple_get(url)

    # parse raw HTML using BeautifulSoup
    parsed_html = parse_content(raw_html)

    # get and save article name (only works if article uses H1 tag for title, which they *should)
    article_title = parsed_html.select('h1')

    # only save the text attribute of the h1
    if article_title is not None:
        article_title = article_title[0].text

    content = {}

    # loop through and save only encoded, line-broken paragraph text to results dictionary
    for i, li in enumerate(parsed_html.select('p')):
        raw_p = li.text
        content[i] = raw_p

    # create the new file by opening it with the desired name in write mode
    file = open("articles/" + article_title + ".html", "w")

    file.write("<html>")

    # print result dictionary directly to file
    for cur in content.values():
        file.write("<p>")
        file.write(cur)
        file.write("</p>")

    file.write("</html>")

    # close file, job is complete
    file.close()


def initiate_scrape():
    """
    Called from main.py. Begins the scraping process by reading from the scrape list.
    """
    url_list = read_scrape_list()

    for url in url_list:
        scrape(url)

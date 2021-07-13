"""os for define path, and create dir
get just to unload the html
and lxml for job Xpath
"""
from os import path, mkdir
from datetime import date
from requests import get
import lxml.html as html

"""This is links and Xpath exclusive for titles, summarys and bodys."""
HOME_URL = 'https://nytimes.com'
XPATH_LINK_TO_ARTICLE = '//section[@class="story-wrapper"]//a/@href'
XPATH_TITLE = '//h1//text()'
XPATH_SUMMARY = '//p[@id="article-summary"]/text()'
XPATH_BODY = '//section[@name="articleBody"]//p/text()'


def parse_notice(link, today):
    """Receive each link of a news and create a file with the title of the news."""
    try:
        response = get(link)
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)
            try:
                title = parsed.xpath(XPATH_TITLE)[0]
                title = title.replace('\"', '')
                summary = parsed.xpath(XPATH_SUMMARY)[0]
                body = parsed.xpath(XPATH_BODY)
            except IndexError:
                return IndexError
            """Create every file with the title news."""
            with open(f'{today}/{title}.txt','w', encoding='utf-8') as file:
                file.write(title)
                file.write('\n\n')
                file.write(summary)
                file.write('\n\n')
                for line in body:
                    file.write(line)
                    file.write('\n')
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError:
        print(ValueError)


def parse_home():
    """Extract links from news, and create dir with today's date."""
    try:
        response = get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            today = date.today().strftime('%d-%m-%Y')
            if not path.isdir(today):
                mkdir(today)
            for link in links_to_notices:
                parse_notice(link, today)
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError:
        print(ValueError)

if __name__ == '__main__':
    parse_home()

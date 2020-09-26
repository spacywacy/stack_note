import os
import requests
import json
from bs4 import BeautifulSoup


def main():
	url = 'https://stackoverflow.com/a/2427389/11623643'
	re = requests.get(url)
	soup = BeautifulSoup(re.content, 'html.parser')
	

	answer_section = soup.find_all(id='answer-{}'.format(2427389))[0]
	post_content = answer_section.find_all(class_='s-prose js-post-body')
	text = '\n'.join([x.text for x in post_content])
	print(text)















if __name__ == '__main__':
	main()








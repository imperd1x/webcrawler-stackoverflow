import os
import re
import time
import json
import requests
from bs4 import BeautifulSoup
import urllib.parse as urlparse


class Questions:

    url_base = "https://stackoverflow.com"
    uri_base = "/questions?tab=votes"
    res = requests.get(url_base+uri_base)
    soup = BeautifulSoup(res.text, "html.parser")

    questions_data = {
        "questions": []
    }

    def get_questions_from_page(self):

        # Questions list
        questions = self.soup.select(".question-summary")
        for item in questions:
            # Get Info from each item
            q = item.select_one('.question-hyperlink').getText()
            vote_count = item.select_one('.vote-count-post').getText()
            link = item.select_one('.question-hyperlink').get('href')
            views = item.select_one('.views').attrs['title']
            views = re.sub('[^0-9]', '', str(views))
            q_id = link.split('/')[2]

            self.save_question_id(q_id)

            # Get total'[^0-9,]', "" of answers
            answers = item.find("div", class_="status answered")
            answers = re.sub('<[^>]+>', '', str(answers))

            try:
                re.findall("\\d+", answers)[0]
            except IndexError:
                answers = str(0)
            else:
                answers = str(re.findall("\\d+", answers)[0])

            # Check if have Answered Accepted
            answered_accepted = item.find(
                "div", class_="status answered-accepted")
            answered_accepted = re.sub('<[^>]+>', '', str(answered_accepted))

            # Try to catch information about Answer
            try:
                re.findall("\\d+", answered_accepted)[0]
            except IndexError:
                answered_accepted = 'False'
            else:
                vote_count = item.select_one('.vote-count-post').getText()
                answers = str(re.findall("\\d+", answered_accepted)[0])
                answered_accepted = 'True'

            self.questions_data['questions'].append({
                "id": q_id,
                "question": q,
                "answers": answers,
                "views": views,
                "vote_count": vote_count,
                "link": link
            })

        return json.dumps(self.questions_data)

    def get_next_page(self, url):
        try:
            output = [a.get('href') for a in self.soup.select_one(
                ".pager").find_all('a', {'rel': 'next'}, href=True)][-1]
        except IndexError:
            output = 0
        else:
            return output

    def save_question_id(self, question_id):
        with open("./question_ids.txt", "r+") as file:
            for line in file:
                if question_id in line:
                    break
            else:  # not found, we are at the eof
                file.write(question_id+'\n')  # append missing data

    def first_sprint(self):
        # Get data from first page
        questions_json = self.get_questions_from_page()
        
        # Save on the file
        f = open('./results/1.txt', 'w')
        f.write(questions_json)
        f.close()

        # Restart questions data
        self.questions_data = {
            "questions": []
        }

        # Explore other pages 
        self.explore()

    def explore(self):

        print('\n')
        print(65*'*')
        print('* Web Crawler to stackoverflow.com')
        print('* This is example how get all questions')
        print('* Cristiano Perdigao <https://github.com/cristianodpp>')
        print(65*'*')
        print('\n')
        print('| Connecting...')

        count_group_pages = 0
        limit_to_merge = 2

        while True:
            time.sleep(1)
            get_pagination = self.get_next_page(self.url_base+self.uri_base)
            if get_pagination is None:
                print('\n')
                print(65*'=')
                print('Success! Nothing more to do.')
                break
            else:
                parsed = urlparse.urlparse(get_pagination)
                page_id = urlparse.parse_qs(parsed.query)['page'][0]

                if(os.path.exists('./results/'+page_id+'.txt')):
                    print(65*'=')
                    print('| ' + 'Page ===> ' + get_pagination)
                    print('| Skipped, file already exist.')
                else:
                    questions_json = self.get_questions_from_page()

                    print(65*'=')
                    for i in range(101):
                        print('| ' + 'Page ===> ' + get_pagination +
                              '{:25}%'.format(i), end='\r')
                        time.sleep(.03)

                    print('\n| Done. ')

                    if(count_group_pages == limit_to_merge):
                        f = open('./results/'+page_id+'.txt', 'w')
                        f.write(questions_json)
                        f.close()
                        count_group_pages = 0
                        self.questions_data = {
                            "questions": []
                        }
                    else:
                        count_group_pages += 1

            uri_base = get_pagination
            res = requests.get(self.url_base+uri_base)
            self.soup = BeautifulSoup(res.text, "html.parser")

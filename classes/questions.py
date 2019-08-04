import os
import re
import time
import json
import requests
from core import dbconnection
from bs4 import BeautifulSoup
import urllib.parse as urlparse


class Questions:

    db = dbconnection.database()
    url_base = "https://stackoverflow.com"
    uri_base = "/questions?tab=votes"
    res = requests.get(url_base+uri_base)
    soup = BeautifulSoup(res.text, "html.parser")

    questions_data = []

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
                answered_accepted = 0
            else:
                vote_count = item.select_one('.vote-count-post').getText()
                answers = str(re.findall("\\d+", answered_accepted)[0])
                answered_accepted = 1

            self.questions_data.append({
                "id": q_id,
                "question": q,
                "answers": answers,
                "views": views,
                "vote_count": vote_count,
                "answered_accepted": answered_accepted,
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

        # Get pagination 
        get_pagination = self.url_base+self.uri_base

        print(65*'=')
        for i in range(101):
            print('| ' + 'Page ===> ' + get_pagination +
                    '{:25}%'.format(i), end='\r')
            time.sleep(.03)

        print('\n| Done. ')

        # Send the question to insert on database
        self.db.insertBulkList(questions_json)

        # Restart questions data
        self.questions_data = []

        # Explore other pages
        self.explore()

    def explore(self):

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
                questions_json = self.get_questions_from_page()

                print(65*'=')
                for i in range(101):
                    print('| ' + 'Page ===> ' + get_pagination +
                        '{:25}%'.format(i), end='\r')
                    time.sleep(.03)

                print('\n| Done. ')

                if(count_group_pages == limit_to_merge):
                    self.db.insertBulkList(questions_json)
                    count_group_pages = 0
                    self.questions_data = []
                else:
                    count_group_pages += 1

            uri_base = get_pagination
            res = requests.get(self.url_base + uri_base)
            self.soup = BeautifulSoup(res.text, "html.parser")

#!/usr/bin/python3

from classes import questions as q
import sys

# Hide errors
sys.tracebacklimit = 0

if __name__ == "__main__":

    print('\n')
    print(65*'*')
    print('* Web Crawler to stackoverflow.com')
    print('* This is example how get all questions')
    print('* Cristiano Perdigao <https://github.com/cristianodpp>')
    print(65*'*')
    print('\n')

    q = q.Questions()
    q.first_sprint()

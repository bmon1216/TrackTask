"""
Title:      setup.py
Desc:       sets up the database for tracktask app
"""
import os
from pathlib import Path

from tracktask import db
from tracktask import models

DIR_HERE = Path(__file__).parent

if not os.path.exists(DIR_HERE / "simplist.db"):
    db.create_all()

    user_1 = models.User(user_name='Bryan',
                         user_email='bmon@bmontech.com',
                         password='password', )
    user_2 = models.User(user_name='Beth',
                         user_email='beth@bmontech.com',
                         password='password', )

    task_1 = models.Task(task_name='Create SimpleList application',
                         text='Create a program to act as a task organizer as well as showcase the Flask web framework',
                         date_posted='JUN-23-2022',
                         status=False,
                         date_complete=None,
                         user_id=1, )
    task_2 = models.Task(task_name='Python certificate program',
                         text='Complete the 8 month program to learn how to make web applications using Python',
                         date_posted='AUG-22-2021',
                         status=True,
                         date_complete='JUN-09-2021',
                         user_id=1, )
    task_3 = models.Task(task_name='Create MagicLookup',
                         text='MTG card lookup and database storage. Will use the Django framework',
                         date_posted='JUN-19-2022',
                         status=False,
                         date_complete=None,
                         user_id=1, )
    task_4 = models.Task(task_name='Create GitHub account',
                         text='create an account and move projects to a public repo',
                         date_posted='SEP-22-2021',
                         status=True,
                         date_complete='SEP-27-2021',
                         user_id=1, )

    db.session.commit()

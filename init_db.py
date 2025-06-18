import os
from datetime import datetime

import  psycopg2

connection = psycopg2.connect(
    host = "localhost",
    database ="ToDoApp_DB",
    user = os.getenv('DB_USERNAME'),
    password = os.getenv('DB_USERNAME')
)

cur = connection.cursor()

cur.execute('DROP TABLE IF EXISTS task;')
cur.execute('''
            CREATE TABLE task
            id serial PRIMARY KEY,
            title VARCHAR(50) NOT NULL UNIQUE,
            description VARCHAR(250) NOT NULL,
            is_done BOOLEAN,
            created_on TIMESTAMP;
            ''')
cur.execute('INSERT INTO task (title, description, is_done, created_on)'
            'VALUES (%s, %s, %s, %s);',
            (
                'Devops Final',
                'Create a project, which summarizes all the topics we\'ve learned this semester into one big assignment',
                False,
                datetime(2025,6,18)
                )
            )
connection.commit()

cur.close()
connection.close()
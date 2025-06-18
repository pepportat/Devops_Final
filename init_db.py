import os
from datetime import datetime
import  psycopg2
from flask.cli import load_dotenv

class DB_Connection:
    load_dotenv()
    connection = psycopg2.connect(
        host = "localhost",
        database ="ToDoApp_DB",
        user = os.getenv('DB_USERNAME'),
        password = os.getenv('DB_PASSWORD')
    )
    cursor =connection.cursor()

    def insert(self, title, description, is_done, created_on=datetime.now()):
        self.cursor.execute(
            "INSERT INTO task (title, description, is_done, created_on) values (%s, %s, %s, %s)",
            (title, description, is_done, created_on)
        )

    def get_by_id(self, task_id):
        self.cursor.execute(
            'SELECT * FROM task WHERE task_id = %s',
            task_id
        )

    def get_all(self):
        self.cursor.execute('SELECT * FROM task')

    def get_by_title(self, title):
        self.cursor.execute(
            'SELECT * FROM task WHERE title = %s',
            title
        )

    def delete_by_id(self, task_id):
        self.cursor.execute(
            'DELETE FROM task WHERE task_id = %S',
            task_id
        )

    def delete_by_title(self, title):
        self.cursor.execute(
            'DELETE FROM task WHERE title = %S',
            title
        )

cur = DB_Connection.cursor

cur.execute('DROP TABLE IF EXISTS task;')
cur.execute('''
                CREATE TABLE task (
                task_id serial PRIMARY KEY,
                title VARCHAR(50) NOT NULL UNIQUE,
                description VARCHAR(250) NOT NULL,
                is_done BOOLEAN,
                created_on TIMESTAMP);
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
DB_Connection.connection.commit()

cur.close()
DB_Connection.connection.close()
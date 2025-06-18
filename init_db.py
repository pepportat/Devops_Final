import os
from datetime import datetime
import  psycopg2
from flask.cli import load_dotenv

class DB_Connection:

    def __init__(self):
        load_dotenv()
        self.connection = self.get_connection()
        self.cursor = self.connection.cursor()

    def get_connection(self):
        return psycopg2.connect(
            host = "localhost",
            database ="ToDoApp_DB",
            user = os.getenv('DB_USERNAME'),
            password = os.getenv('DB_PASSWORD')
        )

    cursor =get_connection().cursor()

    def insert(self, title, description, is_done, created_on=datetime.now()):
        self.cursor.execute(
            "INSERT INTO task (title, description, is_done, created_on) values (%s, %s, %s, %s)",
            (title, description, is_done, created_on)
        )
        self.connection.commit()

    def get_by_id(self, task_id):
        self.cursor.execute(
            'SELECT * FROM task WHERE task_id = %s',
            (task_id,)
        )
        self.connection.commit()

    def get_all(self):
        self.cursor.execute('SELECT * FROM task')
        return self.cursor.fetchall()


    def get_by_title(self, title):
        self.cursor.execute(
            'SELECT * FROM task WHERE title = %s',
            (title,)
        )
        self.connection.commit()


    def delete_by_id(self, task_id):
        self.cursor.execute(
            'DELETE FROM task WHERE task_id = %S',
            (task_id,)
        )
        self.connection.commit()

    def delete_by_title(self, title):
        self.cursor.execute(
            'DELETE FROM task WHERE title = %s',
            (title,)
        )
        self.connection.commit()

    def create_table(self):
        self.cursor.execute('DROP TABLE IF EXISTS task;')
        self.cursor.execute('''
                        CREATE TABLE task (
                        task_id serial PRIMARY KEY,
                        title VARCHAR(50) NOT NULL UNIQUE,
                        description VARCHAR(250) NOT NULL,
                        is_done BOOLEAN,
                        created_on TIMESTAMP);
                    ''')
        self.connection.commit()

    def seed_table(self):
        self.cursor.execute('INSERT INTO task (title, description, is_done, created_on)'
                    'VALUES (%s, %s, %s, %s);',
                    (
                        'Devops Final',
                        'Create a project, which summarizes all the topics we\'ve learned this semester into one big assignment',
                        False,
                        datetime(2025, 6, 18)
                    )
                    )
        self.connection.commit()

    def close_connection(self):
        self.cursor.close()
        self.connection.close()

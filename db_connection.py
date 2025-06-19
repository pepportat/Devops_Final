import os
from datetime import datetime
from os import getenv

import  psycopg2
from flask.cli import load_dotenv

class DB_Connection:

    def __init__(self):
        load_dotenv()
        self.connection = self.get_connection()
        self.cursor = self.connection.cursor()

    def get_connection(self):
        return psycopg2.connect(
            host = os.getenv('DB_HOST'),
            database = os.getenv('DB_NAME'),
            user = os.getenv('DB_USERNAME'),
            password = os.getenv('DB_PASSWORD')
        )

    def insert(self, title, description, is_done, created_on=datetime.now()):
        self.cursor.execute(
            "INSERT INTO task (title, description, is_done, created_on) VALUES (%s, %s, %s, %s)",
            (title, description, is_done, created_on)
        )
        self.connection.commit()

    def get_by_id(self, task_id):
        self.cursor.execute(
            'SELECT * FROM task WHERE task_id = %s',
            (task_id,)
        )
        return  self.cursor.fetchone()

    def get_all(self):
        self.cursor.execute('SELECT * FROM task')
        return self.cursor.fetchall()


    def get_by_title(self, title):
        self.cursor.execute(
            'SELECT * FROM task WHERE title = %s',
            (title,)
        )
        return  self.cursor.fetchone()


    def delete_by_id(self, task_id):
        self.cursor.execute(
            'DELETE FROM task WHERE task_id = %s',
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

    def update_task(self, task_id, title=None, description=None, is_done=None):
        set_clauses = []
        params = []

        if title is not None:
            set_clauses.append("title = %s")
            params.append(title)
        if description is not None:
            set_clauses.append("description = %s")
            params.append(description)
        if is_done is not None:
            set_clauses.append("is_done = %s")
            params.append(is_done)

        if not set_clauses:
            print("No fields provided for update.")
            return False

        query = f"UPDATE task SET {', '.join(set_clauses)} WHERE task_id = %s"
        params.append(task_id)

        try:
            self.cursor.execute(query, tuple(params))
            self.connection.commit()
            if self.cursor.rowcount > 0:
                print(f"Task with ID {task_id} updated successfully.")
                return True
            else:
                print(f"No task found with ID {task_id} to update.")
                return False
        except psycopg2.Error as e:
            print(f"Error updating task with ID {task_id}: {e}")
            self.connection.rollback()
            raise
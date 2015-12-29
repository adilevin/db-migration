import sqlite3

from model import task_model
from exceptions import TaskIdNotFoundException

class SQLiteDAO(object):
    def __init__(self,config):
        self.conn = sqlite3.connect(config['sqlite_file_path'])
        self.create_table_if_doesnt_exist()
        self.create_index_if_doesnt_exist()

    def create_table_if_doesnt_exist(self):
        c = self.conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS tasks
            (id text, assignee text, description text, done boolean)
        """)

    def create_index_if_doesnt_exist(self):
        c = self.conn.cursor()
        c.execute('CREATE INDEX IF NOT EXISTS assignee_done_index ON tasks (assignee,done)')

    def delete_all_tasks(self):
        c = self.conn.cursor()
        c.execute("DELETE FROM tasks")
        self.conn.commit()

    def get_task_by_id(self,task_id):
        c = self.conn.cursor()
        c.execute('SELECT * FROM tasks WHERE id=?',(task_id,))
        tuple = c.fetchone()
        if tuple==None:
            raise TaskIdNotFoundException(task_id)
        return task_model.Task(tuple[0],tuple[1],tuple[2],tuple[3])

    def get_all_undone_tasks_for_assignee(self,assignee):
        c = self.conn.cursor()
        c.execute('SELECT * FROM tasks WHERE assignee="%s" AND done=0' % assignee)
        tuples = c.fetchall()
        return [task_model.Task(tuple[0],tuple[1],tuple[2],tuple[3]) for tuple in tuples]

    # Returns the inserted task_id
    def add_task(self,task):
        c = self.conn.cursor()
        c.execute('INSERT INTO tasks VALUES (?,?,?,?)',(task.id, task.assignee, task.description, task.done))
        self.conn.commit()
        return task.id

    def mark_task_as_done(self,task_id):
        c = self.conn.cursor()
        c.execute('UPDATE tasks SET done=1 WHERE id=?',(task_id,))
        self.conn.commit()
        return self.get_task_by_id(task_id)

if __name__ == '__main__':
    s = SQLiteDAO('c:/temp/s.db')
    s.create_table_if_doesnt_exist()
    s.add_task(task_model.Task('xsdf98ksljhfsf','adi','get up',True))
    print s.get_task_by_id('xsdf98ksljhfsf')
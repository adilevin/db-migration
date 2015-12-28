import sqlite3

from model import task_model


class SQLiteRepo(object):
    def __init__(self,sqlite_file_path):
        print 'Connecting to SQLite db at %s' % sqlite_file_path
        self.conn = sqlite3.connect(sqlite_file_path)
        print '  Creating tasks table if doesnt exist'
        self.create_table_if_doesnt_exist()
        print '  Creating index by (assignee,done)'
        self.create_index_if_doesnt_exist()

    def create_table_if_doesnt_exist(self):
        c = self.conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS tasks
            (id text, assignee text, description text, done boolean)
        """)

    def create_index_if_doesnt_exist(self):
        c = self.conn.cursor()
        c.execute("CREATE INDEX IF NOT EXISTS assignee_done_index ON tasks (assignee,done)")

    def delete_all_tasks(self):
        c = self.conn.cursor()
        c.execute("DELETE FROM tasks")
        self.conn.commit()

    def get_task_by_id(self,task_id):
        c = self.conn.cursor()
        c.execute("SELECT * FROM tasks WHERE id=?",(task_id,))
        tuple = c.fetchone()
        return task_model.Task(tuple[0],tuple[1],tuple[2],tuple[3])

    def get_tasks_by_filter(self,filter_dict):
        c = self.conn.cursor()
        query = "SELECT * FROM tasks WHERE 1"
        if 'assignee' in filter_dict.keys():
            query += ' AND assignee="%s"' % filter_dict['assignee']
        if 'done' in filter_dict.keys():
            query += ' AND done=%i' % filter_dict['done']
        print query
        c.execute(query)
        tuples = c.fetchall()
        return [task_model.Task(tuple[0],tuple[1],tuple[2],tuple[3]) for tuple in tuples]

    # Returns the inserted task_id
    def add_task(self,task):
        c = self.conn.cursor()
        c.execute("""
           INSERT INTO tasks VALUES (?,?,?,?)
        """,(task.id, task.assignee, task.description, task.done))
        self.conn.commit()
        return task.id

    def mark_task_as_done(self,task_id):
        c = self.conn.cursor()
        c.execute("UPDATE tasks SET done=1 WHERE id=?",(task_id,))
        self.conn.commit()
        return self.get_task_by_id(task_id)

if __name__ == '__main__':
    s = SQLiteRepo('c:/temp/s.db')
    s.create_table_if_doesnt_exist()
    s.add_task(task_model.Task('xsdf98ksljhfsf','adi','get up',True))
    print s.get_task_by_id('xsdf98ksljhfsf')
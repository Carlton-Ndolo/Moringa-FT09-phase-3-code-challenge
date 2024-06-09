from database.connection import get_db_connection
from database.setup import create_tables

conn = get_db_connection()
cursor = conn.cursor()

class Author:
    def __init__(self, id, name):
        self.id = id  
        self._name = None  
        self.name = name 
        self._ensure_in_db()  

    def __repr__(self):
        return f'<Author {self.name}>'

    def _ensure_in_db(self):
        cursor.execute("SELECT id, name FROM authors WHERE id = ?", (self._id,))
        existing_author = cursor.fetchone()
        if existing_author:
            if existing_author[1] != self._name:
                raise ValueError(f"Author with id {self._id} already exists with a different name")
        else:
            self._save_to_db()

    def _save_to_db(self):
        sql = """
         INSERT INTO authors (id, name)
         VALUES (?, ?)
        """
        cursor.execute(sql, (self._id, self._name))
        conn.commit()

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        if not isinstance(id, int):
            raise TypeError("id must be an integer")
        self._id = id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        if len(name) == 0:
            raise ValueError("name must be longer than 0 characters")
        if self._name is not None:
            raise AttributeError("Cannot change the name after it is set")
        self._name = name

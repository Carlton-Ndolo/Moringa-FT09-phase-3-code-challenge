from database.connection import get_db_connection
from database.setup import create_tables

conn = get_db_connection()
cursor = conn.cursor()

class Article:
    def __init__(self, id, title, content, author_id, magazine_id):
        self.id = id
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id
        self._title = None 
        self.title = title  
        self._save_to_db()

    def __repr__(self):
        return f'<Article {self.title}>'

    def _save_to_db(self):
        cursor.execute("SELECT id FROM articles WHERE id = ?", (self.id,))
        if cursor.fetchone():
            cursor.execute("""
                UPDATE articles 
                SET title = ?, content = ?, author_id = ?, magazine_id = ?
                WHERE id = ?
            """, (self._title, self.content, self.author_id, self.magazine_id, self.id))
        else:
            sql = """
                INSERT INTO articles (id, title, content, author_id, magazine_id)
                VALUES (?, ?, ?, ?, ?)
            """
            cursor.execute(sql, (self.id, self._title, self.content, self.author_id, self.magazine_id))
        conn.commit()

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        if not isinstance(title, str):
            raise TypeError("title must be a string")
        if not (5 <= len(title) <= 50):
            raise ValueError("title must be between 5 and 50 characters")
        if self._title is not None:
            raise AttributeError("Cannot change the title after it is set")
        self._title = title

    def author_name(self):
        query = """
            SELECT authors.name
            FROM articles
            LEFT JOIN authors
            ON articles.author_id = authors.id
            WHERE articles.id = ?
        """
        cursor.execute(query, (self.id,))
        author = cursor.fetchone()
        return author[0] if author else None
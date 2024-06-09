from database.connection import get_db_connection

conn = get_db_connection()
cursor = conn.cursor()

class Magazine:
    def __init__(self, name, category=None):
        self.name = str(name)  
        self.category = category  
        self._id = None  
        self._save_to_db()

    def __repr__(self):
        return f'<Magazine {self.name}>'

    def _save_to_db(self):
        cursor.execute("SELECT id FROM magazines WHERE id = ?", (self._id,))
        if cursor.fetchone():
            raise ValueError(f"Magazine with id {self._id} already exists")
        sql = """
             INSERT INTO magazines (name, category)
             VALUES (?, ?)
            """
        cursor.execute(sql, (self.name, self.category))
        conn.commit()
        self._id = cursor.lastrowid 

    def articles(self):
        query = """
              SELECT articles.title
              FROM articles
              LEFT JOIN magazines
              ON articles.magazine_id = magazines.id
              WHERE magazines.id = ?
        """
        cursor.execute(query, (self._id,))
        articles = cursor.fetchall()
        return [article[0] for article in articles] if articles else None

    def contributors(self):
        sql = """
          SELECT authors.name
          FROM authors
          LEFT JOIN articles
          ON authors.id = articles.author_id
          LEFT JOIN magazines
          ON articles.magazine_id = magazines.id
          WHERE magazines.id = ?
        """
        cursor.execute(sql, (self._id,))
        contributors = cursor.fetchall()
        return [contributor[0] for contributor in contributors] if contributors else None

    def article_titles(self):
        sql = """
            SELECT articles.title
            FROM articles
            WHERE articles.magazine_id = ?
        """
        cursor.execute(sql, (self._id,))
        article_titles = cursor.fetchall()
        return [article_title[0] for article_title in article_titles] if article_titles else None

    def contributing_authors(self):
        sql = """
            SELECT authors.name
            FROM authors
            LEFT JOIN articles 
            ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
            GROUP BY authors.id
            HAVING COUNT(articles.id) > 2
        """
        cursor.execute(sql, (self._id,))
        contributing_authors = cursor.fetchall()
        return [contributing_author[0] for contributing_author in contributing_authors] if contributing_authors else None

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if not isinstance(name, str):
            raise TypeError("Name must be a string")
        self._name = name

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if value is not None and (not isinstance(value, str) or len(value) == 0):
            raise ValueError("Category must be a non-empty string or None")
        self._category = value

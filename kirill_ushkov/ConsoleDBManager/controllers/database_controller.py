import sqlite3
from contextlib import closing
from ..models.menu_item import MenuItem
import csv
import os


class DatabaseController:
    def __init__(self):
        self.__db_name = "company.db"
        self.create_db_if_needed()

    def create_db_if_needed(self):
        if self.check_db_exists():
            return

        create_menu_query = """
            CREATE TABLE IF NOT EXISTS menu_item(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                description TEXT,
                syntax TEXT,
                parent_id INTEGER NULLABLE,
                FOREIGN KEY(parent_id) REFERENCES menu_item(id)
            );            
        """
        create_dep_query = """
            CREATE TABLE IF NOT EXISTS department(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT
            );
        """

        conn = self.get_connection()
        queries = [create_menu_query, create_dep_query]
        with closing(conn):
            with conn:
                for query in queries:
                    conn.execute(query)
        self.fill_menu_table()
        self.fill_dep_table()

    def fill_menu_table(self):
        menu_create_query = """
            INSERT INTO menu_item('name', 'description', 'syntax', 'parent_id') VALUES (?, ?, ?, ?);
        """

        this_folder = os.path.dirname(os.path.abspath(__file__))
        initial_menu_file = os.path.join(this_folder, 'initial_menu.csv')

        conn = self.get_connection()
        cursor = conn.cursor()

        with open(initial_menu_file, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                parent_id = row["parent_id"]
                if not parent_id:
                    parent_id = None
                params = (row["name"], row["description"], row["syntax"], parent_id)
                cursor.execute(menu_create_query, params)
                conn.commit()
        conn.close()

    def fill_dep_table(self):
        dep_create_query = """
            INSERT INTO department('name') VALUES (?);
        """
        this_folder = os.path.dirname(os.path.abspath(__file__))
        initial_deps_file = os.path.join(this_folder, 'initial_deps.csv')

        conn = self.get_connection()
        cursor = conn.cursor()

        with open(initial_deps_file, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                params = (row["name"],)
                cursor.execute(dep_create_query, params)
                conn.commit()
        conn.close()

    def check_db_exists(self):
        return os.path.exists(self.__db_name)

    def get_connection(self):
        return sqlite3.connect(self.__db_name)

    def get_initial_menu_items(self):
        query = """
            SELECT * FROM menu_item WHERE parent_id IS NULL;
        """

        cursor = self.get_connection().cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

        menu_items = []

        for row in rows:
            item = MenuItem(identifier=row[0],
                            name=row[1],
                            description=row[2],
                            syntax=row[3],
                            parent_id=row[4])
            menu_items.append(item)
        return menu_items

    def get_selected_menu_item(self, user_input):
        query = """
            SELECT * FROM menu_item WHERE id = ?
        """
        cursor = self.get_connection().cursor()
        cursor.execute(query, user_input)
        row = cursor.fetchone()
        if row is not None:
            item = MenuItem(row[0], row[1], row[2], row[3], row[4])
            return item
        return None

    def get_child_menu_items(self, menu_item_id):
        query = """
            SELECT * FROM menu_item WHERE parent_id = ?
        """
        cursor = self.get_connection().cursor()
        cursor.execute(query, str(menu_item_id))

        children = []

        for row in cursor.fetchall():
            item = MenuItem(row[0], row[1], row[2], row[3], row[4])
            children.append(item)
        return children

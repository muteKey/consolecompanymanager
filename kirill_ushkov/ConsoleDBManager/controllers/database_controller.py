import sqlite3
from contextlib import closing
from ..models.menu_item import MenuItem
from ..models.department import Department
from ..models.employee import Employee
import csv
import os
import logging

logger = logging.getLogger(__name__)


print(logger.name)

class DatabaseController:
    def __init__(self):
        self.__db_name = "company.db"
        self.create_db_if_needed()

    def create_db_if_needed(self):
        if self.check_db_exists():
            logger.info("Database already exists")
            return

        logger.info("Database does not exist")

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
        create_employee_query = """
            CREATE TABLE IF NOT EXISTS employee(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT,
                last_name TEXT,
                position TEXT,
                department_id INTEGER,
                FOREIGN KEY(department_id) REFERENCES department(id)
            );
        """

        conn = self.get_connection()
        queries = [create_menu_query, create_dep_query, create_employee_query]
        try:
            with closing(conn):
                with conn:
                    for query in queries:
                        conn.execute(query)
        except sqlite3.Error:
            logger.exception("Problem with creating database tables")

        self.fill_menu_table()
        self.fill_dep_table()
        self.fill_employee_table()

    def fill_menu_table(self):
        menu_create_query = """
            INSERT INTO menu_item('name', 'description', 'syntax', 'parent_id') VALUES (?, ?, ?, ?);
        """

        this_folder = os.path.dirname(os.path.abspath(__file__))
        initial_menu_file = os.path.join(this_folder, 'initial_menu.csv')

        conn = self.get_connection()
        cursor = conn.cursor()

        try:
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
        except sqlite3.Error:
            logger.exception("Filling menu table problem")
        except csv.Error:
            logger.exception("Menu csv file reading problem")
        finally:
            conn.close()

    def fill_employee_table(self):
        employee_fill_query = """
            INSERT INTO employee('first_name','last_name','position','department_id') VALUES (?,?,?,?) 
        """
        this_folder = os.path.dirname(os.path.abspath(__file__))
        initial_menu_file = os.path.join(this_folder, 'initial_employees.csv')

        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            with open(initial_menu_file, 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    params = (row["first_name"], row["last_name"], row["position"], row["department_id"])
                    cursor.execute(employee_fill_query, params)
                    conn.commit()
            conn.close()
        except sqlite3.Error:
            logger.exception("Filling employee table problem")
        except csv.Error:
            logger.exception("Employee csv file reading problem")
        finally:
            conn.close()

    def fill_dep_table(self):
        dep_create_query = """
            INSERT INTO department('name') VALUES (?);
        """
        this_folder = os.path.dirname(os.path.abspath(__file__))
        initial_deps_file = os.path.join(this_folder, 'initial_deps.csv')

        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            with open(initial_deps_file, 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    params = (row["name"],)
                    cursor.execute(dep_create_query, params)
                    conn.commit()
            conn.close()
        except sqlite3.Error:
            logger.exception("Filling departments table problem")
        except csv.Error:
            logger.exception("Departments csv file reading problem")
        finally:
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

    def get_selected_menu_item(self, command_name):
        query = """
            SELECT * FROM menu_item WHERE name = ?;
        """
        cursor = self.get_connection().cursor()
        cursor.execute(query, (command_name,))
        row = cursor.fetchone()
        if row is not None:
            item = MenuItem(row[0], row[1], row[2], row[3], row[4])
            return item
        logger.info("No menu command found with name {}".format(command_name))
        return None

    def get_child_menu_items(self, menu_item_id):
        query = """
            SELECT * FROM menu_item WHERE parent_id = ?;
        """
        cursor = self.get_connection().cursor()
        cursor.execute(query, (menu_item_id,))

        children = []

        for row in cursor.fetchall():
            item = MenuItem(row[0], row[1], row[2], row[3], row[4])
            children.append(item)
        return children

    def get_all_departments(self):
        query = """
            SELECT * FROM department;
        """
        cursor = self.get_connection().cursor()
        cursor.execute(query)

        children = []

        for row in cursor.fetchall():
            item = Department(row[0], row[1])
            children.append(item)
        return children

    def add_department(self, dep_name):
        query = """
            INSERT INTO department('name') VALUES (?);
        """
        conn = self.get_connection()
        try:
            with closing(conn):
                with conn:
                    conn.execute(query, (dep_name,))
        except sqlite3.Error:
            logger.exception("Insert department problem")
        finally:
            conn.close()

    def get_department_by_name(self, dep_name):
        query = """
            SELECT * FROM department WHERE name LIKE ?;
        """
        conn = self.get_connection()
        with closing(conn):
            with conn:
                cursor = self.get_connection().cursor()
                cursor.execute(query, (dep_name,))
                row = cursor.fetchone()
                if row is None:
                    logger.debug("Department with name {} not found".format(dep_name))
                    return None
                return Department(row[0], row[1])

    def get_employees_for_department(self, dep_id):
        query = """
            SELECT * FROM employee WHERE department_id=?;
        """
        conn = self.get_connection()
        with closing(conn):
            cursor = self.get_connection().cursor()
            cursor.execute(query, (dep_id,))
            employees = []
            for row in cursor.fetchall():
                employee = Employee(row[0], row[1], row[2], row[3], row[4])
                employees.append(employee)
            return employees

    def add_employee(self, first_name, last_name, position, department_id):
        query = """
            INSERT INTO employee('first_name','last_name','position','department_id') VALUES (?,?,?,?);
        """

        conn = self.get_connection()
        try:
            with closing(conn):
                with conn:
                    cursor = conn.cursor()
                    cursor.execute(query, (first_name, last_name, position, department_id))
        except sqlite3.Error:
            logger.exception("Insert employee problem")
        finally:
            conn.close()

    def remove_employee(self, emp_id, department_id):
        query = """
            DELETE FROM employee WHERE id = ? AND department_id = ?;
        """
        conn = self.get_connection()
        try:
            with closing(conn):
                with conn:
                    cursor = conn.cursor()
                    cursor.execute(query, (emp_id, department_id))
        except sqlite3.Error:
            logger.exception("Delete employee problem")
        finally:
            conn.close()

    def edit_employee(self, emp_id, first_name, last_name, position):
        query = """
            UPDATE employee SET first_name = ?, last_name = ?, position = ?
            WHERE id = ?;
        """
        conn = self.get_connection()
        try:
            with closing(conn):
                with conn:
                    cursor = conn.cursor()
                    cursor.execute(query, (first_name, last_name, position, emp_id))
        except sqlite3.Error:
            logger.exception("Update employee problem")
        finally:
            conn.close()

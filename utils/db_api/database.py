import sqlite3
from datetime import datetime


class Database:
    def __init__(self, path_to_db="data/main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: list = None,
                fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = []
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()

        return data

    # USER таблицы
    def create_table_users(self):
        sql = """
        CREATE TABLE if not exists users (
            id int NOT NULL,
            first_name varchar(255)  ,
            last_name varchar(255)  ,
            phone_number varchar(255)   ,
            name_Line varchar (255),
            is_registered varchar (255),
            PRIMARY KEY (id)
            );
"""
        self.execute(sql, commit=True)

    def select_all_tg_id(self):
        sql = """
            SELECT  id FROM users
        """
        return self.execute(sql, fetchall=True)

    def add_user(self, first_name: str, last_name: str, phone_numbber: str, name_line: str, isregistered: str,
                 id: int):
        sql = """
                   UPDATE users SET first_name =?,last_name=?,phone_number=?,name_Line = ?,is_registered=? WHERE id=?

        """
        self.execute(sql, parameters=(first_name, last_name, phone_numbber, name_line, isregistered, id), commit=True)

    def get_users_admin(self):
        sql = """
        SELECT * FROM users 
        """
        return self.execute(sql, fetchall=True, commit=True)

    def select_users(self, name_line: str):
        sql = """
            SELECT last_name,id 
            FROM users 
            WHERE name_Line = ?
        """
        return self.execute(sql, parameters=(name_line,), fetchall=True, commit=True)

    def select_user(self, user_id: int):
        sql = """
            SELECT last_name
            FROM users 
            WHERE id = ?
        """
        return self.execute(sql, parameters=(user_id,), fetchone=True, commit=True)

    def select_isregis(self, id: int):
        sql = """
        SELECT is_registered
        FROM users 
        WHERE id = ?
        """
        return self.execute(sql, parameters=(id,), fetchone=True, commit=True)

    def admin_add_users(self, id: int, is_registered: str):
        sql = """
               INSERT INTO users(id,is_registered) VALUES(?,?)
                 """
        self.execute(sql, parameters=(id, is_registered), commit=True)

    # Локации
    def create_table_location(self):
        sql = """
                CREATE TABLE if not exists locations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    home_address_lat float ,
                    home_address_long float ,
                    name_line varchar(255),
                    edu_address_lat float ,
                    edu_address_long float ,
                    edu_name varchar(255),
                    others_name varchar(255),
                    others_address_lat float ,
                    others_address_long float ,
                    user_id int,
                    is_registed varchar(255),
                    FOREIGN KEY (user_id) REFERENCES users(id)
                    );
        """
        self.execute(sql, commit=True)

    def add_users_loc(self, user_id: int, is_registered: str):
        sql = """
               INSERT INTO locations(user_id,is_registed)
               VALUES(?,?)
                 """
        self.execute(sql, parameters=(user_id, is_registered), commit=True)

    def all_tg_id(self):
        sql = """
            SELECT  user_id 
            FROM locations
        """
        return self.execute(sql, fetchall=True)

    def add_location_home(self, home_address_lat: float, home_address_long: float, name_line: str, is_registed: str,
                          user_id: int):
        sql = """
         UPDATE locations 
         SET home_address_lat =?,home_address_long=?,name_line=?,is_registed = ?  
         WHERE  user_id=?
        """
        self.execute(sql,
                     parameters=(home_address_lat, home_address_long, name_line, is_registed, user_id),
                     commit=True)

    def select_isregis_location(self, user_id: int):
        sql = """
        SELECT is_registed 
        FROM locations 
        WHERE user_id = ?
        """
        return self.execute(sql, parameters=(user_id,), fetchone=True)

    def add_location_edu(self, edu_address_lat: float, edu_address_long, edu_name: str, user_id: int):
        sql = """
        UPDATE locations 
        SET edu_address_lat=?,edu_address_long=?, edu_name=? 
        WHERE user_id=? 
        """
        self.execute(sql, parameters=(edu_address_lat, edu_address_long, edu_name, user_id), fetchone=True, commit=True)

    def other_location(self, other_address_lat: float, other_address_long: float, others_name: str, user_id: int):
        sql = """
        UPDATE locations 
        SET others_address_lat=?,others_address_long=?,others_name = ? 
        WHERE user_id=?
        """
        self.execute(sql, parameters=(other_address_lat, other_address_long, others_name, user_id), fetchone=True,
                     commit=True)

    def get_locations_home(self, user_id: int):
        sql = """
        SELECT  home_address_lat,home_address_long 
        FROM locations 
        WHERE  user_id = ? 
        """
        return self.execute(sql, parameters=(user_id,), fetchall=True)

    def get_other_location(self, user_id: int):
        sql = """
        SELECT others_address_lat,others_address_long
        FROM locations
        WHERE user_id =?
        """
        return self.execute(sql, parameters=(user_id,), fetchall=True)

    def get_edu_location(self, user_id: int):
        sql = """
        SELECT edu_address_lat,edu_address_long
        FROM locations
        WHERE user_id =?
        """
        return self.execute(sql, parameters=(user_id,), fetchall=True)

    def select_other(self):
        sql = """
           SELECT others_name,user_id 
           FROM locations 
           WHERE others_address_lat IS NOT NULL  
           """
        return self.execute(sql, fetchall=True, commit=True)

    def select_edu(self):
        sql = """
           SELECT edu_name,user_id 
           FROM locations 
           WHERE edu_address_lat IS NOT NULL  
           """
        return self.execute(sql, fetchall=True, commit=True)

    # Drivers table
    def create_table_drivers(self):
        sql = """
            CREATE TABLE if not exists drivers (
                id int NOT NULL,
                FIO varchar(255)  ,
                ser_num_passport varchar(255)  ,
                phone_number varchar(255)   ,
                is_registered varchar(255),
                home_address_lat float ,
                home_address_long float ,
                PRIMARY KEY (id)
                );
    """
        self.execute(sql, commit=True)

    def admin_add_drivers(self, id: int, is_registered: str):
        sql = """
                INSERT INTO drivers(id,is_registered) 
                VALUES(?,?)
                 """
        self.execute(sql, parameters=(id, is_registered), commit=True)

    def add_drivers(self, FIO: str, ser_num_passport: str, is_registered: str, phone_number: str,
                    home_address_lat: float, home_address_long: float, id: int):
        sql = """
        UPDATE drivers 
        SET FIO=?,ser_num_passport=?,is_registered=? ,phone_number = ?,
        home_address_lat=?,home_address_long=?  
        WHERE id =?
        """
        self.execute(sql, parameters=(FIO, ser_num_passport, is_registered, phone_number,
                                      home_address_lat, home_address_long, id), commit=True)

    def get_home_driver(self, id: int):
        sql = """
        SELECT  home_address_lat,home_address_long 
        FROM drivers 
        WHERE  id = ? 
        """
        return self.execute(sql, parameters=(id,), fetchall=True)

    def get_drivers_admin(self):
        sql = """
        SELECT * FROM drivers 
        """
        return self.execute(sql, fetchall=True, commit=True)

    ####################################################################################
    def select_isregis_drivers(self, id: int):
        sql = """
        SELECT is_registered 
        FROM drivers 
        WHERE id =?
        """
        return self.execute(sql, parameters=(id,), fetchall=True, commit=True)

    #####################################################################################################
    def select_all_drivers_id(self):
        sql = """
            SELECT  id FROM drivers
        """
        return self.execute(sql, fetchall=True)

    # Расходы
    def create_table_road_consumption(self):
        sql = """
        CREATE TABLE if not exists roads (
                id  INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id int  ,
                date_day DATETIME,
                count_day float ,
                oil_view varchar(255),
                view_road varchar (255),
                oil_day float ,
                FOREIGN KEY (user_id) REFERENCES drivers(id)
                );
        """
        self.execute(sql, commit=True)

    def insert_day(self, date_day: datetime, count_day: float, oil_day: float, oil_view: str, view_road: str,
                   user_id: int):
        sql = """
         INSERT INTO roads(date_day,count_day,oil_day,oil_view,view_road,user_id)
         VALUES(?,?,?,?,?,?)
        """
        self.execute(sql, parameters=(date_day, count_day, oil_day, oil_view, view_road, user_id), commit=True)

    def select_day(self):
        sql = """
        SELECT * FROM roads
        """
        return self.execute(sql, fetchall=True)

    # ADMIN
    def create_table_admins(self):
        sql = """
            CREATE TABLE if not exists admins (
                id int NOT NULL,
                PRIMARY KEY (id)
                );
    """
        self.execute(sql, commit=True)

    def admin_add_Admin(self, id: int):
        sql = """
                INSERT INTO admins(id) VALUES(?)
                 """
        self.execute(sql, parameters=(id,), commit=True)

    def select_all_admins_id(self):
        sql = """
            SELECT  id FROM admins
        """
        return self.execute(sql, fetchall=True)

    # CARS
    def create_table_cars(self):
        sql = """
            CREATE TABLE if not exists cars (
                id int NOT NULL,
                ser_num_prava varchar(255)  ,
                mark_avto varchar(255)  ,
                ser_num_tex varchar(255)   ,
                num_car varchar (255),
                is_registered varchar(255),
                km_consumption float,
                oil_view varchar(255),
                PRIMARY KEY (id)
                );
    """
        self.execute(sql, commit=True)

    def add_cars_petrol(self, ser_num_prava: str, mark_avto: str, ser_num_tex: str, num_car: str,
                        is_registered: str, km_consumption: float, oil_view: str, id: int):
        sql = """
        UPDATE cars 
        SET ser_num_prava=?,mark_avto=?,ser_num_tex=?,num_car=?,is_registered=?,
        km_consumption=?,oil_view =?
        WHERE id=?
        """
        self.execute(sql, parameters=(
            ser_num_prava, mark_avto, ser_num_tex, num_car, is_registered, km_consumption, oil_view, id),
                     commit=True)

    def add_cars_gas(self, ser_num_prava: str, mark_avto: str, ser_num_tex: str, num_car: str,
                     is_registered: str, km_consumption: float, oil_view: str,
                     id: int):
        sql = """
        UPDATE cars 
        SET ser_num_prava=?,mark_avto=?,ser_num_tex=?,num_car=?,is_registered=?,
        km_consumption=?,oil_view=?
        WHERE id=?
        """
        self.execute(sql, parameters=(
            ser_num_prava, mark_avto, ser_num_tex, num_car, is_registered, km_consumption, oil_view, id),
                     commit=True)

    def select_oil_view(self, user_id: int):
        sql = """
               SELECT oil_view 
               FROM cars 
               WHERE id = ?
               """
        return self.execute(sql, parameters=(user_id,), fetchone=True)

    def select_km_consumption(self, user_id: int):
        sql = """
               SELECT km_consumption 
               FROM cars 
               WHERE id = ?
               """
        return self.execute(sql, parameters=(user_id,), fetchone=True)

    def select_all_cars_id(self):
        sql = """
            SELECT  id FROM cars
        """
        return self.execute(sql, fetchall=True)

    def select_isregis_cars(self, id: int):
        sql = """
        SELECT is_registered 
        FROM cars
        WHERE id=? 
        """
        return self.execute(sql, parameters=(id,), fetchone=True, commit=True)

    def admin_add_cars(self, id: int, is_registered: str):
        sql = """
                INSERT INTO cars(id,is_registered) VALUES(?,?)
                 """
        self.execute(sql, parameters=(id, is_registered), commit=True)

    def get_cars_petrol_admin(self, oil_view: str):
        sql = """
        SELECT ser_num_prava,mark_avto,num_car,ser_num_tex,km_consumption, id
        FROM cars
        WHERE oil_view=?
        """
        return self.execute(sql, parameters=(oil_view,), fetchall=True, commit=True)

    def get_cars_gas_admin(self, oil_view: str):
        sql = """
        SELECT ser_num_prava,mark_avto,ser_num_tex,num_car,is_registered,
        km_consumption, id
        FROM cars
        WHERE oil_view=?
        """
        return self.execute(sql, parameters=(oil_view,), fetchall=True, commit=True)

    # TEX.PROBLEM
    def create_table_tex(self):
        sql = """
            CREATE TABLE if not exists tex_problem (
            id  INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id int  ,
            tex_problem varchar(255),
            description varchar (255),
            fuel varchar(255),
            fuel_name varchar(255),
            FOREIGN KEY (user_id) REFERENCES drivers(id)
            );
            """
        self.execute(sql, commit=True)

    def add_problem(self, user_id: int, tex_problem: str, description: str):
        sql = """
            INSERT INTO tex_problem(user_id,tex_problem,description) VALUES (?,?,?)
        """
        self.execute(sql, parameters=(user_id, tex_problem, description), commit=True)

    def add_Feul(self, user_id: int, fuel: str, fuel_name: str):
        sql = """
        INSERT INTO tex_problem(user_id,fuel,fuel_name) VALUES (?,?,?)
        """
        self.execute(sql, parameters=(user_id, fuel, fuel_name), commit=True)

    def select_fuel(self):
        sql = """
        SELECT user_id,fuel ,fuel_name
        FROM tex_problem
        WHERE fuel_name IS NOT NULL 
        """
        return self.execute(sql, fetchall=True)

    def select_problem(self):
        sql = """
        SELECT user_id,tex_problem,description 
        FROM tex_problem 
        WHERE tex_problem IS NOT NULL 
        """
        return self.execute(sql, fetchall=True, commit=True)


def logger(statement):
    print(f"""
    ______________________________________________________
    Executing:
    {statement}
    ______________________________________________________
    """)

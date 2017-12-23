import sqlite3
import arrow
import uuid

DB_FILE = "maps.db"
sql_create_map_history_table = """ CREATE TABLE IF NOT EXISTS maps_history (
                                        src text NOT NULL,
                                        dest text NOT NULL,
                                        sdate text NOT NULL,
                                        map_link text NOT NULL
                                    ); """       
sql_set_map = 'insert into maps_history values (?, ?, ?, ?)'
                
sql_get_map = 'select map_link from maps_history where src = ? and dest = ? and sdate = ?'


class search_maps:

    def __init__(self, conn):
        self.db_conn = conn

    def _set_map(self, src, dest, date, map_link):
        cur=self.db_conn.cursor()
        cur.execute(sql_set_map, (src, dest, date, map_link))
        self.db_conn.commit()
        cur.close()

    def _get_image(self, src, dest):
        ''' GEt image with src and destination from google map'''
        return my_random_string(6)
    
    def create_table_if_not_exist(self):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return
        """
        try:
            c = self.db_conn.cursor()
            c.execute(sql_create_map_history_table)
            self.db_conn.commit()
        except Error as e:
            print(e)


    def get_map(self, src, dest, date):
        try:
            cur = self.db_conn.cursor()
            cur.execute(sql_get_map, (src, dest, date))
            rows = cur.fetchall()
            for row in rows:
                print('map links are {}'.format(row))
            cur.close()
        except Error as e:
            print(e)
        finally:
            self.db_conn.commit()


    def set_maps_for_today(self, locations):
        date = arrow.utcnow().to('Asia/Kolkata').format('YYYY-MM-DD-HH')
        for src in locations:
            for dest in locations:
                if src == dest:
                    continue
                map_link = _get_image(src, dest)
                print('Inserting {}, {}, {}, {} '.format(src, dest, date, map_link))
                self._set_map(src, dest, date, map_link)

    

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None

def my_random_string(string_length=10):
    """Returns a random string of length string_length."""
    random = str(uuid.uuid4()) # Convert UUID format to a Python string.
    random = random.upper() # Make all characters uppercase.
    random = random.replace("-","") # Remove the UUID '-'.
    return random[0:string_length] # Return the random string.



locations = ['kormangla', 'btm', 'indiranagar']
conn = create_connection(DB_FILE)
with conn:
    smaps = search_maps(conn)
    smaps.create_table_if_not_exist()
    #smaps.set_maps_for_today(locations)

    date = arrow.utcnow().to('Asia/Kolkata').format('YYYY-MM-DD-HH')
    #smaps.get_map('kormangla', 'indiranagar', date)        

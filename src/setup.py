# This code creates a db where all metrics will be stored.A

import sqlite3
import yaml


def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
        return conn
    except Error as err:
        print(err)
    return None

def create_db(conn, db_file):
    try:
        c = conn.cursor()
        c.execute(db_file)
        print(str(db_file) + ' was succesfuly created.')
    except Error as err:
        print(err)

def main():
    #database = '../db/pywebtoring_store.db'
 
    create_url_table= """ CREATE TABLE IF NOT EXISTS urls (
                                        date text,
                                        url text,
                                        response_time integer,
                                        response_code integer,
                                        ex_http text
                                    ); """
 
    config = yaml.load(open('../config/bd.yml')) 
    database = str(config['DB_PATH']) + str(config['DB_NAME'])
    print('home de la bd: ' + database)
    conn = create_connection(database)
    if conn is not None:
        
        create_db(conn, create_url_table)
        conn.close()
    else:
        print('')
        print('Error! DB cannot be created.')


# here we go!
if __name__ == '__main__':
    main()

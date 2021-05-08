import psycopg2

con = psycopg2.connect(
    host='localhost',
    database='postgres',
    user='postgres',
    password='postgres',
    port=5432
)
cursor = con.cursor()

create_currency_exchanges_table = '''
    CREATE TABLE  IF NOT EXISTS Currency_exchanges(
       ID SERIAL PRIMARY KEY NOT NULL,
       NAME TEXT,
       EXCHANGE_RATE TEXT
    )
'''
cursor.execute(create_currency_exchanges_table)

create_last_request_table = '''
    CREATE TABLE IF NOT EXISTS Last_request(
       ID SERIAL PRIMARY KEY NOT NULL,
        LAST_REQUEST TIMESTAMP
        ) 
'''
cursor.execute(create_last_request_table)


def clear_table():
    cursor.execute('TRUNCATE TABLE currency_exchanges')


def save_currency_exchanges_to_db(currency_id, name, exchange_rate):
    insert_data = f'''
        INSERT INTO currency_exchanges (ID, NAME, EXCHANGE_RATE) VALUES({currency_id}, '{name}', '{exchange_rate}')
    '''
    cursor.execute(insert_data)
    con.commit()


def get_all_currency_exchanges_data():
    command = '''
        SELECT name, exchange_rate FROM currency_exchanges
    '''
    cursor.execute(command)
    return cursor.fetchall()


def get_currency_rate(currency):
    command = f'''
        SELECT exchange_rate FROM currency_exchanges WHERE name='{currency}'
    '''
    cursor.execute(command)
    return cursor.fetchone()


def set_last_request():
    cursor.execute('TRUNCATE TABLE last_request')
    insert_data = f'''
        INSERT INTO last_request (ID, LAST_REQUEST) VALUES(1, current_timestamp)
    '''
    cursor.execute(insert_data)
    con.commit()


def get_last_request():
    last_request_command = '''
            SELECT last_request FROM last_request WHERE id=1
        '''
    cursor.execute(last_request_command)
    return cursor.fetchall()

con.commit()

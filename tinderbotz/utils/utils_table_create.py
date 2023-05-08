from tinderbotz.helpers import db_connection_helper

def main() -> None:
    try:
        connection = db_connection_helper.connect()
        cursor = connection.cursor()
        query: str = "CREATE TABLE tinder_keys (" \
                     "id INTEGER PRIMARY KEY," \
                     "serial_number TEXT NOT NULL," \
                     "is_activated boolean NOT NULL," \
                     "activation_ts BIGINT NOT NULL," \
                     "expiration_ts BIGINT NOT NULL," \
                     "hwid TEXT NOT NULL," \
                     "is_trial boolean NOT NULL)"
        cursor.execute(query)
        connection.commit()
        cursor.close()
        connection.close()
    except BaseException as ex:
        input(ex)
        cursor.close()
        connection.close()

    input("success")

if __name__ == "__main__":
    main()
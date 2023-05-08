from tinderbotz.helpers import db_connection_helper

try:
    from mysql import connector
    import uuid
except BaseException as ex:
    input(ex)

if __name__ == "__main__":
    try:
        connection = db_connection_helper.connect()
        cursor = connection.cursor()
        number: str = input("Keys count: ")
        is_trial: int = int(input("is_trial: int: "))
        input(f"Confirm action? Keys count is {number}")
        for i in range(0, int(number)):
            serial_number = uuid.uuid4()
            is_activated = 0
            activation_ts = -1
            expiration_ts = -1
            query: str = "INSERT INTO tinder_keys (serial_number, is_activated, activation_ts," \
                    f"expiration_ts, hwid, is_trial) VALUES ('{serial_number}', 0, 0, 0, 'null', {is_trial})"
            cursor.execute(query)
        connection.commit()
        cursor.close()
        connection.close()

    except BaseException as ex:
        input(ex)
        cursor.close()
        connection.close()
from typing import Union
from mysql import connector
from mysql.connector.pooling import PooledMySQLConnection
from mysql.connector.plugins import mysql_native_password
from mysql.connector.plugins import caching_sha2_password

_user: str = ""
_password: str = ""
_host: str = ""
_database: str = ""
_port: int = 3306
_auth_plugin: str = "mysql_native_password"

def connect() -> Union[PooledMySQLConnection, connector.MySQLConnection, None]:
    return connector.connect(user=_user, password=_password,
                             host=_host, database=_database,
                             port=_port, auth_plugin=_auth_plugin)

from psycopg.rows import dict_row
from psycopg_pool import AsyncConnectionPool
class PostgresPoolFactory():
    def __init__(self,
            host: str,
            port: int,
            user: str,
            password: str,
            dbname: str,
            min_size: int = 1,
            max_size: int = 10,
    ):
        if not isinstance(host, str) or not host.strip():
            raise ValueError("Invalid host value. It must be a non-empty string.")
        if isinstance(port, bool) or not isinstance(port, int):
            raise ValueError("Invalid port value. It must be a positive integer.")
        if port <= 0 or port > 65535:
            raise ValueError("Invalid port value. It must be a positive integer between 1 and 65535.")
        if not isinstance(user, str) or not user.strip():
            raise ValueError("Invalid user value. It must be a non-empty string.")
        if not isinstance(password, str) or not password.strip():
            raise ValueError("Invalid password value. It must be a non-empty string.")
        if not isinstance(dbname, str) or not dbname.strip():
            raise ValueError("Invalid dbname value. It must be a non-empty string.")
        if isinstance(min_size, bool) or not isinstance(min_size, int):
            raise ValueError("min_size must be an integer.")

        if isinstance(max_size, bool) or not isinstance(max_size, int):
            raise ValueError("max_size must be an integer.")

        if not 1 <= min_size <= max_size <= 10:
            raise ValueError(
                "Pool size must satisfy 1 <= min_size <= max_size <= 10."
            )
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.dbname = dbname
        self.min_size = min_size
        self.max_size = max_size
    def create_pool(self) -> AsyncConnectionPool:
        conninfo = (
            f"host={self.host} "
            f"port={self.port} "
            f"user={self.user} "
            f"password={self.password} "
            f"dbname={self.dbname}"
        )
        return AsyncConnectionPool(
            conninfo=conninfo,
            min_size=self.min_size,
            max_size=self.max_size,
            kwargs={"row_factory": dict_row},
            open = False
        )
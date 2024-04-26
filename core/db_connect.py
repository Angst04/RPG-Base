import psycopg2
import redis
from core.config import DB_HOST as host, DB_USER as user, DB_PASSWORD as password, DB_NAME as db_name
from core.config import REDIS_HOST as r_host, REDIS_PORT as r_port, REDIS_DB as r_db

cache = redis.Redis(
   host=r_host, 
   port=r_port, 
   db=r_db
)

conn_cfg = psycopg2.connect(
   host=host,
   user=user,
   password=password,
   database=db_name
)
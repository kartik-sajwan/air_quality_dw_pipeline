import psycopg2
from psycopg2 import OperationalError, DatabaseError
from dotenv import load_dotenv
import os
import argparse
from loguru import logger

load_dotenv()

db_name = os.getenv("POSTGRES_DB")
db_host = os.getenv("POSTGRES_HOST")
db_port = os.getenv("POSTGRES_PORT")
db_user = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")


class DatabaseHelper:
  def __init__(self, dbname, user, password, host, port=5432):
    self.host = host
    self.dbname = dbname
    self.user = user
    self.password = password
    self.port = port

  def connect(self):
    self.conn = psycopg2.connect(
        dbname=self.dbname,
        user=self.user,
        password=self.password,
        host=self.host,
        port=self.port
    )
    return self.conn

  def close(self):
    if self.conn:
      self.conn.close()

  def execute_sql(self, query):
    try:
      with self.connect() as conn:
        with conn.cursor() as cur:
          cur.execute(query)
          conn.commit()
    except OperationalError as err:
      logger.info(f'Connection unsuccessful: {err}')
    except DatabaseError as err:
      logger.info(f'Database error occured: {err}')
      conn.rollback()
    except Exception as err:
      logger.info(f'Unexpected error occured: {err}')


def main(args):

  sql_file_path = f"sql/{args.mode}_tables.sql"
  with open(sql_file_path, 'r') as f:
    sql_query = f.read()

  db_helper = DatabaseHelper(db_name, db_user, db_password, db_host, db_port)
  db_helper.execute_sql(sql_query)


if __name__ == "__main__":
  parser = argparse.ArgumentParser(
      description="Air Quality Data Warehouse ETL Runner")
  parser.add_argument("--mode", required=True,
                      choices=["create", "update", "delete"], help="SQL to execute")
  args = parser.parse_args()
  main(args)

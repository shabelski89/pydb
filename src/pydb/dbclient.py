import os
import sys
import cmd
import time
import argparse
from urllib.parse import urlparse
from prettytable import from_db_cursor, PrettyTable
try:
    from dbms import UniDbConnector
except ModuleNotFoundError:
    from .dbms import UniDbConnector


class SqlClient(cmd.Cmd):
    def __init__(self, db: UniDbConnector):
        super().__init__()
        self.prompt = 'SQL> '
        self.delimiter = '=' * 40
        self.db = db

    def default(self, line: str) -> None:
        self.do_execute(query=line)

    def do_execute(self, query: str) -> None:
        time_begin_execute = time.time()
        cursor = self.execute(query=query)
        if cursor:
            table: PrettyTable = from_db_cursor(cursor)
            table.align = "l"
            time_of_execute = time.time() - time_begin_execute
            print(table)
            print(f'Rows: {cursor.rowcount}')
            print(f'Time: {time_of_execute:.2f}')

    def help_execute(self):
        print(f'{self.delimiter}\nType: SELECT * FROM table;')

    def execute(self, query: str):
        """
        Method to fetchall data
        :param query: sql query to execute
        :return: List[tuple] of query results
        """

        try:
            cursor = self.db.execute(query=query)
            return cursor
        except Exception as Error:
            print(f'{self.delimiter}\nError: {Error}')

    def do_exit(self, line):
        print(line)
        print(f'{self.delimiter}\nGoodbye!')
        return True

    def help_exit(self):
        print(f'{self.delimiter}\nInput exit or Ctrl+C to quit')


def main():
    program_name = os.path.basename(sys.argv[0])
    help_msg = f'{program_name} -c "postgres://user:password@hostname:port/database"'
    arg_parser = argparse.ArgumentParser(description=program_name, formatter_class=argparse.RawTextHelpFormatter)
    arg_parser.add_argument("-c", dest="connection", required=True, type=str, help=help_msg)
    args = arg_parser.parse_args()

    connection_parse_args = urlparse(args.connection)
    cfg = dict(
        host=connection_parse_args.hostname,
        port=connection_parse_args.port,
        user=connection_parse_args.username,
        password=connection_parse_args.password,
        database=connection_parse_args.path.lstrip("/"),
        dbms=connection_parse_args.scheme
    )

    db = UniDbConnector(config=cfg)
    client = SqlClient(db=db)

    try:
        client.cmdloop()
    except KeyboardInterrupt:
        print('Goodbye!')


if __name__ == '__main__':
    main()

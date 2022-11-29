import os
import sys
import cmd
import argparse
from urllib.parse import urlparse
from prettytable import from_db_cursor, PrettyTable
from dbms import UniDbConnector


class SqlClient(cmd.Cmd):
    def __init__(self, db: UniDbConnector):
        super().__init__()
        self.prompt = 'SQL> '
        self.delimiter = '=' * 40
        self.db = db

    def default(self, line: str) -> None:
        self.do_execute(query=line)

    def do_execute(self, query: str, limit: int = 50) -> None:
        table = self.execute(query=query, limit=limit)
        print(table)

    def help_execute(self):
        print(f'{self.delimiter}\nType: "execute SELECT * FROM table;"')

    def execute(self, query: str, limit: int) -> PrettyTable:
        """
        Method to fetchall data
        :param query: sql query to execute
        :param limit: limit in where clause
        :return: List[tuple] of query results
        """
        limit_flag = False
        limits_words = ['limit', 'fetch first', 'rownum <=']
        for word in limits_words:
            if word in query.lower():
                limit_flag = True
                break

        if not limit_flag:
            if self.db == 'oracle':
                limit_clause = f' fetch first {limit} rows only'
            else:
                limit_clause = f' limit {limit}'
            query += limit_clause

        try:
            cursor = self.db.execute(query=query)
            table = from_db_cursor(cursor)
            table.align = "l"
            return table
        except Exception as Error:
            print(f'{self.delimiter}\nError: {Error}')

    def do_exit(self, line):
        print(line)
        print(f'{self.delimiter}\nGoodbye!')
        return True

    def help_exit(self):
        print(f'{self.delimiter}\nInput exit or Ctrl+C to quit')


if __name__ == '__main__':
    desc_msg = os.path.basename(sys.argv[0])
    help_msg = f'{desc_msg} -c "postgres://user:password@hostname:port/database"'
    arg_parser = argparse.ArgumentParser(description=desc_msg, formatter_class=argparse.RawTextHelpFormatter)
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

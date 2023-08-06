"""Flink SQL Magic Wrapper

Simplifies Flink SQL Client Usage in Jupyter Notebooks

This code can be put in any Python module, it does not require IPython
itself to be running already.  It only creates the magics subclass but
doesn't instantiate it yet.
"""

import logging
import time
import IPython
import pandas as pd
from flink_sql_gateway_client.flink_sql_client import FlinkSQLClient
from IPython.core.magic import Magics, magics_class, line_magic, cell_magic
from IPython.core import magic_arguments


@magics_class
class FlinkSQLMagic(Magics):
    """Flink SQL Magic

    This wrapper class uses ipython magics to simplify usage of
    the flink sql gateway in jupyter notebooks

    """

    def __init__(self, shell):
        """Constructs a flink sql magic wrapper around the flink sql client

        Args:
            shell (object): IPython Shell
        """
        super(FlinkSQLMagic, self).__init__(shell)
        self.flink_sql_client = None

    @magic_arguments.magic_arguments()
    @magic_arguments.argument(
        "--host",
        type=str,
        default="0.0.0.0",
        help=("host name or ip of flink sql gateway"),
    )
    @magic_arguments.argument(
        "--port",
        type=int,
        default=8083,
        help=("port of flink sql gateway"),
    )
    @magic_arguments.argument(
        "--session_name",
        type=str,
        default="my_session",
        help=("human readable name to name your session"),
    )
    @line_magic
    def connect_flink_sql(self, line):
        """Connects to a flink sql gateway

        Args:
            line (string): Arguments in the jupyter notebook % line
        """
        args = magic_arguments.parse_argstring(FlinkSQLMagic.connect_flink_sql, line)
        self.flink_sql_client = FlinkSQLClient(args.host, args.port, args.session_name)

    @magic_arguments.magic_arguments()
    @magic_arguments.argument(
        "destination_var",
        nargs="?",
        help=(
            "if provided, save the output to this variable instead of displaying it."
        ),
    )
    @magic_arguments.argument(
        "--catalog",
        type=str,
        default="pulsar",
        help=("catalog to run flink sql query"),
    )
    @magic_arguments.argument(
        "--execution_timeout",
        type=int,
        default=1000000,
        help=("amount of time to wait for the sql query to start up"),
    )
    @magic_arguments.argument(
        "--num_fetches",
        type=int,
        default=10,
        help=("the number of times to fetch data from the flink sql gateway"),
    )
    @magic_arguments.argument(
        "--max_fetch_size",
        type=int,
        default=1,
        help=("number of records to fetch"),
    )
    @cell_magic
    def flink_sql(self, line, cell):
        """Runs flink sql query

        Args:
            line (string): Arguments in the jupyter notebook % line
            cell (string): Arguments in the jupyter notebook %% cell
        """
        args = magic_arguments.parse_argstring(FlinkSQLMagic.flink_sql, line)
        cell = cell.replace("\n", " ")
        cell = cell.rstrip(";")

        self.flink_sql_client.execute_statement(f"USE CATALOG {args.catalog}")
        job = self.flink_sql_client.execute_statement(cell, args.execution_timeout)
        columns = None
        data = []

        if job.is_one_time():
            columns = job.fetch_job_results(args.max_fetch_size)["results"][0]["columns"]
            data = job.fetch_job_results(args.max_fetch_size)["results"][0]["data"]
        else:
            num_data_fetched = 0
            waiting_for_data = True
            while num_data_fetched < args.num_fetches:
                job_results = job.fetch_job_results(args.max_fetch_size)["results"][0]
                job_data = job_results["data"]
                if job_data != []:
                    waiting_for_data = False
                    columns = job_results["columns"]
                    for row in job_data:
                        data.append(row)

                if not waiting_for_data:
                    # This may not be needed, but seems safer to wait a small amount
                    # of time for flink sql to get results from flink.
                    time.sleep(0.05)
                    num_data_fetched += 1
                else:
                    # It can take a little bit for the flink job to start up
                    # so we need to wait for the first record to be available.
                    time.sleep(1)
                    logging.info("sleeping, waiting for data")

        column_names = [column["name"] for column in columns]
        pd_data = pd.DataFrame.from_dict(data)
        pd_data.columns = column_names

        if args.destination_var:
            IPython.get_ipython().push({args.destination_var: pd_data})
        else:
            print(data)


def load_ipython_extension(ipython):
    """
    Any module file that define a function named `load_ipython_extension`
    can be loaded via `%load_ext module.path` or be configured to be
    autoloaded by IPython at startup time.
    """
    ipython.register_magics(FlinkSQLMagic)

"""Flink SQL Client

This module wraps the flink sql rest api for simplier user
experience.

"""
import logging
from enum import Enum
import flink_sql_gateway_client
from flink_sql_gateway_client.api import default_api, flink_sql_api
from flink_sql_gateway_client import Configuration
from flink_sql_gateway_client.model.create_session_request import CreateSessionRequest
from flink_sql_gateway_client.model.execute_statement_request import (
    ExecuteStatementRequest,
)
from flink_sql_gateway_client.model.result_fetch_request import ResultFetchRequest


class Planner(Enum):
    """Types of Planners used in Flink"""

    BLINK = "blink"


class ExecutionType(Enum):
    """Types of execution used in Flink"""

    STREAMING = "streaming"
    BATCH = "batch"


class FlinkSQLOneTimeJob:
    """Flink job wrapper that returns a one time result
    from the flink sql gateway
    """

    def __init__(
        self,
        api_response,
    ):
        self.api_response = api_response

    def is_one_time(self):
        """Is this a one time job result

        Returns:
            bool: return true
        """
        return True

    def fetch_job_results(self, _):
        """Fetches result from parent execute statement

        Returns:
            api_response(json): A json representation of the results of your query
        """
        return self.api_response


class FlinkSQLJob:
    """Flink job wrapper that allows for fetching results and
    automatically deletes the job when the object is deleted.
    """

    def __init__(
        self,
        session_id: str,
        job_id: str,
        flink_sql_api_instance: flink_sql_api.FlinkSqlApi,
    ):
        """Constructs a flink sql job to poll data

        Args:
            session_id (str): The session id created went createing a session with Flink SQL
            job_id (string): The job id created from the SELECT statement
            flink_sql_api_instance (flink_sql_api.FlinkSqlApi): [description]
        """
        self.token = 0
        self.session_id = session_id
        self.job_id = job_id
        self.flink_sql_api_instance = flink_sql_api_instance

    def __del__(self):
        """Deletes the job with flink sql"""
        self.__delete_job()

    def __delete_job(self):
        """Deletes a job running on the server

        Args:
            job_id (string): A guid suppied from the flink sql gateway
        """
        try:
            api_response = self.flink_sql_api_instance.cancel_job(
                self.session_id, self.job_id
            )
            logging.info("Deleted Job: %s", api_response)
        except flink_sql_gateway_client.ApiException as api_exception:
            logging.error("Exception when deleting job: %s", api_exception)

    def is_one_time(self):
        """Is this a one time job result

        Returns:
            bool: return false
        """
        return False

    def fetch_job_results(self, max_fetch_size: int = 1):
        """Fetch job results from the flink sql gateway

        Args:
            max_fetch_size (int, optional): Number of records to fetch. Defaults to 1.

        Returns:
            api_response(json): A json representation of the results of your query
        """
        assert max_fetch_size > 0
        result_fetch_request = ResultFetchRequest(max_fetch_size=max_fetch_size)
        try:
            api_response = self.flink_sql_api_instance.get_job_results(
                self.session_id, self.job_id, self.token, result_fetch_request
            )
            self.token += 1
            return api_response
        except flink_sql_gateway_client.ApiException as api_exception:
            logging.error("Exception when getting job results: %s", api_exception)


class FlinkSQLClient:
    """Flink sql wrapper that creates sessions to run jobs on the
    flink sql gateway.
    """

    def __init__(
        self,
        host: str,
        port: int,
        session_name: str,
        planner: Planner = Planner.BLINK,
        execution_type: ExecutionType = ExecutionType.STREAMING,
    ):
        """Constructs a Flink SQL Client

        Args:
            host (string): host name or ip to use to connect tot he flink sql gateway
            port (int): port to use to connect to the flink sql gateway
            session_name (string): human readable name to name your session
            planner (string, optional): flink planner to use. Defaults to "blink".
            execution_type (string, optional): flink execution type ["batch", "streaming"]. Defaults to "streaming".
        """
        self.api_client = None
        self.default_api_instance = None
        self.flink_sql_api_instance = None
        self.configuration = Configuration(host=f"http://{host}:{port}/v1")
        self.create_session_request = CreateSessionRequest(
            session_name=session_name,
            planner=planner.value,
            execution_type=execution_type.value,
        )
        self.__connect()
        self.session_id = self.__create_session()

    def __del__(self):
        """Closes the session with flink sql"""
        self.__cancel_session()

    def __connect(self):
        """Connects to a flink sql gateway"""

        logging.info("Connecting to Flink SQL Gateway: %s", self.configuration.host)
        self.api_client = flink_sql_gateway_client.ApiClient(self.configuration)
        self.default_api_instance = default_api.DefaultApi(self.api_client)
        self.flink_sql_api_instance = flink_sql_api.FlinkSqlApi(self.api_client)
        self.__get_info()

    def __get_info(self):
        """Gets info from the flink sql gateway to ensure the connection was successful"""
        try:
            api_response = self.default_api_instance.info_get()
            logging.info("Connected with info: %s", api_response)
        except flink_sql_gateway_client.ApiException as api_exception:
            logging.error("Exception when getting info: %s", api_exception)

    def __create_session(self):
        """Creates a session with flink sql gatway.  Each flink sql client is
            expected to have only one session.

        Returns:
            session_id(string): A session id created by the flink sql gateway
        """
        try:
            api_response = self.flink_sql_api_instance.create_session(
                self.create_session_request
            )
            logging.info("Created Session: %s", api_response)
            return api_response["session_id"]
        except flink_sql_gateway_client.ApiException as api_exception:
            logging.error("Exception when creating a session: %s", api_exception)

    def __cancel_session(self):
        """Cancels a session that is created on the server."""
        try:
            api_response = self.flink_sql_api_instance.cancel_session(self.session_id)
            logging.info("Cancelled Session: %s", api_response)
        except flink_sql_gateway_client.ApiException as api_exception:
            logging.error("Exception when canceling a session: %s", api_exception)

    def execute_statement(self, statement: str, execution_timeout: int = 1000000):
        """Executes a sql statement on the flink sql gateway

        Args:
            statement (string): Flink SQL Statement.  See here: https://ci.apache.org/projects/flink/flink-docs-master/docs/dev/table/sql/overview/
            execution_timeout (int, optional): Amount of time to wait for the sql query to start up. Defaults to 1000000.

        Returns:
            FlinkSQLJob: If the flink sql statement is of type SELECT, this method returns a job class to fetch data
        """
        assert statement != ""
        execute_statement_request = ExecuteStatementRequest(
            statement=statement,
            execution_timeout=execution_timeout,
        )
        try:
            api_response = self.flink_sql_api_instance.execute_statement(
                self.session_id, execute_statement_request
            )
            logging.info("Executed SQL Statement: %s", api_response)
            if api_response["statement_types"][0] == "SELECT":
                # This is not great, something we might want to eventually parse
                job_id = api_response["results"][0]["data"][0][0]
                return FlinkSQLJob(self.session_id, job_id, self.flink_sql_api_instance)
            else:
                return FlinkSQLOneTimeJob(api_response)
        except flink_sql_gateway_client.ApiException as api_exception:
            logging.error("Exception when executing a statement: %s", api_exception)

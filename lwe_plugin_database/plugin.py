from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
from langchain_community.utilities import SQLDatabase

from lwe.core.plugin import Plugin
import lwe.core.util as util

class Database(Plugin):
    """
    Send natural language commands to a database
    """

    def default_config(self):
        return {
            'database': {
                'default': None,
            },
            'agent': {
                'verbose': True,
            },
        }

    def setup(self):
        self.log.info(f"Setting up database plugin, running with backend: {self.backend.name}")
        self.default_database = self.config.get('plugins.database.database.default') or self.config.get('database')
        self.agent_verbose = self.config.get('plugins.database.agent.verbose')
        self.disconnect()

    def get_shell_completions(self, _base_shell_completions):
        commands = {}
        commands[util.command_with_leader('database')] = util.list_to_completion_hash(['connect', 'disconnect'])
        return commands

    def connect(self, connection_string=None):
        # TODO: Connection testsing
        self.connection_string = connection_string or self.default_database
        self.database = SQLDatabase.from_uri(self.connection_string)
        llm = self.make_llm()
        toolkit = SQLDatabaseToolkit(
            llm=llm,
            db=self.database,
        )
        self.agent = create_sql_agent(
            llm=llm,
            toolkit=toolkit,
            verbose=self.agent_verbose,
            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        )

    def disconnect(self):
        self.connection_string = None
        self.database = None
        self.agent = None

    def command_database(self, arg):
        """
        Send natural language commands to a database

        WARNING: This is a dangerous command, use it at your own risk, there is
                 NO GUARANTEE that the integrity of your data will be preserved.

        Arguments:

            configure: Optional configuration commands, one of:
                connect: Connect to a database, requires a connection string in a format accepted by SQLAlchemy. Only one database can be connected at a time. If no connection string is provided, connects to the default database.
                disconnect: Disconnect from a database

            prompt: Prompt to send to the database

        Examples:
            {COMMAND} connect sqlite:///test.db
            {COMMAND} disconnect
            {COMMAND} List all tables in the database
        """
        if not arg:
            return False, arg, "Command is required"
        args = arg.split(maxsplit=1)
        if args[0] == 'connect':
            connection_string = args[1] if len(args) > 1 else None
            self.connect(connection_string)
            # TODO: Error handling on failed connect.
            return True, None, f"Database {self.connection_string} connected"
        if args[0] == 'disconnect':
            connection_string = self.connection_string
            self.disconnect()
            return True, None, f"Database {connection_string} disconnected"
        if not self.agent:
            return False, None, "No database connected"
        try:
            result = self.agent.invoke(arg)
        except ValueError as e:
            return False, arg, e
        return True, arg, result

import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path
from env import env
from resolvers.test_chat import TestChatResolver

class BotProcessor:

    RESOLVERS = {
        'resolver_name': TestChatResolver()
    }

    def process(self, bot_id, message):
        engine_path = Path(__file__)
        engine_path = (f"sqlite:///{engine_path.absolute()}/{env['database']}"
                       .replace("bot_processor.py", ""))
        engine = create_engine(engine_path, echo=False)
        with engine.connect() as connection:
            data = pd.read_sql_query(
                f"SELECT resolver FROM {env['database']} WHERE bot_id={bot_id}",
                connection
            )
        if len(data) == 0:
            return None
        resolver = data.resolver[0]
        return self.RESOLVERS[resolver].resolve(message)

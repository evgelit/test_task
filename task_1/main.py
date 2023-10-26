from user_parser import UserParser
from env import env

parser = UserParser(session_name=env['session_name'])
parser.parse_users(dialog_name=env['dialog_name'])

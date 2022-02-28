from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

channel = -1001623310468
chat_id = -1001631818891


BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str
ADMINS = env.list("ADMINS")  # Тут у нас будет список из админов
IP = env.str("ip")  # Тоже str, но для айпи адреса хоста

DB_USER = env.str("DB_USER")
DB_NAME = env.str("DB_NAME")
DB_PASS = env.str("DB_PASSWORD")
DB_HOST = env.str("DB_HOST")
DB_PLUGIN = env.str("DB_PLUGIN")
DB = env.str("DB")
DB_PORT = env.str("DB_PORT")
DB_LINK = f'{DB}+{DB_PLUGIN}://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'

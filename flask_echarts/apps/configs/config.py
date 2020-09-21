HOST = '127.0.0.1'
USER = 'root'
PASSWORD = 'aaaa'
DATABASE = 'flask'

SECRET_KEY = "abc"
SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://' + USER+':'+PASSWORD+'@'+HOST+':3306/'+DATABASE+'?charset=utf8mb4'
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = False
from database import execute


# # fetchall() - вытащить всё, что пришло из БД
# # fetchone() - вытащить первый пришедший из БД
# # fetchmany(N) - вытащить N строк из БД

# Создайте базу данных для хранения информации о фильмах, включая 
# название, режиссера, год выпуска и оценку IMDb.
# Реализуйте функции для
#  добавления, обновления, удаления и получения данных о фильмах.
# stmt = """
# CREATE TABLE users (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     username VARCHAR(255),
#     password VARCHAR(255)
# );
# """


# print(execute(stmt, (), is_commitable=True))

stmt = """
CREATE TABLE user_history (
    user_id INTEGER PRIMARY KEY,
    request VARCHAR(255)
);
"""


print(execute(stmt, (), is_commitable=True))
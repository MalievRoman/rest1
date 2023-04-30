from requests import get, post, delete, put

# Создайте файл test.py, в котором проверьте ответы сервера на следующие запросы:
#
# Получение всех работ
# Корректное получение одной работы
# Ошибочный запрос на получение одной работы — неверный id
# Ошибочный запрос на получение одной работы — строка
#
# print(get('http://localhost:8080/api/jobs').json())
# print(get('http://localhost:8080/api/jobs/2').json())
# print(get('http://localhost:8080/api/jobs/-1').json())
# print(get('http://localhost:8080/api/jobs/haha').json())
#
#
# Напишите файл тестирования корректного запроса и нескольких некорректных (не менее трех).
# В файле должны присутствовать комментарии, в чем именно заключается некорректность запроса.
# Добавьте запрос на получение всех работ, чтобы убедиться, что работа добавлена.
# print(get('http://localhost:8080/api/jobs').json())
#
# # корректный
# print(post('http://localhost:8080/api/jobs',
#            json={"id": 3, "team_leader_id": 1, "job": "hello", "work_size": 2,
#                  "hazard_category": 9, "collaborators": "2, 3",
#                  "start_date": None, "end_date": None, "is_finished": True}).json())
# # нет такого Тимлида
# print(post('http://localhost:8080/api/jobs',
#            json={"id": 3, "team_leader_id": 53, "job": "hello", "work_size": 2,
#                  "hazard_category": 9, "collaborators": "2, 3",
#                  "start_date": None, "end_date": None, "is_finished": True}).json())
# # уже есть такой id работы
# print(post('http://localhost:8080/api/jobs',
#            json={"id": 2, "team_leader_id": 1, "job": "hello", "work_size": 2,
#                  "hazard_category": 9, "collaborators": "2, 3",
#                  "start_date": None, "end_date": None, "is_finished": True}).json())
# # не указана продолжительность работы
# print(post('http://localhost:8080/api/jobs',
#            json={"id": 2, "team_leader_id": 1, "job": "hello",
#                  "hazard_category": 9, "collaborators": "2, 3",
#                  "start_date": None, "end_date": None, "is_finished": True}).json())
#
#
# # Напишите файл тестирования корректного запроса на удаление и нескольких некорректных.
# # Добавьте запрос на получение всех работ, чтобы убедиться, что работа удалена.
# print(get('http://localhost:8080/api/jobs').json())
#
# # работы с id = 999 нет в базе
# print(delete('http://localhost:8080/api/jobs/999').json())
#
# # работы с id в виде строки нет в базе
# print(delete('http://localhost:8080/api/jobs/авфы').json())
#
# print(delete('http://localhost:8080/api/jobs/3').json())
#
# print(get('http://localhost:8080/api/jobs').json())


# Напишите файл тестирования корректного запроса на редактирование и нескольких некорректных.
# Добавьте запрос на получение всех работ, чтобы убедиться, что работа изменена.
print(get('http://localhost:8080/api/jobs').json())

# корректный
print(put('http://localhost:8080/api/jobs/2',
          json={"team_leader_id": 2, "job": "Exploration of mineral resources", "work_size": 2,
                "hazard_category": 5, "collaborators": "2, 3",
                "start_date": None, "end_date": None, "is_finished": True}).json())

# нет такой работы
print(put('http://localhost:8080/api/jobs/5',
          json={"team_leader_id": 2, "job": "Exploration of mineral resources", "work_size": 2,
                "hazard_category": 5, "collaborators": "2, 3",
                "start_date": None, "end_date": None, "is_finished": True}).json())

# нет такого тимлида
print(put('http://localhost:8080/api/jobs/1',
          json={"team_leader_id": 2000, "job": "Exploration of mineral resources", "work_size": 2,
                "hazard_category": 5, "collaborators": "2, 3",
                "start_date": None, "end_date": None, "is_finished": True}).json())

print(get('http://localhost:8080/api/jobs').json())

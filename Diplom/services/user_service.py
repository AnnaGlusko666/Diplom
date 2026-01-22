import json
import uuid

FILE_PATH = "data/users.json"


def load_data():
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def register_teacher(login, password):
    data = load_data()
    for t in data["teachers"]:
        if t["login"] == login:
            return False
    data["teachers"].append({
        "id": str(uuid.uuid4()),
        "login": login,
        "password": password,
        "students": []
    })
    save_data(data)
    return True


def auth_teacher(login, password):
    data = load_data()
    for t in data["teachers"]:
        if t["login"] == login and t["password"] == password:
            return t
    return None


def auth_student(login, password):
    data = load_data()
    for s in data["students"]:
        if s["login"] == login and s["password"] == password:
            return s
    return None


def add_student(teacher_id, name):
    data = load_data()
    login = f"student_{uuid.uuid4().hex[:5]}"
    password = uuid.uuid4().hex[:4]

    student = {
        "id": str(uuid.uuid4()),
        "name": name,
        "login": login,
        "password": password,
        "teacher_id": teacher_id
    }

    data["students"].append(student)
    save_data(data)
    return student

import requests

BASE_URL = "http://127.0.0.1:8000/students/"


def test_create_student():
    print("\n----- Creating Student -----")

    payload = {
        "name": "Alice",
        "age": 22,
        "Course": "Python",
        "Score": 89.5
    }

    response = requests.post(BASE_URL, json=payload)
    print("Status Code:", response.status_code)
    print("Response:", response.json())


def test_get_all_students():
    print("\n----- Getting All Students -----")

    response = requests.get(BASE_URL)
    print("Status Code:", response.status_code)
    print("Response:", response.json())


def test_get_single_student(student_id=1):
    print("\n----- Getting Single Student -----")

    response = requests.get(BASE_URL + str(student_id))
    print("Status Code:", response.status_code)
    print("Response:", response.json())


def test_update_student(student_id=1):
    print("\n----- Updating Student -----")

    payload = {
        "Score": 95.0
    }

    response = requests.put(BASE_URL + str(student_id), json=payload)
    print("Status Code:", response.status_code)
    print("Response:", response.json())


def test_delete_student(student_id=1):
    print("\n----- Deleting Student -----")

    response = requests.delete(BASE_URL + str(student_id))
    print("Status Code:", response.status_code)
    print("Response:", response.json())


if __name__ == "__main__":
    test_create_student()
    test_get_all_students()
    test_get_single_student()
    test_update_student()
    test_delete_student()

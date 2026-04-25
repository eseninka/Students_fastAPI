import pytest
import os
from fastapi import UploadFile
from io import BytesIO
import psycopg2


@pytest.fixture
def data_preparation_1_user():
    data = "full_name,estimation\nИванов Иван Иванович,2"
    file = BytesIO(data.encode("utf-8"))
    upload_file = UploadFile(filename="data_test_post.csv", file=file)
    yield upload_file


@pytest.fixture(scope="session")
def connect_db():
    HOST = os.getenv("HOST")
    NAME_USER = os.getenv("NAME_USER")
    PASSWORD = os.getenv("PASSWORD")
    DATABASE = os.getenv("DATABASE")
    connection = psycopg2.connect(host=HOST, user=NAME_USER, password=PASSWORD, database=DATABASE)
    connection.autocommit = True

    yield connection
    connection.close()


@pytest.fixture(scope="function")
def clean_db(connect_db):
    with connect_db.cursor() as cursor:
        cursor.execute("TRUNCATE TABLE students, data_about_students RESTART IDENTITY CASCADE")
    yield connect_db
    with connect_db.cursor() as cursor:
        cursor.execute("TRUNCATE TABLE students, data_about_students RESTART IDENTITY CASCADE")

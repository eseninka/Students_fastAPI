import psycopg2
import csv
from fastapi import APIRouter, status, UploadFile, File, HTTPException
import os
from dotenv import load_dotenv
from schemas.schem import SGrade
import codecs

load_dotenv()

HOST = os.getenv("HOST")
NAME_USER = os.getenv("NAME_USER")
PASSWORD = os.getenv("PASSWORD")
DATABASE = os.getenv("DATABASE")
CONNECT = os.getenv("CONNECT")

router_student = APIRouter(prefix="/students", tags=["Статистика"])
router_upload = APIRouter(prefix="/upload-grades", tags=["Загрузка данных"])


@router_upload.post("")
async def upload_data(data: UploadFile = File(...)):
    if not (data.filename.endswith('.csv')):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f"Файл должен быть с расширением .csv"
        )
    stream = codecs.iterdecode(data.file, 'utf-8')
    reader = csv.DictReader(stream)
    valid_rows = []
    for row in reader:
        try:
            validated_data = SGrade(**row)
            valid_rows.append(validated_data.model_dump())
        except Exception as e:
            raise HTTPException(status_code=422, detail=f"Ошибка в данных: {e}")

    s4 = 0
    connection = psycopg2.connect(host=HOST, user=NAME_USER, password=PASSWORD, database=DATABASE)
    connection.autocommit = True
    try:
        with connection.cursor() as cursor:
            for records in valid_rows:
                cursor.execute('select student_id from students where full_name=%s', (records['full_name'],))
                fet = cursor.fetchone()
                id_students = fet if fet else 0
                if id_students == 0:
                    s4 += 1
                    cursor.execute('insert into students(full_name) values (%s)', (records['full_name'],))
                    cursor.execute('select student_id from students where full_name=%s', (records['full_name'],))
                    id_students = cursor.fetchone()
                cursor.execute('insert into data_about_students(estimation, student_id) values (%s, %s)',
                               (records['estimation'], id_students))
    except Exception as e:
        print(f'info: ошибка {e}')
    finally:
        if connection:
            connection.close()
            print('info: коннект закрыт')
    return {"status": "ok", "records_loaded": len(valid_rows), "students": s4}


@router_student.get("/more-than-3-twos")
async def create_task():
    connection = psycopg2.connect(host=HOST, user=NAME_USER, password=PASSWORD, database=DATABASE)
    connection.autocommit = True
    data_res = []
    try:
        with connection.cursor() as cursor:
            cursor.execute('select students.full_name, COUNT(d_a_s.estimation) from data_about_students as d_a_s JOIN students USING(student_id) where d_a_s.estimation = 2 group by students.full_name having count(d_a_s.estimation) > 3')
            data_more_than_3_twos = cursor.fetchall()
    except Exception as e:
        print(f'info: ошибка {e}')
    finally:
        if connection:
            connection.close()
            print('info: коннект закрыт')
    for records in data_more_than_3_twos:
        data_res.append({"full_name" : records[0], "count_twos" : records[1]})
    return data_res

@router_student.get("/less-than-5-twos")
async def create_task():
    connection = psycopg2.connect(host=HOST, user=NAME_USER, password=PASSWORD, database=DATABASE)
    connection.autocommit = True
    data_res = []
    try:
        with connection.cursor() as cursor:
            cursor.execute('select students.full_name, COUNT(d_a_s.estimation) from data_about_students as d_a_s JOIN students USING(student_id) where d_a_s.estimation = 2 group by students.full_name having count(d_a_s.estimation) < 5')
            less_than_5_twos = cursor.fetchall()
    except Exception as e:
        print(f'info: ошибка {e}')
    finally:
        if connection:
            connection.close()
            print('info: коннект закрыт')
    for records in less_than_5_twos:
        data_res.append({"full_name" : records[0], "count_twos" : records[1]})
    return data_res
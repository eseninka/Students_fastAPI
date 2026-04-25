from routers.students import more_3_twos, less_5_twos
import pytest


@pytest.mark.get
@pytest.mark.parametrize("data, count", [pytest.param([{"full_name": "Петров Пётр Петрович", "estimation": 3},
                                                       {"full_name": "Петров Пётр Петрович", "estimation": 3},
                                                       {"full_name": "Петров Пётр Петрович", "estimation": 3},
                                                       {"full_name": "Петров Пётр Петрович", "estimation": 3}], 0,
                                                      id="zero twos"),
                                         pytest.param([{"full_name": "Петров Пётр Петрович", "estimation": 2},
                                                       {"full_name": "Петров Пётр Петрович", "estimation": 3},
                                                       {"full_name": "Петров Пётр Петрович", "estimation": 3},
                                                       {"full_name": "Петров Пётр Петрович", "estimation": 3}], 0,
                                                      id="one twos"),
                                         pytest.param([{"full_name": "Петров Пётр Петрович", "estimation": 2},
                                                       {"full_name": "Петров Пётр Петрович", "estimation": 2},
                                                       {"full_name": "Петров Пётр Петрович", "estimation": 3},
                                                       {"full_name": "Петров Пётр Петрович", "estimation": 3}], 0,
                                                      id="two twos"),
                                         pytest.param([{"full_name": "Петров Пётр Петрович", "estimation": 2},
                                                       {"full_name": "Петров Пётр Петрович", "estimation": 2},
                                                       {"full_name": "Петров Пётр Петрович", "estimation": 2},
                                                       {"full_name": "Петров Пётр Петрович", "estimation": 2}], 1,
                                                      id="four twos"),
                                         pytest.param([{"full_name": "Петров Пётр Петрович", "estimation": 2},
                                                       {"full_name": "Петров Пётр Петрович", "estimation": 2},
                                                       {"full_name": "Петров Пётр Петрович", "estimation": 2},
                                                       {"full_name": "Петров Пётр Петрович", "estimation": 2},
                                                       {"full_name": "Иванов Иван Иванович", "estimation": 2},
                                                       {"full_name": "Иванов Иван Иванович", "estimation": 2},
                                                       {"full_name": "Иванов Иван Иванович", "estimation": 2},
                                                       {"full_name": "Иванов Иван Иванович", "estimation": 2}
                                                       ], 2,
                                                      id="two more 3 twos")])
@pytest.mark.asyncio
async def test_more_3_twos(clean_db, data, count):
    conn = clean_db
    try:
        with conn.cursor() as cursor:
            for records in data:
                cursor.execute('select student_id from students where full_name=%s', (records['full_name'],))
                fet = cursor.fetchone()
                id_students = fet if fet else 0
                if id_students == 0:
                    cursor.execute('insert into students(full_name) values (%s)', (records['full_name'],))
                    cursor.execute('select student_id from students where full_name=%s', (records['full_name'],))
                    id_students = cursor.fetchone()
                cursor.execute('insert into data_about_students(estimation, student_id) values (%s, %s)',
                               (records['estimation'], id_students))
    except Exception as e:
        print(f'info: ошибка {e}')
        raise e
    res = await more_3_twos()
    assert len(res) == count


@pytest.mark.get
@pytest.mark.parametrize("data, count", [pytest.param([{"full_name": "Петров Пётр Петрович", "estimation": 3},
                                                       {"full_name": "Петров Пётр Петрович", "estimation": 3},
                                                       {"full_name": "Петров Пётр Петрович", "estimation": 3},
                                                       {"full_name": "Петров Пётр Петрович", "estimation": 3}], 0,
                                                      id="zero twos"),
                                         pytest.param([{"full_name": "Петров Пётр Петрович", "estimation": 2},
                                                       {"full_name": "Петров Пётр Петрович", "estimation": 3},
                                                       {"full_name": "Петров Пётр Петрович", "estimation": 3},
                                                       {"full_name": "Петров Пётр Петрович", "estimation": 3}], 1,
                                                      id="one twos"),
                                         pytest.param([{"full_name": "Петров Пётр Петрович", "estimation": 2},
                                                       {"full_name": "Иванов Иван Иванович", "estimation": 2},
                                                       {"full_name": "Петров Пётр Петрович", "estimation": 3},
                                                       {"full_name": "Петров Пётр Петрович", "estimation": 3}], 2,
                                                      id="two twos"),
                                         pytest.param([{"full_name": "Петров Пётр Петрович", "estimation": 2},
                                                       {"full_name": "Иванов Иван Иванович", "estimation": 2},
                                                       {"full_name": "Матвеев Матвей Матвеевич", "estimation": 2}], 3,
                                                      id="three twos"),
                                         pytest.param([{"full_name": "Петров Пётр Петрович", "estimation": 2},
                                                       {"full_name": "Петров Пётр Петрович", "estimation": 2},
                                                       {"full_name": "Петров Пётр Петрович", "estimation": 2},
                                                       {"full_name": "Петров Пётр Петрович", "estimation": 2},
                                                       {"full_name": "Петров Пётр Петрович", "estimation": 2},
                                                       {"full_name": "Матвеев Матвей Матвеевич", "estimation": 2},
                                                       {"full_name": "Иванов Иван Иванович", "estimation": 2},
                                                       {"full_name": "Иванов Иван Иванович", "estimation": 2}
                                                       ], 2,
                                                      id="two and more 5")])
@pytest.mark.asyncio
async def test_less_5_twos(clean_db, data, count):
    conn = clean_db
    try:
        with conn.cursor() as cursor:
            for records in data:
                cursor.execute('select student_id from students where full_name=%s', (records['full_name'],))
                fet = cursor.fetchone()
                id_students = fet if fet else 0
                if id_students == 0:
                    cursor.execute('insert into students(full_name) values (%s)', (records['full_name'],))
                    cursor.execute('select student_id from students where full_name=%s', (records['full_name'],))
                    id_students = cursor.fetchone()
                cursor.execute('insert into data_about_students(estimation, student_id) values (%s, %s)',
                               (records['estimation'], id_students))
    except Exception as e:
        print(f'info: ошибка {e}')
        raise e
    res = await less_5_twos()
    assert len(res) == count

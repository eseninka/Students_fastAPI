from routers.students import upload_data
import pytest
from fastapi import UploadFile
from io import BytesIO
from fastapi import status, HTTPException
from pydantic import ValidationError

@pytest.mark.post
@pytest.mark.parametrize("csv_content, expected_records, expected_students", [
    # Успешные сценарии
    pytest.param("full_name,estimation\nИванов Иван Иванович,2", 1, 1, id="one students"),
    pytest.param("full_name,estimation\n", 0, 0, id="zero students"),
    pytest.param("full_name,estimation\nИванов Иван Иванович,2\nПетров Пётр Петрович,5", 2, 2, id="two students")
])
@pytest.mark.asyncio
async def test_upload_data_success(clean_db, csv_content, expected_records, expected_students):
    file = BytesIO(csv_content.encode("utf-8"))
    upload_file = UploadFile(filename="test.csv", file=file)

    resp = await upload_data(upload_file)
    assert resp == {
        "status": "ok",
        "records_loaded": expected_records,
        "students": expected_students
    }


@pytest.mark.post
@pytest.mark.asyncio
async def test_upload_data_failed_422_not_csv(clean_db):
    csv_content = "full_name,estimation\nИванов Иван Иванович,2"
    file = BytesIO(csv_content.encode("utf-8"))
    upload_file = UploadFile(filename="test.txt", file=file)
    with pytest.raises(HTTPException) as e:
        await upload_data(upload_file)
    assert e.value.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


@pytest.mark.post
@pytest.mark.asyncio
async def test_upload_data_failed_422_not_valid(clean_db):
    csv_content ="full_name,estimation\nИванов Иван Иванович,two"
    file = BytesIO(csv_content.encode("utf-8"))
    upload_file = UploadFile(filename="test.csv", file=file)
    with pytest.raises(HTTPException) as e:
        await upload_data(upload_file)
    assert e.value.status_code == 422

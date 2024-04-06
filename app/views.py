import traceback
from fastapi import APIRouter, UploadFile, File
import zipfile
import csv
import io

from app.base.utils import send_message
from app.dto import PeaceAwardOutput
from app.exceptions import ValidationError
from app.prompt import get_peace_award

router = APIRouter()


@router.post("/peace-award", response_model=PeaceAwardOutput)
async def peace_award(file: UploadFile = File(...)) -> PeaceAwardOutput:
    file_extension = file.filename.split(".")[-1]  # type: ignore

    if file_extension == "zip":
        # ZIP 파일 처리
        try:
            content = await file.read()
            with zipfile.ZipFile(io.BytesIO(content), "r") as zip_ref:
                # ZIP 파일 내의 모든 파일을 읽어서 하나의 문자열로 합침
                text_contents = []
                for filename in zip_ref.namelist():
                    with zip_ref.open(filename) as f:
                        if filename.endswith(".txt") or filename.endswith(".csv"):
                            text_contents.append(f.read().decode("utf-8"))
                return await get_peace_award("\n".join(text_contents))
        except Exception as e:
            send_message(str(traceback.format_exc()))
            raise ValidationError(f"ZIP 파일 처리 중 오류 발생: {e}")

    elif file_extension == "csv":
        # CSV 파일 처리
        try:
            content = await file.read()
            csv_reader = csv.reader(io.StringIO(content.decode("utf-8")))
            rows = [",".join(row) for row in csv_reader]
            return await get_peace_award("\n".join(rows))
        except Exception as e:
            send_message(str(traceback.format_exc()))
            raise ValidationError(f"CSV 파일 처리 중 오류 발생: {e}")

    elif file_extension == "txt":
        # TXT 파일 처리
        try:
            content = await file.read()
            return await get_peace_award(content.decode("utf-8"))
        except Exception as e:
            send_message(str(traceback.format_exc()))
            raise ValidationError(f"TXT 파일 처리 중 오류 발생: {e}")

    else:
        raise ValidationError("지원하지 않는 파일 형식입니다.")

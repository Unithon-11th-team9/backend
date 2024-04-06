import traceback
from fastapi import APIRouter, UploadFile, File
import zipfile
import csv
import io

from app import db
from app.base.utils import send_message
from app.dto import AnalysisStatistics, PeaceAwardOutput
from app.exceptions import ValidationError
from app.prompt import get_peace_award
from app.db import save_to_result

router = APIRouter()


@router.post("/peace-award", response_model=PeaceAwardOutput, status_code=200)
async def peace_award(file: UploadFile = File(...)) -> PeaceAwardOutput:
    """대화내용에 대한 평화상 데이터를 응답합니다."""
    file_extension = file.filename.split(".")[-1]  # type: ignore
    start_index = -10000  # 속도를 위해 최근 10000자 미만으로 요청

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

                chat_content = "\n".join(text_contents)[start_index:]
        except Exception as e:
            send_message(str(traceback.format_exc()))
            raise ValidationError(f"ZIP 파일 처리 중 오류 발생: {e}")

    elif file_extension == "csv":
        # CSV 파일 처리
        try:
            content = await file.read()
            csv_reader = csv.reader(io.StringIO(content.decode("utf-8")))
            rows = [",".join(row) for row in csv_reader]

            # 속도를 위해 최근 10000자 미만으로 요청
            chat_content = "\n".join(rows)[start_index:]
        except Exception as e:
            send_message(str(traceback.format_exc()))
            raise ValidationError(f"CSV 파일 처리 중 오류 발생: {e}")

    elif file_extension == "txt":
        # TXT 파일 처리
        try:
            content = await file.read()

            # 속도를 위해 최근 10000자 미만으로 요청
            chat_content = content.decode("utf-8")[start_index:]
        except Exception as e:
            send_message(str(traceback.format_exc()))
            raise ValidationError(f"TXT 파일 처리 중 오류 발생: {e}")

    else:
        raise ValidationError("지원하지 않는 파일 형식입니다.")

    result = await get_peace_award(chat_content)
    try:
        await save_to_result(
            result=result.model_dump(mode="json"), char_count=len(chat_content)
        )
    except Exception:
        send_message(str(traceback.format_exc()))
        # 저장은 로그용이므로 실패해도 결과는 반환합니다.
        pass
    return result


@router.get("/analysis-statistics", response_model=AnalysisStatistics, status_code=200)
async def fetch_analysis_statistics() -> AnalysisStatistics:
    """현재까지의 분석 통계를 응답합니다."""
    analysis_statistics = await db.fetch_analysis_statistics()
    return AnalysisStatistics(**analysis_statistics)

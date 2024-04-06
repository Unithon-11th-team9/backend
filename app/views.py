from fastapi import APIRouter


router = APIRouter()


@router.post("/")
def ping2() -> str:
    return "Hello, Unithon!"

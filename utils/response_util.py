from fastapi.responses import JSONResponse

from pydantic import BaseModel

from fastapi import HTTPException

class ResponseOut(BaseModel):
    data: dict
    message: str
    response_code: str

class ErrorOut(BaseModel):
    message: str
    response_code: str

class BadResponseOut(BaseModel):
    detail: ErrorOut

class ResponseUtil:
    @staticmethod
    def api_response(data:dict ={},message: str="Success",response_code: str="200",status_code: int=200):
        return JSONResponse(status_code=status_code, content={
            "data": data,
            "message": message,
            "response_code": response_code
        })
    @staticmethod
    def internal_server_response(message: str="Internal Server Error",response_code: str="500",status_code: int=500):
        raise HTTPException(
            status_code=status_code,
            detail={
            "message": message,
            "response_code": response_code
            })




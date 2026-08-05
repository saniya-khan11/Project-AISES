from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


def register_exception_handlers(app: FastAPI):
    """
    Register global exception handlers for the AISES REST API.
    """

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError,
    ):
        return JSONResponse(
            status_code=422,
            content={
                "success": False,
                "error": "Validation Error",
                "details": exc.errors(),
            },
        )

    @app.exception_handler(FileNotFoundError)
    async def file_not_found_handler(
        request: Request,
        exc: FileNotFoundError,
    ):
        return JSONResponse(
            status_code=404,
            content={
                "success": False,
                "error": "File Not Found",
                "details": str(exc),
            },
        )

    @app.exception_handler(RuntimeError)
    async def runtime_error_handler(
        request: Request,
        exc: RuntimeError,
    ):
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "Runtime Error",
                "details": str(exc),
            },
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(
        request: Request,
        exc: Exception,
    ):
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "Internal Server Error",
                "details": str(exc),
            },
        )
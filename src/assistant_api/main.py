"""Team API foundation — Lab 4.  Run:  uvicorn assistant_api.main:create_app --factory --reload

GET /health and T1 chat are complete. Other owners implement T2–T4/H1 and Part F.

Endpoints (v1): GET /health, POST /v1/chat, POST /v1/feedback, GET /v1/feedback (admin),
GET /v1/weather, GET /v1/offices
"""

from __future__ import annotations

import uuid

from fastapi import Depends, FastAPI, Header, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from assistant_api.config import APISettings, load_api_settings, resolve_data_dir
from assistant_api.ratelimit import RateLimiter
from assistant_api.schemas import ChatRequest, ChatResponse, ErrorResponse, FeedbackIn, FeedbackOut, OfficeOut, Weather
from assistant_api.weather import ExternalServiceError, WeatherClient
from assistant_core import AssistantService
from assistant_core.models import Message


def create_app(
    settings: APISettings | None = None, service: AssistantService | None = None, weather: WeatherClient | None = None
) -> FastAPI:
    settings = settings or load_api_settings()
    service = service or AssistantService.default(settings=settings, data_dir=resolve_data_dir(settings))
    weather = weather or WeatherClient(
        settings.weather_url, settings.campus_lat, settings.campus_lon, timeout_s=settings.weather_timeout_s
    )
    feedback_store: list[FeedbackOut] = []  # Lab 5 replaces this with a database

    app = FastAPI(
        title="Study Assistant API", version="1.0.0", description="Backend of the CSC10014 Smart Virtual Assistant."
    )

    app.state.feedback_store = feedback_store
    app.state.rate_limiter = RateLimiter(settings.rate_limit_per_min)

    def error(code: int, key: str, message: str) -> JSONResponse:
        return JSONResponse(status_code=code, content={"error": {"code": key, "message": message}})

    @app.exception_handler(RequestValidationError)
    async def on_validation(_: Request, exc: RequestValidationError):
        first = exc.errors()[0]
        field = ".".join(str(p) for p in first["loc"][1:]) or "body"
        return error(422, "invalid_request", f"{field}: {first['msg']}")

    @app.exception_handler(StarletteHTTPException)
    async def on_http(_: Request, exc: StarletteHTTPException):
        return error(exc.status_code, str(exc.detail).lower().replace(" ", "_"), str(exc.detail))

    def require_admin(x_api_key: str | None = Header(default=None)) -> None:
        if not settings.api_admin_key or x_api_key != settings.api_admin_key:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Missing or invalid API key")

    @app.get("/health", tags=["ops"])
    def health() -> dict:
        return {"status": "ok", "version": app.version}

    @app.post(
        "/v1/chat",
        response_model=ChatResponse,
        tags=["chat"],
        responses={422: {"model": ErrorResponse}, 429: {"model": ErrorResponse}},
    )
    def chat(req: ChatRequest, request: Request) -> ChatResponse:
        # Owner: Nguyễn Phúc Khánh (T1). Trần Phúc Khánh adds Part F enforcement
        # using app.state.rate_limiter before the service call below.
        resp = service.handle(Message(text=req.message, session_id=req.session_id))
        return ChatResponse(**resp.model_dump(), request_id=uuid.uuid4().hex[:12])

    @app.post("/v1/feedback", response_model=FeedbackOut, status_code=201, tags=["feedback"])
    def add_feedback(fb: FeedbackIn) -> FeedbackOut:
        # Owner: Kiệt. Use this same feedback_store with T3.
        # TODO T2 (3 lines):
        #   1. item = FeedbackOut(**fb.model_dump(), id=len(feedback_store) + 1, created_at=datetime.now(timezone.utc))
        #   2. add item to feedback_store
        #   3. return item
        raise NotImplementedError("T2")

    @app.get("/v1/feedback", response_model=list[FeedbackOut], tags=["feedback"], dependencies=[Depends(require_admin)])
    def list_feedback() -> list[FeedbackOut]:
        # Owner: Trần Phúc Khánh.
        # TODO T3 (1 line): return the list. The API-key check is already done by `require_admin` above.
        raise NotImplementedError("T3")

    @app.get("/v1/weather", response_model=Weather, tags=["external"], responses={503: {"model": ErrorResponse}})
    def campus_weather() -> Weather:
        # Owner: Trần Thành Lợi (T4). Upstream failures become a clean 503.
        try:
            return weather.current()
        except ExternalServiceError:
            raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "Weather service unavailable") from None

    @app.get(
        "/v1/offices",
        response_model=list[OfficeOut],
        tags=["offices"],
        summary="List campus offices",
        description="Retrieve all campus offices and opening hours sorted alphabetically.",
    )
    def list_offices() -> list[dict[str, str]]:
        # Owner: Phát (H1). Add all() to the directory actually used by the service.
        return [o.__dict__ for o in service.offices.all()]

    return app

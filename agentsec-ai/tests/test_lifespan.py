
from fastapi import FastAPI

from backend.main import create_app


def test_create_app_exposes_lifespan() -> None:
    app = create_app()

    assert isinstance(app, FastAPI)
    assert app.router.lifespan_context is not None

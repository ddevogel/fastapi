from pydantic import HttpUrl
import pytest
from fastapi import Request, HTTPException
from app.dependencies import RequestIdContext, get_state, check_404, verify_token


def test_request_id_context():
    r = RequestIdContext()
    assert r.get_request_id() is None
    r.set_request_id("bob")
    assert r.get_request_id() == "bob"
    r.reset()
    assert r.get_request_id() is None


def test_request_state():
    r = Request({"type": "http", "method": "GET", "path": "/abc/", "url": "url"})
    r.state.message = "the message"
    assert get_state(r).message == "the message"


@pytest.mark.asyncio
async def test_verify_token():
    with pytest.raises(HTTPException) as e:
        await verify_token("token")
    assert e.value.status_code == 401


def test_check_404_exception_response():
    check_404("response")


def test_check_404_exception_empty_response():
    with pytest.raises(HTTPException) as e:
        check_404(None)
    assert e.value.status_code == 404
    assert e.value.detail == "Item not found"

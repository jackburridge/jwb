import uvicorn

# application_start
async def application(scope, receive, send):
    # this application does not support other types
    assert scope["type"] == "http"
    await send(
        {
            "type": "http.response.start",
            "status": 200,
            "headers": [[b"content-type", b"text/plain"]],
        }
    )
    await send({"type": "http.response.body", "body": b"Hello, World!"})


# application_end

# using
uvicorn.run(application, host="0.0.0.0", port=8000)

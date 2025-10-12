import uvicorn


# app_start
async def app(scope, receive, send):
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


# app_end

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

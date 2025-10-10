import wsgiref.simple_server


# simple_app_start
def simple_app(environ, start_response):
    status = "200 OK"
    headers = [("Content-type", "text/plain; charset=utf-8")]

    start_response(status, headers)

    return [b"Hello World!"]


# simple_app_end


# add_header_start
def add_header(app):
    def wrapper(environ, start_response):
        wrapped_start_response = lambda status, headers: start_response(
            status, headers + [("X-Powered-By", "WSGI")]
        )
        return app(environ, wrapped_start_response)

    return wrapper


# add_header_end


# using
with wsgiref.simple_server.make_server("", 8000, add_header(simple_app)) as httpd:
    print("Serving on port 8000...")
    httpd.serve_forever()

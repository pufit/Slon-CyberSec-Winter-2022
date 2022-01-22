from starlette.requests import Request
from starlette.responses import Response


async def app(scope, receive, send):
    assert scope['type'] == 'http'
    request = Request(scope, receive)
    body = await request.body()
    content = '%s %s %s' % (request.method, request.url.path, body)
    print(content)

    response = Response(content, media_type='text/plain', headers={
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': '*'
    })
    await response(scope, receive, send)

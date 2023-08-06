# pylint: skip-file
import asyncio
import typing

import pydantic
import uvicorn
import marshmallow

from unimatrix.ext import webapi
from unimatrix.ext.webapi import ResourceEndpointSet
from unimatrix.ext.webapi import __boot__


asyncio.run(__boot__.on_setup())


app = webapi.Application(
    allowed_hosts=['*'],
    enable_debug_endpoints=True
)


class BookEndpoints(ResourceEndpointSet):
    path_parameter = 'book_id'
    require_authentication = False

    class author_resource(ResourceEndpointSet):
        name = 'authors'
        path_parameter = 'author_id'
        require_authentication = False

        async def index(self):
            pass

        async def retrieve(self):
            pass

    subresources = [author_resource]

    class resource_class(marshmallow.Schema):
        title = marshmallow.fields.String(required=True)

    @webapi.action
    async def index_action(self):
        return "Index Action"

    @webapi.action(detail=True)
    async def detail_action(self, book_id: int):
        return f"Detail Action: {book_id}"

    async def apply(self, dto: dict):
        return dto

    async def create(self, dto: dict):
        return dto

    async def destroy(self, book_id: int):
        return book_id

    async def index(self):
        return "List all resources under the base path."

    async def purge(self):
        return "Destroy all resources under the base path."

    async def replace(self, book_id: str):
        return book_id

    async def retrieve(self, book_id: str):
        return book_id

    async def update(self, book_id: str):
        return book_id


BookEndpoints.add_to_router(app, '/books')

if __name__ == '__main__':
    uvicorn.run(app,
        host="127.0.0.1",
        port=5000,
        log_level="info"
    )

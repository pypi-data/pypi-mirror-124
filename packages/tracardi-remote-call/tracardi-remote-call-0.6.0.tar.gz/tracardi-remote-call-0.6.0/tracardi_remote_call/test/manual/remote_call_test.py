import asyncio

from tracardi_remote_call.model.configuration import Content
from tracardi_remote_call.plugin import RemoteCallAction


async def main():
    init = {
        "url": "http://localhost:8686/healthcheck",
        "method": "post",
        "timeout": 1,
        "headers": [
            ("X-AAA", "test")
        ],
        "cookies": {},
        "body": Content(
            content="""
            {"test": {
            "a": 1,
            "b": [1, 2]
            }} 
            """,
            type="application/json"
        )
    }

    plugin = RemoteCallAction(**init)

    payload = {

    }

    result = await plugin.run(payload)
    print(result)


asyncio.run(main())

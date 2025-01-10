import json

from grpclib import GRPCError, Status

from app.exceptions import ExpiredTokenError, BaseAPIError
from app.framework.dependencies import get_token_factory, get_db, get_token_repo, get_user_repo
from app.use_cases.auth_service import auth_case
from proto.auth_grpc import AuthBase
from grpclib.server import Server

from proto.auth_pb2 import AuthUserResponse


class AuthService(AuthBase):
    async def AuthUser(self, stream):
        async for db_session in get_db():
            try:
                request = await stream.recv_message()
                token_fact = await get_token_factory()
                user_repo = await get_user_repo(db_session)
                token_repo = await get_token_repo(user_repo)
                user = await auth_case(request.token, token_fact, token_repo, user_repo)
                await stream.send_message(AuthUserResponse(user_id=user.id, username=user.username))
            except BaseAPIError as e:
                raise GRPCError(Status.UNAUTHENTICATED, json.dumps(e.__dict__))


async def main():
    server = Server([AuthService()])
    await server.start("localhost", 50051)
    await server.wait_closed()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

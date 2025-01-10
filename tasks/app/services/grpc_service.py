import json

from fastapi import HTTPException
from grpclib import GRPCError
from grpclib.client import Channel

from app.proto.auth_grpc import AuthStub
from app.proto.auth_pb2 import AuthUserRequest, AuthUserResponse
from app.schemas.auth import UserBase


async def auth_user(token: str) -> UserBase:
    async with Channel('localhost', 50051) as channel:
        stub = AuthStub(channel)
        try:
            response: AuthUserResponse = await stub.AuthUser(AuthUserRequest(token=token))
            return UserBase(id=response.user_id, username=response.username)
        except GRPCError as e:
            data = json.loads(e.message)
            raise HTTPException(**data)

from concurrent import futures

import grpc

from app.exceptions import BaseAPIError
from app.framework.dependencies import get_token_factory, get_token_repo, get_user_repo
from app.use_cases.auth_service import auth_case
from proto import auth_pb2, auth_pb2_grpc


class AuthServicer(auth_pb2_grpc.AuthServiceServicer):
    async def AuthUser(self, request, context):
        try:
            user = await auth_case(
                request.token,
                token_fact=await get_token_factory(),
                token_repo=await get_token_repo(),
                user_repo=await get_user_repo()
            )
            return auth_pb2.AuthUserResponse(user_id=user.id, username=user.username)
        except BaseAPIError as e:
            context.abort(grpc.StatusCode, str(e))


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    auth_pb2_grpc.add_AuthServiceServicer_to_server(AuthServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

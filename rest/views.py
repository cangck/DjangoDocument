# Create your views here.
import json

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


def get_request_args(func):
    def _get_request_args(self, request):
        if request.method == 'GET':
            args = request.GET
        else:
            body = request.body
            if body:
                try:
                    args = json.loads(body)
                except Exception as e:
                    print
                    e
                    # return makeJsonResponse(status=StatusCode.EXECUTE_FAIL, message=str(e))
                    args = request.POST
            else:
                args = request.POST
        return func(self, request, args)

    return _get_request_args


class UserView(APIView):
    """
    处理用户的信息
    """
    permission_classes = (AllowAny,)

    @swagger_auto_schema(operation_description="partial_update description override",
                         responses={404: 'id not found'},
                         manual_parameters=[openapi.Parameter("username", openapi.IN_QUERY,
                                                              description="用户名",
                                                              type=openapi.TYPE_STRING),
                                            openapi.Parameter("password",
                                                              openapi.IN_QUERY,
                                                              type=openapi.TYPE_STRING,
                                                              ),
                                            openapi.Parameter("Content-Type",
                                                              openapi.IN_HEADER,
                                                              description="服务器返回的数据类型",
                                                              type=openapi.TYPE_STRING,
                                                              default='application/json'
                                                              )
                                            ])
    @get_request_args
    def get(self, request, *args, **kwargs):
        return Response("get")

    @swagger_auto_schema(
        operation_description="apiview post description override",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', "password"],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING)

            },
        ),
        security=[],

    )
    @get_request_args
    def post(self, request, *args, **kwargs):
        """
        添加用户
        """
        return Response("post")

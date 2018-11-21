#使用drf-yasg实现文档生成
###依赖库

    certifi==2018.10.15
    chardet==3.0.4
    click==6.7
    coreapi==2.3.3
    coreschema==0.0.4
    Django==2.1.3
    django-rest-swagger==2.2.0
    djangorestframework==3.9.0
    djangorestframework-jwt==1.11.0
    drf-yasg==1.11.0
    flex==6.13.2
    idna==2.7
    inflection==0.3.1
    itypes==1.1.0
    Jinja2==2.10
    jsonpointer==1.14
    jsonschema==2.6.0
    MarkupSafe==1.1.0
    openapi-codec==1.3.2
    PyJWT==1.6.4
    pytz==2018.7
    PyYAML==3.13
    requests==2.20.1
    rfc3987==1.3.8
    ruamel.yaml==0.15.78
    simplejson==3.16.0
    six==1.11.0
    strict-rfc3339==0.7
    swagger-spec-validator==2.4.1
    ua-parser==0.8.0
    uritemplate==3.0.0
    urllib3==1.24.1
    user-agents==1.1.0
    validate-email==1.3

###第一步

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


###第二步

    # 对文档的一些说明信息
    swagger_info = openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="""This is a demo project for the [drf-yasg](https://github.com/axnsan12/drf-yasg) Django Rest Framework library.

    The `swagger-ui` view can be found [here](/cached/swagger).
    The `ReDoc` view can be found [here](/cached/redoc).
    The swagger YAML document can be found [here](/cached/swagger.yaml).

    You can log in using the pre-existing `admin` user with password `passwordadmin`.""",  # noqa
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    )

    SchemaView = get_schema_view(
        validators=['ssv', 'flex'],
        public=True,
        permission_classes=(permissions.AllowAny,),
    )


    # 对不同的客户端进行处理
    def root_redirect(request):
        user_agent_string = request.META.get('HTTP_USER_AGENT', '')
        user_agent = user_agents.parse(user_agent_string)

        if user_agent.is_mobile:
            schema_view = 'cschema-redoc'
        else:
            schema_view = 'cschema-swagger-ui'

        return redirect(schema_view, permanent=True)


    urlpatterns = [
        url(r'^admin/', admin.site.urls),
        # 通过用户代理工具类处理相关的界面显示
        url(r'^swagger(?P<format>.json|.yaml)$', SchemaView.without_ui(cache_timeout=0), name='schema-json'),
        url(r'^swagger/$', SchemaView.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        url(r'^redoc/$', SchemaView.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
        url(r'^redoc-old/$', SchemaView.with_ui('redoc-old', cache_timeout=0), name='schema-redoc-old'),

        url(r'^cached/swagger(?P<format>.json|.yaml)$', SchemaView.without_ui(cache_timeout=None), name='cschema-json'),
        url(r'^cached/swagger/$', SchemaView.with_ui('swagger', cache_timeout=None), name='cschema-swagger-ui'),
        url(r'^cached/redoc/$', SchemaView.with_ui('redoc', cache_timeout=None), name='cschema-redoc'),
        url(r'^$', root_redirect),
        path('admin/', admin.site.urls),
        path('rest/', include("rest.urls"))
    ]

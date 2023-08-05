from starlette_authlib.middleware import AuthlibMiddleware
# import secMgr
import os
import traceback as tb
import json
from starlette.datastructures import MutableHeaders, Secret
from collections import namedtuple
from starlette.types import ASGIApp, Message, Receive, Scope, Send
from starlette.responses import Response
from starlette.requests import HTTPConnection
from fastapi import HTTPException
from authlib.jose import jwt
from authlib.jose.errors import BadSignatureError, ExpiredTokenError, DecodeError
import time
import datetime

SecretKey = namedtuple("SecretKey", ("encode", "decode"))

# Use this code snippet in your app.
# If you need more information about configurations or implementing the sample code, visit the AWS docs:
# https://aws.amazon.com/developers/getting-started/python/

import boto3
import base64
from botocore.exceptions import ClientError
import os


def get_secret(secret_name):
    # secret_name = "dev-ml"
    region_name = os.environ.get('AWS_DEFAULT_REGION')  # "us-west-2"

    # Create a Secrets Manager client
    session = boto3.session.Session()

    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    # In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
    # See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
    # We rethrow the exception by default.

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
    else:
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
            return secret
        else:
            decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
            return decoded_binary_secret

    # Your code goes here.


class AuthlibMiddlewareAlbert(AuthlibMiddleware):
    def __init__(self,app: ASGIApp,*args, **kwargs):
        try:
            env = os.environ.get('ECS_CLUSTER_NAME')
            secrets = get_secret(env)#os.environ.get('ECS_CLUSTER_NAME'))
            secrets = json.loads(secrets)
            jwt_secret_token = secrets['JWT_TOKEN_SECRET']
            self.secrets = jwt_secret_token
        except Exception as e:
            print(str(e))
            print(tb.format_exc())
            secrets = ''#[]
            jwt_secret_token = ''
        
        super().__init__(app=app,secret_key=SecretKey(Secret(str(jwt_secret_token)), None),max_age=48*60*60)


    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] not in ("http", "websocket"):  # pragma: no cover
            await self.app(scope, receive, send)
            return

        connection = HTTPConnection(scope)
        initial_session_was_empty = True
        print(connection.headers.get('authorization'))
        # print(connection.cookies)

        try:
            try:
                header = connection.headers.get('authorization').split(' ')[1]
            except:
                header = connection.headers.get('authorization')
            payload = jwt.decode(
                header,
                key=self.secrets#jwt_secret_token
            #    str(
            #         self.jwt_secret.decode
            #         if self.jwt_secret.decode
            #         else self.jwt_secret.encode
            #     ),
                )
            payload.validate_exp(time.time(), 0)
            expiration = payload['exp'] if 'exp' in payload.keys() else 0
            if expiration == 0:
                if payload['iat']+self.max_age>time.mktime(datetime.date.today().timetuple()):
                    authorized = True
                else:
                    print('token expired')
                    raise ExpiredTokenError                
            else:
                if datetime(expiration)>datetime.now():
                    authorized = True
                else:
                    print('token expired')
                    raise ExpiredTokenError
            # authorized = True
            scope["session"] = payload
            initial_session_was_empty = False
            print('token valid')
            await self.app(scope, receive, send)
        except (BadSignatureError, ExpiredTokenError, DecodeError, AttributeError):
            scope["session"] = {}
            print('token invalid')
            # raise HTTPException(status_code=401, detail="Unauthorized")
            response = Response('Unauthorized', status_code=401, media_type='application/json')
            await response(scope, receive, send)

        #     expiration = payload['exp'] if 'exp' in payload.keys() else 0
        #     if expiration == 0:
        #         if payload['iat']+self.max_age>time.mktime(datetime.date.today().timetuple()):
        #             authorized = True
        #         else:
        #             authorized = False                
        #     else:
        #         if datetime(expiration)>datetime.now():
        #             authorized = True
        #         else:
        #             authorized = False
        #     authorized = True

        # except Exception as e:
        #     print(str(e))
        #     print(tb.format_exc())
        #     return False

        # if not authorized:
        #     # response.status_code = status.HTTP_401_UNAUTHORIZED
        #     response = JSONResponse(content={'error': 'Unauthorized'})
        #     response.status_code = status.HTTP_401_UNAUTHORIZED               
        #     return response
        # else:
        #     response = await original_route_handler(request)
        #     return response

        # if self.session_cookie in connection.cookies:
        #     data = connection.cookies[self.session_cookie].encode("utf-8")
        #     try:
        #         jwt_payload = jwt.decode(
        #             data,
        #             str(
        #                 self.jwt_secret.decode
        #                 if self.jwt_secret.decode
        #                 else self.jwt_secret.encode
        #             ),
        #         )
        #         jwt_payload.validate_exp(time.time(), 0)
        #         scope["session"] = jwt_payload
        #         initial_session_was_empty = False
        #         print('token valid')
        #     except (BadSignatureError, ExpiredTokenError, DecodeError):
        #         scope["session"] = {}
        #         print('token invalid')
        # else:
        #     scope["session"] = {}

        # async def send_wrapper(message: Message) -> None:
        #     if message["type"] == "http.response.start":
        #         if scope["session"]:
        #             if "exp" not in scope["session"]:
        #                 scope["session"]["exp"] = int(time.time()) + self.max_age
        #             data = jwt.encode(
        #                 self.jwt_header, scope["session"], str(self.jwt_secret.encode)
        #             )

        #             headers = MutableHeaders(scope=message)
        #             header_value = "%s=%s; path=/; Max-Age=%d; %s" % (
        #                 self.session_cookie,
        #                 data.decode("utf-8"),
        #                 self.max_age,
        #                 self.security_flags,
        #             )
        #             if self.domain:  # pragma: no cover
        #                 header_value += f"; domain={self.domain}"
        #             headers.append("Set-Cookie", header_value)
        #         elif not initial_session_was_empty:
        #             # The session has been cleared.
        #             headers = MutableHeaders(scope=message)
        #             header_value = "%s=%s; %s" % (
        #                 self.session_cookie,
        #                 "null; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT;",
        #                 self.security_flags,
        #             )
        #             if self.domain:  # pragma: no cover
        #                 header_value += f"; domain={self.domain}"
        #             headers.append("Set-Cookie", header_value)
        #     await send(message)

        

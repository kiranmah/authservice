# Authentication
For clients to authenticate, the JWT Bearer token should be included in the Authorization HTTP header. The key should be prefixed by the string literal "Bearer", with whitespace separating the two strings. For example:

```
Authorization: Bearer eyJ0eXAi1QiLC.eyJ0b2tlblLWM0YzEwODcyMzA0OCJ9.vgc415UaU5J1vKMHYK70
```

Unauthenticated responses that are denied permission will result in an HTTP `401 Unauthorized` response with an appropriate `WWW-Authenticate` header. For example:

```
WWW-Authenticate: Bearer realm="api"
```

The curl command line tool may be useful for testing token authenticated APIs. For example:

```bash
curl -X GET http://127.0.0.1:8000/api/v1/example/ -H 'Authorization: Bearer eyJ0eXAi1QiLC.eyJ0b2tlblLWM0YzEwODcyMzA0OCJ9.vgc415UaU5J1vKMHYK70'
```

## Retrieving Tokens
A registered user can retrieve their login and refresh tokens with the following request:

**Request**:

`POST` `api/login/`

Parameters:

Name | Type | Description
---|---|---
username | string | The user's username
password | string | The user's password

**Response**:
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2t4cCI6MTY0MDAzMTkyNywiaWF0IjoxNjM5OTQ1NTI3LCJqdGkiOiIwNDc1YmZhMmMzYTY0ZmRlODEwM2FhZDYyM2JhOTZTRiZWItYmEwZS0xOTY4OGNiMjg0MGUifQ.kxlgeqdZ_hzFnOMGXBetGvr81uNTvzBBbvJ8-D-YKbY",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBsImp0aSI6ImNkMzBhMTA4Y2IzNTQ1ZjE4ZDAzYjc2YWMwMjQ2MDE5IiwidXNlcl9pZCI6ImJkMzIxZmE5LTZkNjYtNGJlYi1iYTBlLTE5Njg4Y2IyODQwZSJ9.vMAFjfOefWRdFvZ6TKP6eHsCXHg"
}
```

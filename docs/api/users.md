# Users
Supports registering, updating, and deleting user accounts.

## Register a new user account

**Request**:

`POST` `/users/`

Parameters:

Name       | Type   | Required | Description
-----------|--------|----------|------------
username   | string | Yes      | The username for the new user.
password   | string | Yes      | The password for the new user account.
first_name | string | No       | The user's given name.
last_name  | string | No       | The user's family name.

*Note:*

- Not Authorization Protected

**Response**:

```json
Content-Type application/json
201 Created

{
  "id": "6d5f9bae-a31b-4b7b-82c4-3853eda2b011",
  "username": "richard",
  "first_name": "Richard",
  "last_name": "Hendriks",
}
```

The `id` should be used for further requests involving this user.


## Update User profile information

**Request**:

`PUT/PATCH` `/users/:id`

Parameters:

Name       | Type   | Description
-----------|--------|---
first_name | string | The first_name of the user object.
last_name  | string | The last_name of the user object.



*Note:*

- All parameters are optional
- **[Authorization Protected](authentication.md)**
- Superusers can update any user profile

**Response**:

```json
Content-Type application/json
200 OK

{
  "id": "6d5f9bae-a31b-4b7b-82c4-3853eda2b011",
  "username": "richard",
  "first_name": "Richard",
  "last_name": "Hendriks",
}
```

## Delete User

**Request**:

`DELETE` `/users/:id`

*Note:*

- **[Authorization Protected](authentication.md)**
- Superusers can delete any user profile

**Response**:

```json
204 No Content
```

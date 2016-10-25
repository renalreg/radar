# Security

### Login

Users login by making a `POST` request to `/login`:

```json
{
  "username": "admin",
  "password": "password"
}
```

When a correct username and password combination is entered, the user's ID (used to fetch the user's profile) and a session token are returned:

```json
{
  "token": "11.CTSSCQ.Dtd9nKB-b1fHNCfVyEvdRPKn2dE",
  "user_id": 2
}
```

Otherwise the server responds with a `422` status code:

```json
{
  "errors": {
    "username": [
      "Incorrect username or password."
    ]
  }
}
```

These values are stored in the browsers [local storage](https://developer.mozilla.org/en/docs/Web/API/Window/localStorage).

Users can be logged in from multiple browsers / machines. If "Logout Other Sessions?" is checked other sessions for this user will be logged out before the user is logged in.

```json
{
  "username": "admin",
  "password": "password",
  "logout_other_sessions": true
}
```

### Sessions

The user is given a session token when they login. The user's session ID and the current timestamp are signed with the `SECRET_KEY` (using [itsdangerous](http://pythonhosted.org/itsdangerous/)). Sessions expire after `SESSION_TIMEOUT` seconds (currently 15 minutes).

When a user makes a request they include the session token in the `X-Auth-Token` header:

```
X-Auth-Token: 11.CTSSCQ.Dtd9nKB-b1fHNCfVyEvdRPKn2dE
```

The response will also include a `X-Auth-Token` header which is a new session token valid for another `SESSION_TIMEOUT` seconds:

```
X-Auth-Token: 11.CTSS5Q._T--wJEtlEGxYJR-CqpATtfH64Y
```

The new session token should be used for subsequent requests (previous tokens will be still be valid until they expire).

The server checks the session token's signature to make sure it hasn't been tampered with and that it hasn't expired.
The session ID corresponds to a row in the `user_sessions` table.
When a user logs out their session is deleted.
When a user resets their password all of their user sessions are deleted.

### Logout

Users logout by making a `POST` request to `/logout`.

### Reset Password (Forgot Password)

The user sends a `POST` request to `/forgot-password` with their email address and username:

```json
{
  "username": "admin",
  "email": "admin@example.org"
}
```

If a user exists with that username and email they are sent an email with a URL to reset their password.
Otherwise the server responds with a `422` status code.

The URL contains a token which is randomly generated and then Base64 encoded.
The token is stored in `users.reset_password_token` with the date is was generated in `users.reset_password_date` (only one token is valid at a time).
The token expires after `RESET_PASSWORD_MAX_AGE` seconds (currently a day).

The reset password form asks for the user's username and new password. When the form is submitted a `POST` request is sent  to `/reset-password`:

```json
{
  "token": "2e_PYrccV7o3RTfVbIMcVT-9YiHIOGxAVOhs8J2B6p8=",
  "username": "admin",
  "password": "password1"
}
```

The token is checked against the stored token (`users.reset_password_token`) for the supplied username.
The token is invalid if more than `RESET_PASSWORD_MAX_AGE` seconds have passed since it was generated (`users.reset_password_date`).

On success the user's password is updated and any other active sessions for this user logged out.

### Forgot Username

The user sends a `POST` request to `/forgot-username`:

```json
{
  "email_address": "admin@example.org"
}
```

If a user(s) is found with the supplied email address they are sent an email with their username(s).

### Passwords

Password strength is checked using [zxcvbn](https://github.com/dropbox/zxcvbn).
Passwords are penalized if they include the user's username, email, first name or last name.
Passwords must have a strength of 3 (on a scale of 0-4).

### Change Password or Email

The user sends a `PUT` request to `/users/$ID`:

```json
{
  "id": 2,
  "current_password": "password",
  "password": "password1"
}
```

When updating their username or password the user must supply their current password (`current_password`).

### Force Password Change

Users can be forced to change their password by setting `users.force_password_change` to `true`
Until they change their password they are only allowed to access public API endpoints.

### Groups and Permissions

Each patient can belong to many organisations and cohorts.
An organisation is typically a hospital and a cohort is a group of patients in a study.

Users (doctors, nurses, researchers etc.) are assigned to organisations and cohorts.
They are also assigned a role within each group.
The role grants then permissions for that group.
For example being able to view patients who are in that group.

### Admins

There are a small number of users with admin rights (`users.is_admin`) who have all possible permissions.

### Patient Permissions

A user has permission on a patient if the user has the permission on one of the groups in the intersection of the user's and patient's groups.

The `VIEW_PATIENT` permission allows a user to view a patient and their data.
The `EDIT_PATIENT` permission allows them to also modify the patient's record
The `VIEW_DEMOGRAPHICS` permission allows the user to see the patient's demographics (name, DOB, identifiers etc) - this is mostly for users entering data.
There is a separate permission, `RECRUIT_PATIENT`, for adding new patients to RaDaR.

### User Permissions

Users can always view their own account.
If the user has the `VIEW_USER` permission they can view other users in their organisations and cohorts.

Some roles are able to add new users and assign users to groups.
Each role has a list of other roles that the user can assign to other users.

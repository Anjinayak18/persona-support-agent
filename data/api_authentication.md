# API Authentication

All API requests require a valid Bearer Token.

Example:

Authorization: Bearer YOUR_ACCESS_TOKEN

Common authentication failures:

* Missing Authorization header
* Expired token
* Invalid token
* Incorrect API endpoint

A 401 Unauthorized response indicates that the token is invalid or expired.

Recommended actions:

1. Verify token validity.
2. Generate a new token.
3. Confirm the Authorization header format.
4. Retry the request.

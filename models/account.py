"""Account models for Terraform Cloud API

This module contains models for Terraform Cloud account-related requests.
Response schemas are provided for documentation only and not used for validation.
"""

# Request Models
# Currently no request models needed for account endpoints

# Response Schemas (for documentation only, not used for validation)
"""
Response schema for GET /account/details:

{
  "data": {
    "id": "user-id",
    "type": "users",
    "attributes": {
      "username": "username",
      "is-service-account": false,
      "avatar-url": "https://example.com/avatar.jpg",
      "password": null,
      "enterprise-support": false,
      "is-admin": false,
      "is-site-admin": false,
      "is-sso-login": false,
      "is-unified": false,
      "two-factor": {
        "enabled": true,
        "verified": true
      },
      "email": "email@example.com",
      "unconfirmed-email": null,
      "has-git-hub-app-token": false,
      "is-confirmed": true,
      "is-sudo": false,
      "auth-method": "tfc",
      "has-linked-hcp": false,
      "permissions": {
        "can-create-organizations": true,
        "can-view-settings": true,
        "can-view-profile": true,
        "can-change-email": true,
        "can-change-username": true,
        "can-change-password": true,
        "can-manage-sessions": true,
        "can-manage-sso-identities": false,
        "can-manage-user-tokens": true,
        "can-update-user": true,
        "can-reenable-2fa-by-unlinking": true,
        "can-manage-hcp-account": false
      }
    },
    "relationships": {
      "authentication-tokens": {
        "links": {
          "related": "/api/v2/users/user-id/authentication-tokens"
        }
      },
      "github-app-oauth-tokens": {
        "links": {
          "related": "/api/v2/users/user-id/github-app-oauth-tokens"
        }
      },
      "authenticated-resource": {
        "data": {
          "id": "user-id",
          "type": "users"
        },
        "links": {
          "related": "/api/v2/users/user-id"
        }
      }
    },
    "links": {
      "self": "/api/v2/users/user-id"
    }
  }
}
"""

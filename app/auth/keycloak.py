from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from keycloak import KeycloakOpenID
from config import settings
from keycloak import (
    KeycloakGetError,
    KeycloakConnectionError,
    KeycloakAuthenticationError,
    KeycloakError
)
# Configure Keycloak client
keycloak_openid = KeycloakOpenID(
    server_url=settings.KEYCLOAK_SERVER_URL,
    client_id=settings.KEYCLOAK_CLIENT_ID,
    realm_name=settings.KEYCLOAK_REALM,
    client_secret_key=settings.KEYCLOAK_CLIENT_SECRET
)

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=f"{settings.KEYCLOAK_SERVER_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/auth",
    tokenUrl=f"{settings.KEYCLOAK_SERVER_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/token"
)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        # Decode and verify token
        token_info = keycloak_openid.decode_token(
            token,
            keycloak_openid.certs(),
            options={"verify_signature": True, "verify_aud": False}
        )
        return token_info
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def require_role(role: str):
    def role_checker(user: dict = Depends(get_current_user)):
        if role not in user.get("realm_access", {}).get("roles", []):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Missing required role: {role}"
            )
        return user
    return role_checker

# Specific role checkers
get_hr_user = require_role("hr")
get_candidate_user = require_role("candidate")
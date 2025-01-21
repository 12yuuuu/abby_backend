import jwt
from loguru import logger
from fastapi import Depends, HTTPException, Request

from src.core.schema import LoginUser
from src.core.setting import Setting, get_setting


async def get_ip(request: Request) -> str:
    """Get the client's IP address"""
    x_forwarded_for = request.headers.get("X-Forwarded-For", "")
    if x_forwarded_for.strip() != "":
        ips = x_forwarded_for.strip().split(",")
        return ips[0]
    else:
        return request.client.host


def get_login_user(
    request: Request,
    setting: Setting = Depends(get_setting),
) -> LoginUser:
    """Get the currently logged-in user"""
    token = request.headers.get("Authorization", "")
    if not token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = token[7:]

    try:
        decoded = jwt.decode(token, setting.jwt_key, algorithms=setting.jwt_algorithm)
    except jwt.InvalidKeyError:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Credentials expired")
    except Exception as e:
        logger.info("JWT decryption exception: {}", e)
        raise HTTPException(status_code=401, detail="Credential error")

    return LoginUser(tenant_id=decoded.get("tenantId"), user_id=decoded.get("userId"))

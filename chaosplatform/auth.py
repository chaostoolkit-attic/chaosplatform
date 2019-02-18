# -*- coding: utf-8 -*-
from typing import Any, Dict, Union
from uuid import UUID

from chaosplt_account.model import User
from flask import Flask, request, Request
from flask_login import LoginManager
from flask_jwt_extended import JWTManager, verify_jwt_in_request, \
    current_user as api_user, get_jti

__all__ = ["setup_jwt", "setup_login"]


def setup_jwt(app: Flask) -> JWTManager:
    jwt = JWTManager(app)

    @jwt.user_claims_loader
    def add_claims(identity: Union[UUID, str]) -> Dict[str, Any]:
        return {
            'user_id': str(identity)
        }

    @jwt.user_loader_callback_loader
    def user_loader(identity: Union[UUID, str]) -> User:
        return request.services.account.registration.get(identity)

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token: Dict[str, Any]) -> bool:
        """
        Check that the token is active

        When the token has been revoked or has been deleted, this returns
        `True` to indicate that the token should not be allowed.
        """
        user_id = decrypted_token["identity"]
        jti = decrypted_token["jti"]
        token = request.services.auth.access_token.get_by_jti(user_id, jti)
        if not token or token.revoked:
            return True
        return False

    return jwt


def setup_login(app: Flask, from_session: bool = False,
                from_jwt: bool = False) -> LoginManager:
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'github.login'

    if from_session:
        @login_manager.user_loader
        def load_user_from_session(user_id: Union[UUID, str]) -> User:
            return request.services.account.registration.get(user_id)

    if from_jwt:
        @login_manager.request_loader
        def load_user_from_request(request: Request):
            verify_jwt_in_request()
            return api_user

    return login_manager

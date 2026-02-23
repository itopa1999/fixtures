"""
Admin Command Classes
Business logic for admin operations
"""

from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from http import HTTPStatus
from rest_framework_simplejwt.tokens import RefreshToken
from utils.base_result import BaseResultWithData
from utils.log_helpers import OperationLogger
from utils.enums import GroupName



class LoginCommand:
    """Handle admin username/password login"""
    
    @staticmethod
    def Execute(username, password, request=None):
        """
        Authenticate admin user with username and password.
        
        Args:
            username (str): Username
            password (str): Password
            request: HTTP request object (optional)
                        
        Returns:
            BaseResultWithData: Result with token and user info
        """
        op = OperationLogger(
            "AdminLoginCommand",
            username=username
        )
        op.start()
        
        # Validate required fields
        if not username or not password:
            op.fail("Username and password are required")
            return BaseResultWithData(
                message="Username and password are required",
                status_code=HTTPStatus.BAD_REQUEST
            )
        
        # Authenticate user
        user = authenticate(username=username, password=password)
        
        if not user:
            op.fail(f"Invalid credentials for user {username}")
            return BaseResultWithData(
                message="Invalid username or password",
                status_code=HTTPStatus.UNAUTHORIZED
            )
        
        # Check if user is soft deleted
        if hasattr(user, 'is_deleted') and user.is_deleted:
            op.fail(f"User {username} has been deleted")
            return BaseResultWithData(
                message="User account not found",
                status_code=HTTPStatus.UNAUTHORIZED
            )
        
        if not user.is_active:
            op.fail(f"User {username} is inactive")
            return BaseResultWithData(
                message="User account is inactive",
                status_code=HTTPStatus.FORBIDDEN
            )
        
        # Check if user belongs to admin group
        user_groups = user.groups.values_list('name', flat=True)
        if GroupName.ADMIN.value not in user_groups:
            op.fail(f"User {username} does not belong to admin group")
            return BaseResultWithData(
                message="User does not have admin access",
                status_code=HTTPStatus.FORBIDDEN
            )
        
        # Generate token
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        
        # Get groups
        groups = [
            {
                'id': group.id,
                'name': group.name
            }
            for group in user.groups.all()
        ]
        
        op.success(f"Login successful for admin user {user.id}")
        
        return BaseResultWithData(
            message=f"Welcome back, {user.first_name or user.username}!",
            data={
                "access": access_token,
                "refresh": refresh_token,
                "email": user.email,
                "username": user.username,
                "name": f"{user.first_name} {user.last_name}".strip(),
                "id": user.id,
                "groups": groups
            },
            status_code=HTTPStatus.OK
        )

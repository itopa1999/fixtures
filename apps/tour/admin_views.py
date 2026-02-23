"""
Admin Views for Tournament Management
Custom admin endpoints for authentication and dashboard
"""

from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import AdminLoginSerializer
from .BLL.Commands.authCommand.admin_commands import LoginCommand


class AdminLoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = AdminLoginSerializer

    def post(self, request):
        
        # Validate request data
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')

        # Execute login command
        result = LoginCommand.Execute(
            username=username,
            password=password,
            request=request
        )
        
        # Create response
        response = Response(result.to_dict(), status=result.status_code)
        
        # Set cookies from result data
        if result.is_success:
            access_token = result.data.get('access')
            refresh_token = result.data.get('refresh')
            email = result.data.get('email')
            name = result.data.get('name')
            groups = result.data.get('groups', [])
            group_names = ','.join([g['name'] for g in groups]) if groups else ''
            
            response.set_cookie(
                'access', 
                value=access_token, 
                max_age=3600,  # 1 hour
                path='/', 
                samesite='Lax',
            )
            response.set_cookie(
                'refresh', 
                value=refresh_token, 
                max_age=2592000,  # 30 days
                path='/', 
                samesite='Lax',
            )
            response.set_cookie(
                'email', 
                value=email, 
                max_age=2592000, 
                path='/', 
                samesite='Lax',
            )
            response.set_cookie(
                'name', 
                value=name or '', 
                max_age=2592000, 
                path='/', 
                samesite='Lax',
            )
            response.set_cookie(
                'group', 
                value=group_names, 
                max_age=2592000, 
                path='/', 
                samesite='Lax',
            )
        
        return response
        


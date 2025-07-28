from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import uuid

# Simulación de base de datos local en memoria
data_list = []

# Añadiendo algunos datos de ejemplo para probar el GET
data_list.append({'id': str(uuid.uuid4()), 'name': 'User01', 'email': 'user01@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User02', 'email': 'user02@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User03', 'email': 'user03@example.com', 'is_active': False}) # Ejemplo de item inactivo

class DemoRestApi(APIView):
    name = "Demo REST API"

    def get(self, request):
        """
        GET /demo/rest/api/index/
        Retorna una lista de usuarios activos
        """
        # Filtra la lista para incluir solo los elementos donde 'is_active' es True
        active_items = [item for item in data_list if item.get('is_active', False)]
        
        return Response({
            'status': 'success',
            'data': active_items,
            'count': len(active_items)
        }, status=status.HTTP_200_OK)

    def post(self, request):
        """
        POST /demo/rest/api/
        Creates a new user record
        """
        # Extract request data
        data = request.data
        
        # Validate required fields
        errors = {}
        
        # Check for required name field
        name = data.get('name')
        if not name or (isinstance(name, str) and name.strip() == ''):
            errors['name'] = 'Name field is required and cannot be empty'
        
        # Check for required email field
        email = data.get('email')
        if not email or (isinstance(email, str) and email.strip() == ''):
            errors['email'] = 'Email field is required and cannot be empty'
        
        # If validation errors exist, return HTTP 400
        if errors:
            return Response({
                'status': 'error',
                'message': 'Validation failed',
                'errors': errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Generate UUID for new user and create user record
        new_user = {
            'id': str(uuid.uuid4()),
            'name': name.strip() if isinstance(name, str) else name,
            'email': email.strip() if isinstance(email, str) else email,
            'is_active': True
        }
        
        # Add user to data_list
        data_list.append(new_user)
        
        # Return HTTP 201 response with success message
        return Response({
            'status': 'success',
            'message': 'User created successfully',
            'data': new_user
        }, status=status.HTTP_201_CREATED)


class DemoRestApiItem(APIView):
    name = "Demo REST API Item"

    def _find_user_by_id(self, user_id):
        """
        Helper method to find user by ID in data_list
        Returns the user object if found, None otherwise
        """
        for user in data_list:
            if user.get('id') == user_id:
                return user
        return None

    def put(self, request, id):
        """
        PUT /demo/rest/api/<id>/
        Complete resource replacement - replaces all user fields except ID
        """
        # Validate that user ID exists in data_list
        user = self._find_user_by_id(id)
        if not user:
            return Response({
                'status': 'error',
                'message': f'User with ID {id} not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Extract request data
        data = request.data
        
        # Validate required fields in request body
        errors = {}
        
        # Check for required name field
        name = data.get('name')
        if not name or (isinstance(name, str) and name.strip() == ''):
            errors['name'] = 'Name field is required and cannot be empty'
        
        # Check for required email field
        email = data.get('email')
        if not email or (isinstance(email, str) and email.strip() == ''):
            errors['email'] = 'Email field is required and cannot be empty'
        
        # If validation errors exist, return HTTP 400
        if errors:
            return Response({
                'status': 'error',
                'message': 'Validation failed',
                'errors': errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Replace all user fields except ID with new data
        user['name'] = name.strip() if isinstance(name, str) else name
        user['email'] = email.strip() if isinstance(email, str) else email
        
        # Handle is_active field - if provided, use it; otherwise default to True
        is_active = data.get('is_active')
        if is_active is not None:
            user['is_active'] = bool(is_active)
        else:
            user['is_active'] = True
        
        # Return HTTP 200 with updated user data
        return Response({
            'status': 'success',
            'message': 'User updated successfully',
            'data': user
        }, status=status.HTTP_200_OK)

    def patch(self, request, id):
        """
        PATCH /demo/rest/api/<id>/
        Partial resource update - updates only provided fields while preserving unchanged fields
        """
        # Validate that user ID exists in data_list
        user = self._find_user_by_id(id)
        if not user:
            return Response({
                'status': 'error',
                'message': f'User with ID {id} not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Extract request data
        data = request.data
        
        # Validate provided fields (only validate fields that are present)
        errors = {}
        
        # Check name field if provided
        if 'name' in data:
            name = data.get('name')
            if not name or (isinstance(name, str) and name.strip() == ''):
                errors['name'] = 'Name field cannot be empty'
        
        # Check email field if provided
        if 'email' in data:
            email = data.get('email')
            if not email or (isinstance(email, str) and email.strip() == ''):
                errors['email'] = 'Email field cannot be empty'
        
        # If validation errors exist, return HTTP 400
        if errors:
            return Response({
                'status': 'error',
                'message': 'Validation failed',
                'errors': errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Update only provided fields while preserving unchanged fields
        if 'name' in data:
            user['name'] = data['name'].strip() if isinstance(data['name'], str) else data['name']
        
        if 'email' in data:
            user['email'] = data['email'].strip() if isinstance(data['email'], str) else data['email']
        
        if 'is_active' in data:
            user['is_active'] = bool(data['is_active'])
        
        # Return HTTP 200 with updated user data
        return Response({
            'status': 'success',
            'message': 'User updated successfully',
            'data': user
        }, status=status.HTTP_200_OK)

    def delete(self, request, id):
        """
        DELETE /demo/rest/api/<id>/
        Logical deletion - sets is_active to False
        """
        # Validate that user ID exists in data_list
        user = self._find_user_by_id(id)
        if not user:
            return Response({
                'status': 'error',
                'message': f'User with ID {id} not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Set is_active to False for logical deletion
        user['is_active'] = False
        
        # Return HTTP 200 with confirmation message
        return Response({
            'status': 'success',
            'message': f'User with ID {id} has been successfully deleted'
        }, status=status.HTTP_200_OK)


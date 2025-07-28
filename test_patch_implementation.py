#!/usr/bin/env python
"""
Test script to verify PATCH method implementation
"""
import os
import sys
import django
from django.conf import settings

# Add the project directory to Python path
sys.path.append('.')

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_data_server.settings')
django.setup()

from demo_rest_api.views import DemoRestApiItem, data_list
from rest_framework.test import APIRequestFactory
from rest_framework import status
import uuid

def test_patch_method():
    """Test the PATCH method implementation"""
    
    # Clear data_list and add test data
    data_list.clear()
    test_user_id = str(uuid.uuid4())
    test_user = {
        'id': test_user_id,
        'name': 'Original Name',
        'email': 'original@example.com',
        'is_active': True
    }
    data_list.append(test_user)
    
    # Create API request factory and view instance
    factory = APIRequestFactory()
    view = DemoRestApiItem()
    
    print("Testing PATCH method implementation...")
    print(f"Original user: {test_user}")
    
    # Test 1: Partial update with only name field
    print("\n1. Testing partial update (name only)...")
    request = factory.patch(f'/demo/rest/api/{test_user_id}/', {'name': 'Updated Name'}, format='json')
    response = view.patch(request, test_user_id)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.data}")
    print(f"Updated user in data_list: {data_list[0]}")
    
    assert response.status_code == status.HTTP_200_OK
    assert data_list[0]['name'] == 'Updated Name'
    assert data_list[0]['email'] == 'original@example.com'  # Should be preserved
    assert data_list[0]['is_active'] == True  # Should be preserved
    
    # Test 2: Partial update with only email field
    print("\n2. Testing partial update (email only)...")
    request = factory.patch(f'/demo/rest/api/{test_user_id}/', {'email': 'updated@example.com'}, format='json')
    response = view.patch(request, test_user_id)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.data}")
    print(f"Updated user in data_list: {data_list[0]}")
    
    assert response.status_code == status.HTTP_200_OK
    assert data_list[0]['name'] == 'Updated Name'  # Should be preserved from previous test
    assert data_list[0]['email'] == 'updated@example.com'
    assert data_list[0]['is_active'] == True  # Should be preserved
    
    # Test 3: Partial update with multiple fields
    print("\n3. Testing partial update (multiple fields)...")
    request = factory.patch(f'/demo/rest/api/{test_user_id}/', {
        'name': 'Final Name',
        'is_active': False
    }, format='json')
    response = view.patch(request, test_user_id)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.data}")
    print(f"Updated user in data_list: {data_list[0]}")
    
    assert response.status_code == status.HTTP_200_OK
    assert data_list[0]['name'] == 'Final Name'
    assert data_list[0]['email'] == 'updated@example.com'  # Should be preserved
    assert data_list[0]['is_active'] == False
    
    # Test 4: Non-existent ID
    print("\n4. Testing non-existent ID...")
    fake_id = str(uuid.uuid4())
    request = factory.patch(f'/demo/rest/api/{fake_id}/', {'name': 'Test'}, format='json')
    response = view.patch(request, fake_id)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.data}")
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert 'not found' in response.data['message'].lower()
    
    # Test 5: Empty field validation
    print("\n5. Testing empty field validation...")
    request = factory.patch(f'/demo/rest/api/{test_user_id}/', {'name': ''}, format='json')
    response = view.patch(request, test_user_id)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.data}")
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'name' in response.data.get('errors', {})
    
    # Test 6: Empty request body (should succeed - no changes)
    print("\n6. Testing empty request body...")
    request = factory.patch(f'/demo/rest/api/{test_user_id}/', {}, format='json')
    response = view.patch(request, test_user_id)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.data}")
    
    assert response.status_code == status.HTTP_200_OK
    # User should remain unchanged
    assert data_list[0]['name'] == 'Final Name'
    assert data_list[0]['email'] == 'updated@example.com'
    assert data_list[0]['is_active'] == False
    
    print("\n✅ All PATCH method tests passed!")

if __name__ == '__main__':
    test_patch_method()
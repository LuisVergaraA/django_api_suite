#!/usr/bin/env python3
"""
Simple test script to verify PATCH method implementation
"""
import sys
import os
import django
from django.conf import settings

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_data_server.settings')
django.setup()

from demo_rest_api.views import DemoRestApiItem, data_list
from rest_framework.test import APIRequestFactory
import uuid

def test_patch_method():
    """Test PATCH method functionality"""
    
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
    
    # Test 1: Partial update with name only
    print("\n1. Testing partial update (name only)...")
    request = factory.patch(f'/demo/rest/api/{test_user_id}/', {'name': 'Updated Name'}, format='json')
    request.data = {'name': 'Updated Name'}
    response = view.patch(request, test_user_id)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.data}")
    
    # Verify name was updated and email preserved
    updated_user = next((u for u in data_list if u['id'] == test_user_id), None)
    assert updated_user['name'] == 'Updated Name', "Name should be updated"
    assert updated_user['email'] == 'original@example.com', "Email should be preserved"
    assert response.status_code == 200, "Should return HTTP 200"
    
    # Test 2: Partial update with email only
    print("\n2. Testing partial update (email only)...")
    request = factory.patch(f'/demo/rest/api/{test_user_id}/', {'email': 'updated@example.com'}, format='json')
    request.data = {'email': 'updated@example.com'}
    response = view.patch(request, test_user_id)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.data}")
    
    # Verify email was updated and name preserved from previous update
    updated_user = next((u for u in data_list if u['id'] == test_user_id), None)
    assert updated_user['name'] == 'Updated Name', "Name should be preserved from previous update"
    assert updated_user['email'] == 'updated@example.com', "Email should be updated"
    assert response.status_code == 200, "Should return HTTP 200"
    
    # Test 3: Non-existent ID
    print("\n3. Testing non-existent ID...")
    fake_id = str(uuid.uuid4())
    request = factory.patch(f'/demo/rest/api/{fake_id}/', {'name': 'Test'}, format='json')
    request.data = {'name': 'Test'}
    response = view.patch(request, fake_id)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.data}")
    
    assert response.status_code == 404, "Should return HTTP 404 for non-existent ID"
    assert 'not found' in response.data['message'].lower(), "Should have descriptive error message"
    
    # Test 4: Empty field validation
    print("\n4. Testing empty field validation...")
    request = factory.patch(f'/demo/rest/api/{test_user_id}/', {'name': ''}, format='json')
    request.data = {'name': ''}
    response = view.patch(request, test_user_id)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.data}")
    
    assert response.status_code == 400, "Should return HTTP 400 for empty field"
    assert 'errors' in response.data, "Should include validation errors"
    
    print("\n✅ All PATCH method tests passed!")

if __name__ == '__main__':
    test_patch_method()
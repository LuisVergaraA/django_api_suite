from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
import json
import uuid

class DemoRestApiPostTestCase(APITestCase):
    
    def setUp(self):
        # Clear data_list before each test
        from demo_rest_api.views import data_list
        data_list.clear()
    
    def test_post_valid_user_creation(self):
        """Test POST method with valid name and email fields"""
        url = '/demo/rest/api/index/'
        data = {
            'name': 'Test User',
            'email': 'test@example.com'
        }
        
        response = self.client.post(url, data, format='json')
        
        # Should return HTTP 201
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check response structure
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['message'], 'User created successfully')
        self.assertIn('data', response.data)
        
        # Check user data
        user_data = response.data['data']
        self.assertEqual(user_data['name'], 'Test User')
        self.assertEqual(user_data['email'], 'test@example.com')
        self.assertTrue(user_data['is_active'])
        self.assertIn('id', user_data)
    
    def test_post_missing_name_field(self):
        """Test POST method without required name field"""
        url = '/demo/rest/api/index/'
        data = {
            'email': 'test@example.com'
        }
        
        response = self.client.post(url, data, format='json')
        
        # Should return HTTP 400
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'error')
        self.assertIn('name', response.data['errors'])
    
    def test_post_missing_email_field(self):
        """Test POST method without required email field"""
        url = '/demo/rest/api/index/'
        data = {
            'name': 'Test User'
        }
        
        response = self.client.post(url, data, format='json')
        
        # Should return HTTP 400
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'error')
        self.assertIn('email', response.data['errors'])
    
    def test_post_empty_name_field(self):
        """Test POST method with empty name field"""
        url = '/demo/rest/api/index/'
        data = {
            'name': '',
            'email': 'test@example.com'
        }
        
        response = self.client.post(url, data, format='json')
        
        # Should return HTTP 400
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'error')
        self.assertIn('name', response.data['errors'])
    
    def test_post_empty_email_field(self):
        """Test POST method with empty email field"""
        url = '/demo/rest/api/index/'
        data = {
            'name': 'Test User',
            'email': ''
        }
        
        response = self.client.post(url, data, format='json')
        
        # Should return HTTP 400
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'error')
        self.assertIn('email', response.data['errors'])


class DemoRestApiPutTestCase(APITestCase):
    
    def setUp(self):
        # Clear data_list before each test
        from demo_rest_api.views import data_list
        data_list.clear()
        
        # Add a test user to data_list
        self.test_user_id = str(uuid.uuid4())
        data_list.append({
            'id': self.test_user_id,
            'name': 'Original User',
            'email': 'original@example.com',
            'is_active': True
        })
    
    def test_put_valid_user_update(self):
        """Test PUT method with valid user data for complete replacement"""
        url = f'/demo/rest/api/index/{self.test_user_id}/'
        data = {
            'name': 'Updated User',
            'email': 'updated@example.com',
            'is_active': False
        }
        
        response = self.client.put(url, data, format='json')
        
        # Should return HTTP 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check response structure
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['message'], 'User updated successfully')
        self.assertIn('data', response.data)
        
        # Check updated user data
        user_data = response.data['data']
        self.assertEqual(user_data['id'], self.test_user_id)  # ID should remain unchanged
        self.assertEqual(user_data['name'], 'Updated User')
        self.assertEqual(user_data['email'], 'updated@example.com')
        self.assertFalse(user_data['is_active'])
    
    def test_put_nonexistent_user_id(self):
        """Test PUT method with non-existent user ID"""
        nonexistent_id = str(uuid.uuid4())
        url = f'/demo/rest/api/index/{nonexistent_id}/'
        data = {
            'name': 'Updated User',
            'email': 'updated@example.com'
        }
        
        response = self.client.put(url, data, format='json')
        
        # Should return HTTP 404
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['status'], 'error')
        self.assertIn('not found', response.data['message'].lower())
    
    def test_put_missing_name_field(self):
        """Test PUT method without required name field"""
        url = f'/demo/rest/api/index/{self.test_user_id}/'
        data = {
            'email': 'updated@example.com'
        }
        
        response = self.client.put(url, data, format='json')
        
        # Should return HTTP 400
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'error')
        self.assertIn('name', response.data['errors'])
    
    def test_put_missing_email_field(self):
        """Test PUT method without required email field"""
        url = f'/demo/rest/api/index/{self.test_user_id}/'
        data = {
            'name': 'Updated User'
        }
        
        response = self.client.put(url, data, format='json')
        
        # Should return HTTP 400
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'error')
        self.assertIn('email', response.data['errors'])
    
    def test_put_empty_name_field(self):
        """Test PUT method with empty name field"""
        url = f'/demo/rest/api/index/{self.test_user_id}/'
        data = {
            'name': '',
            'email': 'updated@example.com'
        }
        
        response = self.client.put(url, data, format='json')
        
        # Should return HTTP 400
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'error')
        self.assertIn('name', response.data['errors'])
    
    def test_put_empty_email_field(self):
        """Test PUT method with empty email field"""
        url = f'/demo/rest/api/index/{self.test_user_id}/'
        data = {
            'name': 'Updated User',
            'email': ''
        }
        
        response = self.client.put(url, data, format='json')
        
        # Should return HTTP 400
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'error')
        self.assertIn('email', response.data['errors'])
    
    def test_put_without_is_active_defaults_to_true(self):
        """Test PUT method without is_active field defaults to True"""
        url = f'/demo/rest/api/index/{self.test_user_id}/'
        data = {
            'name': 'Updated User',
            'email': 'updated@example.com'
        }
        
        response = self.client.put(url, data, format='json')
        
        # Should return HTTP 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that is_active defaults to True
        user_data = response.data['data']
        self.assertTrue(user_data['is_active'])


class DemoRestApiPatchTestCase(APITestCase):
    
    def setUp(self):
        # Clear data_list before each test
        from demo_rest_api.views import data_list
        data_list.clear()
        
        # Add a test user to data_list
        self.test_user_id = str(uuid.uuid4())
        data_list.append({
            'id': self.test_user_id,
            'name': 'Original User',
            'email': 'original@example.com',
            'is_active': True
        })
    
    def test_patch_partial_name_update(self):
        """Test PATCH method with only name field - should preserve other fields"""
        url = f'/demo/rest/api/index/{self.test_user_id}/'
        data = {
            'name': 'Updated Name Only'
        }
        
        response = self.client.patch(url, data, format='json')
        
        # Should return HTTP 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check response structure
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['message'], 'User updated successfully')
        self.assertIn('data', response.data)
        
        # Check updated user data - name should be updated, other fields preserved
        user_data = response.data['data']
        self.assertEqual(user_data['id'], self.test_user_id)  # ID should remain unchanged
        self.assertEqual(user_data['name'], 'Updated Name Only')
        self.assertEqual(user_data['email'], 'original@example.com')  # Should be preserved
        self.assertTrue(user_data['is_active'])  # Should be preserved
    
    def test_patch_partial_email_update(self):
        """Test PATCH method with only email field - should preserve other fields"""
        url = f'/demo/rest/api/index/{self.test_user_id}/'
        data = {
            'email': 'newemail@example.com'
        }
        
        response = self.client.patch(url, data, format='json')
        
        # Should return HTTP 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check updated user data - email should be updated, other fields preserved
        user_data = response.data['data']
        self.assertEqual(user_data['id'], self.test_user_id)  # ID should remain unchanged
        self.assertEqual(user_data['name'], 'Original User')  # Should be preserved
        self.assertEqual(user_data['email'], 'newemail@example.com')
        self.assertTrue(user_data['is_active'])  # Should be preserved
    
    def test_patch_partial_is_active_update(self):
        """Test PATCH method with only is_active field - should preserve other fields"""
        url = f'/demo/rest/api/index/{self.test_user_id}/'
        data = {
            'is_active': False
        }
        
        response = self.client.patch(url, data, format='json')
        
        # Should return HTTP 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check updated user data - is_active should be updated, other fields preserved
        user_data = response.data['data']
        self.assertEqual(user_data['id'], self.test_user_id)  # ID should remain unchanged
        self.assertEqual(user_data['name'], 'Original User')  # Should be preserved
        self.assertEqual(user_data['email'], 'original@example.com')  # Should be preserved
        self.assertFalse(user_data['is_active'])
    
    def test_patch_multiple_fields_update(self):
        """Test PATCH method with multiple fields"""
        url = f'/demo/rest/api/index/{self.test_user_id}/'
        data = {
            'name': 'Updated Name',
            'email': 'updated@example.com'
        }
        
        response = self.client.patch(url, data, format='json')
        
        # Should return HTTP 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check updated user data
        user_data = response.data['data']
        self.assertEqual(user_data['id'], self.test_user_id)  # ID should remain unchanged
        self.assertEqual(user_data['name'], 'Updated Name')
        self.assertEqual(user_data['email'], 'updated@example.com')
        self.assertTrue(user_data['is_active'])  # Should be preserved
    
    def test_patch_nonexistent_user_id(self):
        """Test PATCH method with non-existent user ID"""
        nonexistent_id = str(uuid.uuid4())
        url = f'/demo/rest/api/index/{nonexistent_id}/'
        data = {
            'name': 'Updated User'
        }
        
        response = self.client.patch(url, data, format='json')
        
        # Should return HTTP 404
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['status'], 'error')
        self.assertIn('not found', response.data['message'].lower())
    
    def test_patch_empty_name_field(self):
        """Test PATCH method with empty name field"""
        url = f'/demo/rest/api/index/{self.test_user_id}/'
        data = {
            'name': ''
        }
        
        response = self.client.patch(url, data, format='json')
        
        # Should return HTTP 400
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'error')
        self.assertIn('name', response.data['errors'])
    
    def test_patch_empty_email_field(self):
        """Test PATCH method with empty email field"""
        url = f'/demo/rest/api/index/{self.test_user_id}/'
        data = {
            'email': ''
        }
        
        response = self.client.patch(url, data, format='json')
        
        # Should return HTTP 400
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'error')
        self.assertIn('email', response.data['errors'])
    
    def test_patch_empty_request_body(self):
        """Test PATCH method with empty request body - should return success with no changes"""
        url = f'/demo/rest/api/index/{self.test_user_id}/'
        data = {}
        
        response = self.client.patch(url, data, format='json')
        
        # Should return HTTP 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that all fields remain unchanged
        user_data = response.data['data']
        self.assertEqual(user_data['id'], self.test_user_id)
        self.assertEqual(user_data['name'], 'Original User')
        self.assertEqual(user_data['email'], 'original@example.com')
        self.assertTrue(user_data['is_active'])


class DemoRestApiDeleteTestCase(APITestCase):
    
    def setUp(self):
        # Clear data_list before each test
        from demo_rest_api.views import data_list
        data_list.clear()
        
        # Add a test user to data_list
        self.test_user_id = str(uuid.uuid4())
        data_list.append({
            'id': self.test_user_id,
            'name': 'Test User',
            'email': 'test@example.com',
            'is_active': True
        })
    
    def test_delete_existing_user(self):
        """Test DELETE method with existing user ID - should set is_active to False"""
        url = f'/demo/rest/api/index/{self.test_user_id}/'
        
        response = self.client.delete(url)
        
        # Should return HTTP 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check response structure
        self.assertEqual(response.data['status'], 'success')
        self.assertIn('successfully deleted', response.data['message'])
        self.assertIn(self.test_user_id, response.data['message'])
        
        # Verify that user is logically deleted (is_active = False) in data_list
        from demo_rest_api.views import data_list
        deleted_user = None
        for user in data_list:
            if user['id'] == self.test_user_id:
                deleted_user = user
                break
        
        self.assertIsNotNone(deleted_user)
        self.assertFalse(deleted_user['is_active'])  # Should be set to False
        self.assertEqual(deleted_user['name'], 'Test User')  # Other fields should remain unchanged
        self.assertEqual(deleted_user['email'], 'test@example.com')
    
    def test_delete_nonexistent_user(self):
        """Test DELETE method with non-existent user ID"""
        nonexistent_id = str(uuid.uuid4())
        url = f'/demo/rest/api/index/{nonexistent_id}/'
        
        response = self.client.delete(url)
        
        # Should return HTTP 404
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['status'], 'error')
        self.assertIn('not found', response.data['message'].lower())
        self.assertIn(nonexistent_id, response.data['message'])
    
    def test_delete_already_inactive_user(self):
        """Test DELETE method on user that is already inactive"""
        # Set user to inactive first
        from demo_rest_api.views import data_list
        for user in data_list:
            if user['id'] == self.test_user_id:
                user['is_active'] = False
                break
        
        url = f'/demo/rest/api/index/{self.test_user_id}/'
        
        response = self.client.delete(url)
        
        # Should still return HTTP 200 (idempotent operation)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        self.assertIn('successfully deleted', response.data['message'])
        
        # Verify user is still inactive
        deleted_user = None
        for user in data_list:
            if user['id'] == self.test_user_id:
                deleted_user = user
                break
        
        self.assertIsNotNone(deleted_user)
        self.assertFalse(deleted_user['is_active'])
    
    def test_delete_user_not_shown_in_get_after_deletion(self):
        """Test that deleted user (is_active=False) is not returned in GET requests"""
        # First delete the user
        delete_url = f'/demo/rest/api/index/{self.test_user_id}/'
        delete_response = self.client.delete(delete_url)
        self.assertEqual(delete_response.status_code, status.HTTP_200_OK)
        
        # Then try to get all active users
        get_url = '/demo/rest/api/index/'
        get_response = self.client.get(get_url)
        
        # Should return HTTP 200 but with empty data (no active users)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(get_response.data['status'], 'success')
        self.assertEqual(get_response.data['count'], 0)
        self.assertEqual(len(get_response.data['data']), 0)
        
        # Verify that the deleted user is not in the returned data
        user_ids = [user['id'] for user in get_response.data['data']]
        self.assertNotIn(self.test_user_id, user_ids)


class DemoRestApiGetTestCase(APITestCase):
    
    def setUp(self):
        # Clear data_list before each test
        from demo_rest_api.views import data_list
        data_list.clear()
        
        # Add test users to data_list
        self.active_user_id = str(uuid.uuid4())
        self.inactive_user_id = str(uuid.uuid4())
        
        data_list.append({
            'id': self.active_user_id,
            'name': 'Active User',
            'email': 'active@example.com',
            'is_active': True
        })
        
        data_list.append({
            'id': self.inactive_user_id,
            'name': 'Inactive User',
            'email': 'inactive@example.com',
            'is_active': False
        })
    
    def test_get_returns_only_active_users(self):
        """Test GET method returns only users with is_active=True"""
        url = '/demo/rest/api/index/'
        
        response = self.client.get(url)
        
        # Should return HTTP 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check response structure
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(len(response.data['data']), 1)
        
        # Check that only active user is returned
        user_data = response.data['data'][0]
        self.assertEqual(user_data['id'], self.active_user_id)
        self.assertEqual(user_data['name'], 'Active User')
        self.assertTrue(user_data['is_active'])
        
        # Verify inactive user is not in results
        user_ids = [user['id'] for user in response.data['data']]
        self.assertNotIn(self.inactive_user_id, user_ids)
    
    def test_get_empty_list_when_no_active_users(self):
        """Test GET method returns empty list when no active users exist"""
        # Clear data_list and add only inactive users
        from demo_rest_api.views import data_list
        data_list.clear()
        
        data_list.append({
            'id': str(uuid.uuid4()),
            'name': 'Inactive User 1',
            'email': 'inactive1@example.com',
            'is_active': False
        })
        
        data_list.append({
            'id': str(uuid.uuid4()),
            'name': 'Inactive User 2',
            'email': 'inactive2@example.com',
            'is_active': False
        })
        
        url = '/demo/rest/api/index/'
        response = self.client.get(url)
        
        # Should return HTTP 200 with empty data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['count'], 0)
        self.assertEqual(len(response.data['data']), 0)


class DemoRestApiIntegrationTestCase(APITestCase):
    
    def setUp(self):
        # Clear data_list before each test
        from demo_rest_api.views import data_list
        data_list.clear()
    
    def test_full_crud_workflow(self):
        """Test complete CRUD workflow: Create -> Read -> Update -> Delete"""
        # 1. CREATE - POST a new user
        create_url = '/demo/rest/api/index/'
        create_data = {
            'name': 'Integration Test User',
            'email': 'integration@example.com'
        }
        
        create_response = self.client.post(create_url, create_data, format='json')
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        
        user_id = create_response.data['data']['id']
        
        # 2. READ - GET the created user
        get_url = '/demo/rest/api/index/'
        get_response = self.client.get(get_url)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(get_response.data['count'], 1)
        self.assertEqual(get_response.data['data'][0]['id'], user_id)
        
        # 3. UPDATE - PUT to update the user
        update_url = f'/demo/rest/api/index/{user_id}/'
        update_data = {
            'name': 'Updated Integration User',
            'email': 'updated_integration@example.com'
        }
        
        update_response = self.client.put(update_url, update_data, format='json')
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_response.data['data']['name'], 'Updated Integration User')
        
        # 4. PARTIAL UPDATE - PATCH to update only name
        patch_url = f'/demo/rest/api/index/{user_id}/'
        patch_data = {
            'name': 'Patched Integration User'
        }
        
        patch_response = self.client.patch(patch_url, patch_data, format='json')
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_response.data['data']['name'], 'Patched Integration User')
        self.assertEqual(patch_response.data['data']['email'], 'updated_integration@example.com')  # Should be preserved
        
        # 5. DELETE - DELETE the user (logical deletion)
        delete_url = f'/demo/rest/api/index/{user_id}/'
        delete_response = self.client.delete(delete_url)
        self.assertEqual(delete_response.status_code, status.HTTP_200_OK)
        
        # 6. VERIFY DELETION - GET should return empty list
        final_get_response = self.client.get(get_url)
        self.assertEqual(final_get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(final_get_response.data['count'], 0)
    
    def test_multiple_users_management(self):
        """Test managing multiple users simultaneously"""
        # Create multiple users
        users_data = [
            {'name': 'User 1', 'email': 'user1@example.com'},
            {'name': 'User 2', 'email': 'user2@example.com'},
            {'name': 'User 3', 'email': 'user3@example.com'}
        ]
        
        created_user_ids = []
        create_url = '/demo/rest/api/index/'
        
        for user_data in users_data:
            response = self.client.post(create_url, user_data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            created_user_ids.append(response.data['data']['id'])
        
        # Verify all users are returned in GET
        get_response = self.client.get(create_url)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(get_response.data['count'], 3)
        
        returned_user_ids = [user['id'] for user in get_response.data['data']]
        for user_id in created_user_ids:
            self.assertIn(user_id, returned_user_ids)
        
        # Delete one user and verify count decreases
        delete_url = f'/demo/rest/api/index/{created_user_ids[0]}/'
        delete_response = self.client.delete(delete_url)
        self.assertEqual(delete_response.status_code, status.HTTP_200_OK)
        
        # Verify only 2 active users remain
        final_get_response = self.client.get(create_url)
        self.assertEqual(final_get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(final_get_response.data['count'], 2)
        
        # Verify deleted user is not in results
        final_user_ids = [user['id'] for user in final_get_response.data['data']]
        self.assertNotIn(created_user_ids[0], final_user_ids)
    
    def test_uuid_generation_uniqueness(self):
        """Test that UUID generation creates unique IDs for different users"""
        create_url = '/demo/rest/api/index/'
        user_data = {
            'name': 'Test User',
            'email': 'test@example.com'
        }
        
        # Create multiple users with same data
        created_ids = []
        for i in range(5):
            response = self.client.post(create_url, user_data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            created_ids.append(response.data['data']['id'])
        
        # Verify all IDs are unique
        self.assertEqual(len(created_ids), len(set(created_ids)))
        
        # Verify all IDs are valid UUIDs (basic format check)
        for user_id in created_ids:
            self.assertIsInstance(user_id, str)
            self.assertEqual(len(user_id), 36)  # Standard UUID string length
            self.assertEqual(user_id.count('-'), 4)  # Standard UUID has 4 hyphens


class DemoRestApiValidationTestCase(APITestCase):
    
    def setUp(self):
        # Clear data_list before each test
        from demo_rest_api.views import data_list
        data_list.clear()
        
        # Add a test user for update/patch/delete tests
        self.test_user_id = str(uuid.uuid4())
        data_list.append({
            'id': self.test_user_id,
            'name': 'Test User',
            'email': 'test@example.com',
            'is_active': True
        })
    
    def test_post_with_null_values(self):
        """Test POST method with null values"""
        url = '/demo/rest/api/index/'
        data = {
            'name': None,
            'email': 'test@example.com'
        }
        
        response = self.client.post(url, data, format='json')
        
        # Should return HTTP 400
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'error')
        self.assertIn('name', response.data['errors'])
    
    def test_post_with_whitespace_only_fields(self):
        """Test POST method with whitespace-only fields"""
        url = '/demo/rest/api/index/'
        data = {
            'name': '   ',
            'email': 'test@example.com'
        }
        
        response = self.client.post(url, data, format='json')
        
        # Should return HTTP 400
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'error')
        self.assertIn('name', response.data['errors'])
    
    def test_put_with_null_values(self):
        """Test PUT method with null values"""
        url = f'/demo/rest/api/index/{self.test_user_id}/'
        data = {
            'name': None,
            'email': 'updated@example.com'
        }
        
        response = self.client.put(url, data, format='json')
        
        # Should return HTTP 400
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'error')
        self.assertIn('name', response.data['errors'])
    
    def test_patch_with_null_values(self):
        """Test PATCH method with null values"""
        url = f'/demo/rest/api/index/{self.test_user_id}/'
        data = {
            'name': None
        }
        
        response = self.client.patch(url, data, format='json')
        
        # Should return HTTP 400
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'error')
        self.assertIn('name', response.data['errors'])
    
    def test_data_trimming_on_create(self):
        """Test that whitespace is trimmed from fields during creation"""
        url = '/demo/rest/api/index/'
        data = {
            'name': '  Test User  ',
            'email': '  test@example.com  '
        }
        
        response = self.client.post(url, data, format='json')
        
        # Should return HTTP 201
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check that whitespace was trimmed
        user_data = response.data['data']
        self.assertEqual(user_data['name'], 'Test User')
        self.assertEqual(user_data['email'], 'test@example.com')
    
    def test_data_trimming_on_update(self):
        """Test that whitespace is trimmed from fields during updates"""
        url = f'/demo/rest/api/index/{self.test_user_id}/'
        data = {
            'name': '  Updated User  ',
            'email': '  updated@example.com  '
        }
        
        response = self.client.put(url, data, format='json')
        
        # Should return HTTP 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that whitespace was trimmed
        user_data = response.data['data']
        self.assertEqual(user_data['name'], 'Updated User')
        self.assertEqual(user_data['email'], 'updated@example.com')
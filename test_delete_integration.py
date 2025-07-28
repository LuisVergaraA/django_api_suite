#!/usr/bin/env python
"""
Integration test to verify DELETE method works with GET filtering
"""
import os
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_data_server.settings')

import django
django.setup()

from rest_framework import status

# Import after Django setup
from demo_rest_api.views import data_list, DemoRestApi, DemoRestApiItem

class TestDeleteIntegration:
    def __init__(self):
        pass
        
    def setup_test_data(self):
        """Setup test data"""
        # Clear existing data
        data_list.clear()
        
        # Add test users
        test_users = [
            {
                'id': 'user-1',
                'name': 'User 1',
                'email': 'user1@example.com',
                'is_active': True
            },
            {
                'id': 'user-2',
                'name': 'User 2',
                'email': 'user2@example.com',
                'is_active': True
            }
        ]
        
        for user in test_users:
            data_list.append(user)
        
        return test_users
        
    def test_delete_and_get_integration(self):
        """Test that deleted users don't appear in GET requests"""
        print("Testing DELETE and GET integration...")
        
        # Setup test data
        test_users = self.setup_test_data()
        
        # Create view instances
        collection_view = DemoRestApi()
        item_view = DemoRestApiItem()
        
        # Create mock request object
        class MockRequest:
            def __init__(self):
                self.data = {}
        
        request = MockRequest()
        
        # First, verify both users appear in GET request
        response = collection_view.get(request)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 2
        assert len(response.data['data']) == 2
        print("✅ Initial GET shows 2 active users")
        
        # Delete one user
        delete_response = item_view.delete(request, 'user-1')
        assert delete_response.status_code == status.HTTP_200_OK
        print("✅ User 1 deleted successfully")
        
        # Verify only one user appears in GET request now
        response = collection_view.get(request)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
        assert len(response.data['data']) == 1
        assert response.data['data'][0]['id'] == 'user-2'
        print("✅ GET now shows only 1 active user (user-2)")
        
        # Verify the deleted user still exists in data_list but is inactive
        deleted_user = item_view._find_user_by_id('user-1')
        assert deleted_user is not None
        assert deleted_user['is_active'] == False
        print("✅ Deleted user still exists in data_list but is_active=False")
        
        print("✅ DELETE and GET integration test passed")
        
    def run_tests(self):
        """Run all tests"""
        print("Running DELETE integration tests...\n")
        
        try:
            self.test_delete_and_get_integration()
            print("\n🎉 All DELETE integration tests passed!")
            return True
        except Exception as e:
            print(f"\n❌ Test failed: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    tester = TestDeleteIntegration()
    success = tester.run_tests()
    sys.exit(0 if success else 1)
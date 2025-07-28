# Design Document

## Overview

This design extends the existing Django REST API demo application to support full CRUD operations. The current implementation uses an in-memory data structure (`data_list`) to simulate a database and only supports GET operations. We will enhance this by adding POST, PUT, PATCH, and DELETE methods while maintaining the existing architecture pattern.

The design follows RESTful principles and Django REST Framework conventions, using class-based API views for clean separation of HTTP method handling.

## Architecture

### Current Architecture
- Django 5.2.4 with Django REST Framework 3.16.0
- Class-based APIView (`DemoRestApi`) for handling requests
- In-memory data storage using Python list (`data_list`)
- UUID-based unique identifiers for user records
- Logical deletion using `is_active` flag

### Enhanced Architecture
The design will extend the current architecture with:
- Additional view class (`DemoRestApiItem`) for individual resource operations
- Enhanced validation and error handling
- Proper HTTP status code responses
- RESTful URL routing for both collection and individual resources

## Components and Interfaces

### View Classes

#### DemoRestApi (Collection Endpoint)
- **Purpose**: Handle operations on the user collection
- **URL Pattern**: `/demo/rest/api/`
- **Methods**:
  - `GET`: List active users (existing functionality)
  - `POST`: Create new user

#### DemoRestApiItem (Individual Resource Endpoint)
- **Purpose**: Handle operations on individual user resources
- **URL Pattern**: `/demo/rest/api/<str:id>/`
- **Methods**:
  - `PUT`: Complete resource replacement
  - `PATCH`: Partial resource update
  - `DELETE`: Logical deletion

### URL Routing Structure
```
/demo/rest/api/                 -> DemoRestApi (collection operations)
/demo/rest/api/<str:id>/        -> DemoRestApiItem (individual resource operations)
```

### Data Structure
The existing `data_list` will continue to serve as the in-memory database with the following user record structure:
```python
{
    'id': str,          # UUID4 string
    'name': str,        # Required field
    'email': str,       # Required field
    'is_active': bool   # Default True, False for logical deletion
}
```

## Data Models

### User Record Schema
- **id**: String (UUID4) - Unique identifier, auto-generated
- **name**: String - Required field for user's name
- **email**: String - Required field for user's email
- **is_active**: Boolean - Default True, used for logical deletion

### Request/Response Formats

#### POST Request Body
```json
{
    "name": "string",
    "email": "string"
}
```

#### PUT Request Body
```json
{
    "name": "string",
    "email": "string",
    "is_active": boolean
}
```

#### PATCH Request Body (partial)
```json
{
    "name": "string"  // or any subset of updatable fields
}
```

#### Success Response Format
```json
{
    "status": "success",
    "message": "descriptive message",
    "data": { /* user object */ }
}
```

#### Error Response Format
```json
{
    "status": "error",
    "message": "descriptive error message",
    "errors": { /* field-specific errors if applicable */ }
}
```

## Error Handling

### Validation Errors (HTTP 400)
- Missing required fields (name, email)
- Invalid data types
- Empty or null values for required fields

### Not Found Errors (HTTP 404)
- Attempting to access non-existent user ID
- Attempting to modify already deleted (inactive) users

### Success Responses
- **HTTP 200**: Successful GET, PUT, PATCH, DELETE operations
- **HTTP 201**: Successful POST (resource creation)

### Error Response Strategy
1. Validate request data before processing
2. Check resource existence for individual operations
3. Return appropriate HTTP status codes
4. Provide descriptive error messages
5. Include field-specific validation errors when applicable

## Testing Strategy

### Unit Testing Approach
1. **Method-level testing**: Test each HTTP method independently
2. **Validation testing**: Test all validation scenarios
3. **Error handling testing**: Test error conditions and status codes
4. **Data integrity testing**: Verify data consistency after operations

### Test Categories

#### POST Method Tests
- Valid user creation
- Missing name field validation
- Missing email field validation
- Verify UUID generation
- Verify is_active default value

#### PUT Method Tests
- Complete resource replacement
- Non-existent ID handling
- Required field validation
- Data preservation verification

#### PATCH Method Tests
- Partial field updates
- Unchanged field preservation
- Non-existent ID handling
- Empty request body handling

#### DELETE Method Tests
- Logical deletion (is_active = False)
- Non-existent ID handling
- Verify exclusion from GET requests
- Confirmation message verification

#### Integration Tests
- End-to-end workflow testing
- URL routing verification
- HTTP status code validation
- Response format consistency

### Test Data Management
- Use separate test data structures to avoid interference
- Reset data state between tests
- Use predictable UUIDs for testing when needed

## Implementation Considerations

### Code Organization
- Maintain existing code structure and patterns
- Add new functionality without breaking existing GET operations
- Use consistent naming conventions
- Follow Django REST Framework best practices

### Performance Considerations
- In-memory operations are fast for demo purposes
- Linear search for ID lookups is acceptable for small datasets
- Consider indexing strategies if scaling beyond demo scope

### Security Considerations
- Input validation for all user-provided data
- Proper HTTP method restrictions
- CSRF protection (handled by Django middleware)
- No sensitive data exposure in error messages

### Maintainability
- Clear separation of concerns between view classes
- Consistent error handling patterns
- Comprehensive documentation and comments
- Modular validation functions
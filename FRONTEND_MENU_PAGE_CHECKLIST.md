# Frontend Menu.Page Implementation Checklist

This checklist helps verify that the menu.page frontend is properly implemented with authentication for order submission.

## 1. API Service Implementation (`src/api.js`)

### Authentication Functions
- [ ] `login(username, password)` function exists
- [ ] Login function properly sends credentials to `/api/auth/login`
- [ ] Login function stores token in localStorage/sessionStorage
- [ ] Login function sets token expiration time
- [ ] `isTokenValid()` function exists to check token validity
- [ ] `ensureAuth()` function exists to handle authentication

### Order Submission Functions
- [ ] `submitOrder(orderData)` function exists
- [ ] Submit order function calls `ensureAuth()` before submission
- [ ] Submit order function includes Authorization header with Bearer token
- [ ] Submit order function properly formats order data
- [ ] Submit order function handles success and error responses

### Helper Functions
- [ ] `getAuthHeaders()` function exists
- [ ] Auth headers function includes Content-Type header
- [ ] Auth headers function includes Authorization header when token exists
- [ ] Auth headers function handles cases where no token exists

## 2. Menu.Page Component Implementation

### State Management
- [ ] Component maintains cart state
- [ ] Component maintains customer information state
- [ ] Component maintains loading/submission state
- [ ] Component maintains error state

### Event Handlers
- [ ] Checkout handler calls `submitOrder()` function
- [ ] Checkout handler properly formats order data
- [ ] Checkout handler handles success response
- [ ] Checkout handler handles error response
- [ ] Checkout handler sets loading state during submission

### UI Elements
- [ ] Display error messages when authentication/order submission fails
- [ ] Disable checkout button when cart is empty
- [ ] Show loading indicator during authentication/submission
- [ ] Clear cart after successful order submission

## 3. Configuration Files

### Vite Configuration (`vite.config.js`)
- [ ] Proxy configuration exists for `/api` routes
- [ ] Proxy target set to `http://localhost:8088`
- [ ] Proxy has `changeOrigin: true`
- [ ] Proxy has `secure: false` (for development)

### Package.json
- [ ] Proxy configuration exists (alternative to vite.config.js)
- [ ] Development dependencies include required packages

## 4. Authentication Flow Verification

### Token Storage
- [ ] Token stored in localStorage or sessionStorage
- [ ] Token expiration time stored
- [ ] Token properly retrieved when making requests

### Token Usage
- [ ] Authorization header includes Bearer token
- [ ] Token refreshed or re-authentication occurs when token expires
- [ ] Proper handling of expired tokens

### Error Handling
- [ ] 401 errors during order submission trigger re-authentication
- [ ] Clear error messages displayed to user
- [ ] Error logging in console for debugging

## 5. Data Format Verification

### Order Data Structure
- [ ] Order data includes `order` array with item objects
- [ ] Each item has `name`, `price`, `category`, and `modifiers`
- [ ] Order data includes `total` field
- [ ] Order data includes `customer_name`
- [ ] Order data includes `payment_type`
- [ ] Order data includes other required fields

### Customer Information
- [ ] Customer name properly collected
- [ ] Customer phone properly collected (if required)
- [ ] Payment type properly selected

## 6. Testing Steps

### Manual Testing
- [ ] Verify login works and token is stored
- [ ] Verify order submission works with valid authentication
- [ ] Verify error handling for network issues
- [ ] Verify error handling for authentication failures
- [ ] Verify error handling for validation errors

### Browser Developer Tools
- [ ] Check Network tab for successful authentication requests
- [ ] Check Network tab for successful order submission requests
- [ ] Verify Authorization headers are present
- [ ] Check Console for any JavaScript errors

### Local Storage
- [ ] Verify token is stored after login
- [ ] Verify token expiration is stored
- [ ] Verify token is used in requests

## 7. Common Issues to Check

### Authentication Issues
- [ ] Token not being stored after login
- [ ] Token expiration not being checked
- [ ] Expired tokens not being refreshed
- [ ] Authorization header missing from requests

### Data Format Issues
- [ ] Order data not properly formatted
- [ ] Required fields missing from order data
- [ ] Incorrect data types in order data

### Configuration Issues
- [ ] Proxy configuration incorrect
- [ ] CORS issues with backend
- [ ] Base URL incorrect in API calls

### Error Handling Issues
- [ ] Errors not properly caught and displayed
- [ ] No user feedback on failures
- [ ] No logging for debugging

## 8. Verification Commands

### Test Authentication
```javascript
// In browser console
localStorage.clear(); // Clear any existing tokens
// Try to login and check if token is stored
```

### Test Order Submission
```javascript
// In browser console
// Check if token exists and is valid
console.log('Token:', localStorage.getItem('authToken'));
console.log('Valid:', isTokenValid()); // If this function exists

// Try to submit a test order
```

### Check Network Requests
1. Open Developer Tools (F12)
2. Go to Network tab
3. Attempt checkout in menu.page
4. Check requests to `/api/orders/`
5. Verify Authorization header is present
6. Check response status and content

## 9. Debugging Tools

### Browser Console Commands
```javascript
// Check token storage
console.log('Auth Token:', localStorage.getItem('authToken'));
console.log('Token Expiry:', localStorage.getItem('tokenExpiry'));

// Test token validity (if function exists)
console.log('Token Valid:', isTokenValid());

// Clear authentication for testing
localStorage.removeItem('authToken');
localStorage.removeItem('tokenExpiry');
```

### Network Analysis
- Request URL: `http://localhost:8088/api/orders/`
- Request Method: `POST`
- Request Headers should include:
  - `Content-Type: application/json`
  - `Authorization: Bearer [token]`
- Request Body should be properly formatted JSON

## 10. Success Criteria

- [ ] User can add items to cart
- [ ] User can proceed to checkout
- [ ] Authentication happens automatically if needed
- [ ] Order is successfully submitted to backend
- [ ] Success message displayed to user
- [ ] Cart is cleared after successful submission
- [ ] No 401 authentication errors
- [ ] Proper error handling for all failure cases

Complete this checklist to ensure your menu.page frontend is properly implemented with authentication.
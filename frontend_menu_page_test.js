/**
 * Frontend Menu.Page Authentication and Order Submission Test
 * This script simulates what the React frontend should be doing
 * to properly authenticate and submit orders
 */

// Configuration
const BASE_URL = 'http://localhost:8088';
const API_PREFIX = '/api';

// State
let authToken = null;
let tokenExpiry = null;

// Utility functions
function log(message, isSuccess = true) {
    const timestamp = new Date().toISOString();
    const status = isSuccess ? '✓' : '✗';
    console.log(`[${timestamp}] ${status} ${message}`);
}

// Authentication functions
async function login(username = 'manager@example.com', password = 'manager123') {
    try {
        log(`Attempting to login as ${username}...`);
        const response = await fetch(`${BASE_URL}${API_PREFIX}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                username: username,
                password: password,
            }),
        });
        
        if (response.ok) {
            const data = await response.json();
            authToken = data.access_token;
            
            // Set token expiry (60 minutes from now)
            tokenExpiry = new Date();
            tokenExpiry.setMinutes(tokenExpiry.getMinutes() + 59);
            
            log(`Login successful. Token: ${authToken.substring(0, 20)}...`);
            return true;
        } else {
            const errorText = await response.text();
            log(`Login failed with status ${response.status}: ${errorText}`, false);
            return false;
        }
    } catch (error) {
        log(`Login failed with error: ${error.message}`, false);
        return false;
    }
}

function isTokenValid() {
    if (!authToken || !tokenExpiry) return false;
    return new Date() < new Date(tokenExpiry);
}

async function ensureAuth() {
    if (!isTokenValid()) {
        log('Token invalid or missing, authenticating...', false);
        return await login();
    }
    return true;
}

// Order submission function
async function submitOrder(orderData) {
    // Ensure we have valid authentication
    const authSuccess = await ensureAuth();
    if (!authSuccess) {
        throw new Error('Authentication failed');
    }
    
    try {
        log('Submitting order...');
        const response = await fetch(`${BASE_URL}${API_PREFIX}/orders/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify(orderData),
        });
        
        if (response.ok) {
            const order = await response.json();
            log(`Order submitted successfully. Order ID: ${order.id}`);
            return order;
        } else {
            const errorText = await response.text();
            log(`Failed to submit order. Status: ${response.status} - ${errorText}`, false);
            throw new Error(`Failed to submit order: ${response.statusText}`);
        }
    } catch (error) {
        log(`Error submitting order: ${error.message}`, false);
        throw error;
    }
}

// Test functions
async function testMenuPageCheckout() {
    console.log('=== Menu.Page Checkout Test ===');
    
    // Test login
    const loginSuccess = await login();
    if (!loginSuccess) {
        log('Cannot proceed without successful login', false);
        return;
    }
    
    // Test order submission
    try {
        // Sample order data (similar to what menu.page would send)
        const sampleOrder = {
            order: [
                {
                    name: "Cheeseburger",
                    price: 8.99,
                    category: "Main Course",
                    modifiers: ["Extra Cheese", "No Onion"]
                },
                {
                    name: "French Fries",
                    price: 3.99,
                    category: "Sides",
                    modifiers: []
                }
            ],
            total: 12.98,
            customer_name: "Test Customer",
            customer_phone: "555-1234",
            payment_type: "cash",
            order_type: "dine_in"
        };
        
        const order = await submitOrder(sampleOrder);
        log('Menu.Page checkout test completed successfully');
        log(`Order details: ID=${order.id}, Total=$${order.total}, Status=${order.status}`);
    } catch (error) {
        log(`Menu.Page checkout test failed: ${error.message}`, false);
    }
    
    console.log('=== Test Complete ===');
}

// Run the test
testMenuPageCheckout().catch(error => {
    log(`Test failed with unhandled error: ${error.message}`, false);
});

// Export functions for potential use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        login,
        submitOrder,
        testMenuPageCheckout,
        isTokenValid,
        ensureAuth
    };
}
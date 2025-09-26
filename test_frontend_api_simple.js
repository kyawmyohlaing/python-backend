/**
 * Simple JavaScript test for sales reports API
 * This mimics what the React frontend should be doing
 */

// Configuration
const BASE_URL = 'http://localhost:8088';
const API_PREFIX = '/api';

// State
let authToken = null;

// Utility functions
function log(message, isSuccess = true) {
    const timestamp = new Date().toISOString();
    const status = isSuccess ? '✓' : '✗';
    console.log(`[${timestamp}] ${status} ${message}`);
}

async function login() {
    try {
        log('Attempting to login...');
        const response = await fetch(`${BASE_URL}${API_PREFIX}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: 'username=manager&password=manager123'
        });
        
        if (response.ok) {
            const data = await response.json();
            authToken = data.access_token;
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

async function fetchDailySalesReport() {
    if (!authToken) {
        log('No auth token available. Please login first.', false);
        throw new Error('Not authenticated');
    }
    
    try {
        log('Fetching daily sales report...');
        const response = await fetch(`${BASE_URL}${API_PREFIX}/analytics/reports/daily`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${authToken}`,
                'Content-Type': 'application/json',
            }
        });
        
        if (response.ok) {
            const data = await response.json();
            log(`Daily sales report retrieved successfully`);
            log(`Period: ${data.period}`);
            log(`Total sales: ${data.total_sales}`);
            log(`Total orders: ${data.total_orders}`);
            log(`Sales data points: ${data.sales_data.length}`);
            return data;
        } else {
            const errorText = await response.text();
            log(`Failed to fetch daily sales report. Status: ${response.status} - ${errorText}`, false);
            throw new Error(`Failed to fetch daily sales report: ${response.statusText}`);
        }
    } catch (error) {
        log(`Error fetching daily sales report: ${error.message}`, false);
        throw error;
    }
}

async function testCompleteFlow() {
    console.log('=== Sales Reports API Test ===');
    
    // Login
    const loginSuccess = await login();
    if (!loginSuccess) {
        log('Cannot proceed without successful login', false);
        return;
    }
    
    // Test daily report
    try {
        const dailyReport = await fetchDailySalesReport();
        log('Daily report test completed successfully');
    } catch (error) {
        log(`Daily report test failed: ${error.message}`, false);
    }
    
    console.log('=== Test Complete ===');
}

// Run the test
testCompleteFlow().catch(error => {
    log(`Test failed with unhandled error: ${error.message}`, false);
});

// Export functions for potential use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        login,
        fetchDailySalesReport,
        testCompleteFlow
    };
}
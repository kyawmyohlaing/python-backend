# How to Fix Authentication Issues

This document explains how to identify and fix the 401 authentication error during menu.page checkout.

## Problem Analysis

From the error logs, we can see:
1. The retry mechanism is working correctly (prevents infinite loops)
2. The re-authentication is being attempted but failing with 401 errors
3. This indicates that the stored credentials are invalid

## Solution Steps

### Step 1: Diagnose the Issue

1. Open the browser's developer console (F12)
2. Run the diagnostic command:
   ```javascript
   fixAuthIssue()
   ```

This will check:
- Current token validity
- Stored credentials
- Attempt re-authentication with stored credentials

### Step 2: If Diagnosis Shows Invalid Credentials

If the diagnosis shows that the stored credentials are invalid:

1. Run the reset command:
   ```javascript
   resetAndFixAuth()
   ```

2. Reload the page (Ctrl+R or Cmd+R)

3. Log in through the normal login page

4. Try submitting your order again

### Step 3: Manual Verification

If the automated tools don't resolve the issue:

1. Check localStorage contents:
   ```javascript
   console.log('Token:', localStorage.getItem('token'));
   console.log('Credentials:', localStorage.getItem('authCredentials'));
   console.log('User:', localStorage.getItem('user'));
   ```

2. Clear authentication data manually:
   ```javascript
   localStorage.removeItem('token');
   localStorage.removeItem('authCredentials');
   localStorage.removeItem('user');
   ```

3. Reload the page and log in again

## Common Causes and Solutions

### Cause 1: Invalid Stored Credentials
**Symptoms**: Re-authentication fails with 401 error
**Solution**: 
1. Run `resetAndFixAuth()`
2. Reload the page
3. Log in again

### Cause 2: Backend Not Running
**Symptoms**: Network errors or unable to connect
**Solution**: 
1. Ensure backend is running on http://localhost:8088
2. Check network connectivity

### Cause 3: User Account Issues
**Symptoms**: Login fails with correct credentials
**Solution**: 
1. Verify account is active
2. Contact system administrator

## Files Created for Fixing Issues

1. `fix_auth_issue.js` - Diagnose and attempt to fix auth issues
2. `reset_and_fix_auth.js` - Reset auth state and provide guidance
3. `HOW_TO_FIX_AUTH_ISSUES.md` - This documentation

## Verification

After following the steps:
1. The 401 authentication error should be resolved
2. Orders should submit successfully
3. Automatic re-authentication should work when tokens expire

## Prevention

To prevent future issues:
1. Regularly check that user accounts are active
2. Ensure backend services are running
3. Use strong, secure passwords
4. Log out and log back in periodically to refresh credentials
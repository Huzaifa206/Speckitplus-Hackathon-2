# Debugging Steps for CRUD Operations Issue

## Current Status
- ✅ Chatbot can add tasks
- ❌ Delete and Update operations return 401 Unauthorized error

## Root Cause
The 401 error indicates that the authentication token is either:
1. Not being sent with the request
2. Invalid or expired
3. Not being properly validated by the backend

## Steps to Debug

### Step 1: Check if token exists in browser
1. Open browser DevTools (F12)
2. Go to Application tab → Local Storage
3. Look for `auth_token` key
4. Copy the token value

### Step 2: Check console logs
1. Open browser Console tab
2. Look for logs from API client:
   - "API Request:" logs showing endpoint, method, and token status
   - "API Error:" logs if request fails
3. Check for "401 Unauthorized" messages

### Step 3: Check backend logs
Look in the backend terminal for:
```
DEBUG: Validating token: [token_prefix]...
DEBUG: Token validated successfully for user_id: [user_id]
```
Or error messages like:
```
DEBUG: Token validation error: [error_message]
```

### Step 4: Test with a fresh login
1. Click "Logout" in the app
2. Log in again with your credentials
3. Try to delete or update a task immediately
4. If it works now, the token was expired (tokens expire after 30 minutes)

## Quick Fixes

### Fix 1: Increase token expiration time
Edit `phase-3/backend/core/security.py` line 15:
```python
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24 hours instead of 30 minutes
```

### Fix 2: Auto-logout on 401
The frontend already clears the token on 401, but doesn't redirect.
You could manually implement: logout → re-login when you see the error.

### Fix 3: Add token refresh mechanism
(More complex - would need backend changes)

## Testing Checklist

After making changes:
1. [ ] Restart backend server
2. [ ] Hard refresh frontend (Ctrl+Shift+R)
3. [ ] Clear browser localStorage
4. [ ] Log in with fresh credentials
5. [ ] Try to:
   - [ ] Add a task (via form)
   - [ ] Add a task (via chatbot)
   - [ ] Toggle task completion
   - [ ] Edit task title
   - [ ] Delete a task

## Common Issues

### Issue: "HTTP error! status: 401" in console
**Solution**: Token expired or invalid. Logout and login again.

### Issue: Task operations work after login but fail after some time
**Solution**: Token expired (30 min default). Increase `ACCESS_TOKEN_EXPIRE_MINUTES` in security.py

### Issue: Tasks added by chatbot use wrong user_id
**Solution**: Already fixed - chatbot now uses authenticated user's ID from auth context

## Current Debug Logs Enabled

### Frontend (lib/api.ts)
- Request details: endpoint, method, token status
- Error details: status code, endpoint, status text

### Backend (core/security.py)
- Token validation attempts
- User ID extraction from token
- Validation errors

### Backend (api/chat.py)
- User ID received in chat requests

### Backend (mcp_tools.py)
- Task creation details
- Date parsing
- Database operations

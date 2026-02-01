(globalThis.TURBOPACK || (globalThis.TURBOPACK = [])).push([typeof document === "object" ? document.currentScript : undefined,
"[project]/phase-3/frontend/lib/api.ts [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "apiClient",
    ()=>apiClient
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/next/dist/build/polyfills/process.js [app-client] (ecmascript)");
// API client utilities for backend communication
const API_BASE_URL = __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"].env.NEXT_PUBLIC_API_URL || __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"].env.BACKEND_URL || 'http://localhost:8000';
class ApiClient {
    baseUrl;
    constructor(baseUrl = API_BASE_URL){
        this.baseUrl = baseUrl;
    }
    async request(endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        // Get auth token from localStorage
        const token = ("TURBOPACK compile-time truthy", 1) ? localStorage.getItem('auth_token') : "TURBOPACK unreachable";
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
                ...token ? {
                    'Authorization': `Bearer ${token}`
                } : {},
                ...options.headers || {}
            }
        };
        const config = {
            ...defaultOptions,
            ...options,
            headers: {
                ...defaultOptions.headers,
                ...options.headers
            }
        };
        const response = await fetch(url, config);
        if (!response.ok) {
            // Handle unauthorized access
            if (response.status === 401) {
                // Clear auth token if unauthorized
                if ("TURBOPACK compile-time truthy", 1) {
                    localStorage.removeItem('auth_token');
                }
            // Optionally redirect to login page
            // window.location.href = '/login';
            }
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    }
    // Authentication endpoints
    async login(email, password) {
        const result = await this.request('/api/auth/login', {
            method: 'POST',
            body: JSON.stringify({
                email,
                password
            })
        });
        // Store token after successful login
        // Backend returns { access_token, token_type }
        if (result.access_token && ("TURBOPACK compile-time value", "object") !== 'undefined') {
            localStorage.setItem('auth_token', result.access_token);
        }
        return result;
    }
    async register(email, name, password) {
        const result = await this.request('/api/auth/register', {
            method: 'POST',
            body: JSON.stringify({
                email,
                name,
                password
            })
        });
        // Store token after successful registration
        // Backend returns { access_token, token_type }
        if (result.access_token && ("TURBOPACK compile-time value", "object") !== 'undefined') {
            localStorage.setItem('auth_token', result.access_token);
        }
        return result;
    }
    // Task endpoints
    async getTasks(userId, params = {}) {
        const queryParams = new URLSearchParams();
        if (params.search) queryParams.append('search', params.search);
        if (params.priority) queryParams.append('priority', params.priority);
        if (params.sort) queryParams.append('sort', params.sort);
        if (params.order) queryParams.append('order', params.order);
        const queryString = queryParams.toString();
        const endpoint = `/api/users/${userId}/tasks/${queryString ? `?${queryString}` : ''}`;
        return this.request(endpoint, {
            method: 'GET'
        });
    }
    async createTask(userId, taskData) {
        return this.request(`/api/users/${userId}/tasks/`, {
            method: 'POST',
            body: JSON.stringify(taskData)
        });
    }
    async updateTask(userId, taskId, taskData) {
        return this.request(`/api/users/${userId}/tasks/${taskId}`, {
            method: 'PUT',
            body: JSON.stringify(taskData)
        });
    }
    async deleteTask(userId, taskId) {
        return this.request(`/api/users/${userId}/tasks/${taskId}`, {
            method: 'DELETE'
        });
    }
}
const apiClient = new ApiClient();
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/phase-3/frontend/components/auth/auth-context.tsx [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "AuthProvider",
    ()=>AuthProvider,
    "useAuth",
    ()=>useAuth
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/next/dist/build/polyfills/process.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$phase$2d$3$2f$frontend$2f$lib$2f$api$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/phase-3/frontend/lib/api.ts [app-client] (ecmascript)");
;
var _s = __turbopack_context__.k.signature(), _s1 = __turbopack_context__.k.signature();
'use client';
;
;
const AuthContext = /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["createContext"])(undefined);
const AuthProvider = ({ children })=>{
    _s();
    const [user, setUser] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(null);
    const [loading, setLoading] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(true);
    // Check for existing session on mount
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useEffect"])({
        "AuthProvider.useEffect": ()=>{
            const checkSession = {
                "AuthProvider.useEffect.checkSession": async ()=>{
                    try {
                        // Only run on client side
                        if ("TURBOPACK compile-time truthy", 1) {
                            // Check if user is already logged in by verifying token or session
                            const token = localStorage.getItem('auth_token');
                            if (token) {
                                // Get API base URL from environment or default
                                const apiUrl = __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"].env.NEXT_PUBLIC_API_URL || __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"].env.BACKEND_URL || 'http://localhost:8000';
                                // Verify token with backend using a direct fetch since we don't have user ID yet
                                const response = await fetch(`${apiUrl}/api/auth/me`, {
                                    headers: {
                                        'Authorization': `Bearer ${token}`,
                                        'Content-Type': 'application/json'
                                    }
                                });
                                if (response.ok) {
                                    const userData = await response.json();
                                    setUser(userData);
                                } else {
                                    // Token is invalid, remove it
                                    localStorage.removeItem('auth_token');
                                }
                            }
                        }
                    } catch (error) {
                        console.error('Error checking session:', error);
                        if ("TURBOPACK compile-time truthy", 1) {
                            localStorage.removeItem('auth_token');
                        }
                    } finally{
                        setLoading(false);
                    }
                }
            }["AuthProvider.useEffect.checkSession"];
            checkSession();
        }
    }["AuthProvider.useEffect"], []);
    const signIn = async (email, password)=>{
        try {
            // Use the API client for login
            const data = await __TURBOPACK__imported__module__$5b$project$5d2f$phase$2d$3$2f$frontend$2f$lib$2f$api$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["apiClient"].login(email, password);
            // The API returns { access_token, token_type }
            const { access_token: token } = data;
            // Get API base URL from environment or default
            const apiUrl = __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"].env.NEXT_PUBLIC_API_URL || __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"].env.BACKEND_URL || 'http://localhost:8000';
            // Fetch user data after successful login
            const userResponse = await fetch(`${apiUrl}/api/auth/me`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            if (userResponse.ok) {
                const userData = await userResponse.json();
                // Store token in localStorage (this is already done in the API client)
                setUser(userData);
            } else {
                throw new Error('Failed to fetch user data after login');
            }
        } catch (error) {
            console.error('Sign in error:', error);
            throw error;
        }
    };
    const signUp = async (email, password, name)=>{
        try {
            // Use the API client for registration
            const data = await __TURBOPACK__imported__module__$5b$project$5d2f$phase$2d$3$2f$frontend$2f$lib$2f$api$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["apiClient"].register(email, name, password);
            // The API returns { access_token, token_type }
            const { access_token: token } = data;
            // Get API base URL from environment or default
            const apiUrl = __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"].env.NEXT_PUBLIC_API_URL || __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"].env.BACKEND_URL || 'http://localhost:8000';
            // Fetch user data after successful registration
            const userResponse = await fetch(`${apiUrl}/api/auth/me`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            if (userResponse.ok) {
                const userData = await userResponse.json();
                // Store token in localStorage (this is already done in the API client)
                setUser(userData);
            } else {
                throw new Error('Failed to fetch user data after registration');
            }
        } catch (error) {
            console.error('Sign up error:', error);
            throw error;
        }
    };
    const signOut = async ()=>{
        try {
            // Clear token from localStorage
            localStorage.removeItem('auth_token');
            // Clear any other stored user data
            setUser(null);
        } catch (error) {
            console.error('Sign out error:', error);
        }
    };
    const updateUser = (userData)=>{
        setUser((prevUser)=>prevUser ? {
                ...prevUser,
                ...userData
            } : null);
    };
    const value = {
        user,
        loading,
        signIn,
        signUp,
        signOut,
        updateUser
    };
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(AuthContext.Provider, {
        value: value,
        children: children
    }, void 0, false, {
        fileName: "[project]/phase-3/frontend/components/auth/auth-context.tsx",
        lineNumber: 156,
        columnNumber: 10
    }, ("TURBOPACK compile-time value", void 0));
};
_s(AuthProvider, "NiO5z6JIqzX62LS5UWDgIqbZYyY=");
_c = AuthProvider;
const useAuth = ()=>{
    _s1();
    const context = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useContext"])(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};
_s1(useAuth, "b9L3QQ+jgeyIrH0NfHrJ8nn7VMU=");
var _c;
__turbopack_context__.k.register(_c, "AuthProvider");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
]);

//# sourceMappingURL=phase-3_frontend_ee4c7c0b._.js.map
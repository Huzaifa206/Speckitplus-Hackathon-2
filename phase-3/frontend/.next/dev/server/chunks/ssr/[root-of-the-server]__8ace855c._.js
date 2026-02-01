module.exports = [
"[externals]/next/dist/compiled/next-server/app-page-turbo.runtime.dev.js [external] (next/dist/compiled/next-server/app-page-turbo.runtime.dev.js, cjs)", ((__turbopack_context__, module, exports) => {

const mod = __turbopack_context__.x("next/dist/compiled/next-server/app-page-turbo.runtime.dev.js", () => require("next/dist/compiled/next-server/app-page-turbo.runtime.dev.js"));

module.exports = mod;
}),
"[project]/phase-3/frontend/lib/api.ts [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "apiClient",
    ()=>apiClient
]);
// API client utilities for backend communication
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || process.env.BACKEND_URL || 'http://localhost:8000';
class ApiClient {
    baseUrl;
    constructor(baseUrl = API_BASE_URL){
        this.baseUrl = baseUrl;
    }
    async request(endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        // Get auth token from localStorage
        const token = ("TURBOPACK compile-time falsy", 0) ? "TURBOPACK unreachable" : null;
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
                ...("TURBOPACK compile-time falsy", 0) ? "TURBOPACK unreachable" : {},
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
                if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
                ;
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
        if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
        ;
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
        if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
        ;
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
}),
"[project]/phase-3/frontend/components/auth/auth-context.tsx [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "AuthProvider",
    ()=>AuthProvider,
    "useAuth",
    ()=>useAuth
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react-jsx-dev-runtime.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$phase$2d$3$2f$frontend$2f$lib$2f$api$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/phase-3/frontend/lib/api.ts [app-ssr] (ecmascript)");
'use client';
;
;
;
const AuthContext = /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["createContext"])(undefined);
const AuthProvider = ({ children })=>{
    const [user, setUser] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])(null);
    const [loading, setLoading] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])(true);
    // Check for existing session on mount
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useEffect"])(()=>{
        const checkSession = async ()=>{
            try {
                // Only run on client side
                if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
                ;
            } catch (error) {
                console.error('Error checking session:', error);
                if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
                ;
            } finally{
                setLoading(false);
            }
        };
        checkSession();
    }, []);
    const signIn = async (email, password)=>{
        try {
            // Use the API client for login
            const data = await __TURBOPACK__imported__module__$5b$project$5d2f$phase$2d$3$2f$frontend$2f$lib$2f$api$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["apiClient"].login(email, password);
            // The API returns { access_token, token_type }
            const { access_token: token } = data;
            // Get API base URL from environment or default
            const apiUrl = process.env.NEXT_PUBLIC_API_URL || process.env.BACKEND_URL || 'http://localhost:8000';
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
            const data = await __TURBOPACK__imported__module__$5b$project$5d2f$phase$2d$3$2f$frontend$2f$lib$2f$api$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["apiClient"].register(email, name, password);
            // The API returns { access_token, token_type }
            const { access_token: token } = data;
            // Get API base URL from environment or default
            const apiUrl = process.env.NEXT_PUBLIC_API_URL || process.env.BACKEND_URL || 'http://localhost:8000';
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
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(AuthContext.Provider, {
        value: value,
        children: children
    }, void 0, false, {
        fileName: "[project]/phase-3/frontend/components/auth/auth-context.tsx",
        lineNumber: 156,
        columnNumber: 10
    }, ("TURBOPACK compile-time value", void 0));
};
const useAuth = ()=>{
    const context = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useContext"])(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};
}),
"[project]/node_modules/next/dist/server/route-modules/app-page/module.compiled.js [app-ssr] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
;
else {
    if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
    ;
    else {
        if ("TURBOPACK compile-time truthy", 1) {
            if ("TURBOPACK compile-time truthy", 1) {
                module.exports = __turbopack_context__.r("[externals]/next/dist/compiled/next-server/app-page-turbo.runtime.dev.js [external] (next/dist/compiled/next-server/app-page-turbo.runtime.dev.js, cjs)");
            } else //TURBOPACK unreachable
            ;
        } else //TURBOPACK unreachable
        ;
    }
} //# sourceMappingURL=module.compiled.js.map
}),
"[project]/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react-jsx-dev-runtime.js [app-ssr] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

module.exports = __turbopack_context__.r("[project]/node_modules/next/dist/server/route-modules/app-page/module.compiled.js [app-ssr] (ecmascript)").vendored['react-ssr'].ReactJsxDevRuntime; //# sourceMappingURL=react-jsx-dev-runtime.js.map
}),
"[project]/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react.js [app-ssr] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

module.exports = __turbopack_context__.r("[project]/node_modules/next/dist/server/route-modules/app-page/module.compiled.js [app-ssr] (ecmascript)").vendored['react-ssr'].React; //# sourceMappingURL=react.js.map
}),
];

//# sourceMappingURL=%5Broot-of-the-server%5D__8ace855c._.js.map
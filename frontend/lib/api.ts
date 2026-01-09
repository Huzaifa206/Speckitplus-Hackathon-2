// API client utilities for backend communication
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  private async request(endpoint: string, options: RequestInit = {}) {
    const url = `${this.baseUrl}${endpoint}`;

    // Get auth token from localStorage
    const token = typeof window !== 'undefined' ? localStorage.getItem('auth_token') : null;

    const defaultOptions: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
        ...(options.headers || {}),
      },
    };

    const config = {
      ...defaultOptions,
      ...options,
      headers: {
        ...defaultOptions.headers,
        ...options.headers,
      },
    };

    const response = await fetch(url, config);

    if (!response.ok) {
      // Handle unauthorized access
      if (response.status === 401) {
        // Clear auth token if unauthorized
        if (typeof window !== 'undefined') {
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
  async login(email: string, password: string) {
    const result = await this.request('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });

    // Store token after successful login
    if (result.token && typeof window !== 'undefined') {
      localStorage.setItem('auth_token', result.token);
    }

    return result;
  }

  async register(email: string, name: string, password: string) {
    const result = await this.request('/api/auth/register', {
      method: 'POST',
      body: JSON.stringify({ email, name, password }),
    });

    // Store token after successful registration
    if (result.token && typeof window !== 'undefined') {
      localStorage.setItem('auth_token', result.token);
    }

    return result;
  }

  // Task endpoints
  async getTasks(userId: string, params: { search?: string; priority?: string; sort?: string; order?: string } = {}) {
    const queryParams = new URLSearchParams();
    if (params.search) queryParams.append('search', params.search);
    if (params.priority) queryParams.append('priority', params.priority);
    if (params.sort) queryParams.append('sort', params.sort);
    if (params.order) queryParams.append('order', params.order);

    const queryString = queryParams.toString();
    const endpoint = `/api/users/${userId}/tasks/${queryString ? `?${queryString}` : ''}`;

    return this.request(endpoint, {
      method: 'GET',
    });
  }

  async createTask(userId: string, taskData: any) {
    return this.request(`/api/users/${userId}/tasks/`, {
      method: 'POST',
      body: JSON.stringify(taskData),
    });
  }

  async updateTask(userId: string, taskId: number, taskData: any) {
    return this.request(`/api/users/${userId}/tasks/${taskId}`, {
      method: 'PUT',
      body: JSON.stringify(taskData),
    });
  }

  async deleteTask(userId: string, taskId: number) {
    return this.request(`/api/users/${userId}/tasks/${taskId}`, {
      method: 'DELETE',
    });
  }
}

export const apiClient = new ApiClient();
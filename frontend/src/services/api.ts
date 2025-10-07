import axios, { type AxiosResponse } from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

// 建立 axios 實例
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 用戶介面
interface User {
  id: number;
  username: string;
  email?: string;
}

// 登入憑證介面
interface LoginCredentials {
  username: string;
  password: string;
}

// 登入回應介面
interface LoginResponse {
  token: string;
  user: User;
}

// 推薦介面
interface Recommendation {
  department?: string;
  university?: string;
  major?: string;
  score?: number;
  reason?: string;
}

// 推薦回應介面
interface RecommendationResponse {
  recommendations: Recommendation[];
}

// 資源介面
interface Resource {
  id: number;
  title: string;
  description?: string;
  category?: string;
  url?: string;
}

// 請求攔截器
api.interceptors.request.use(
  (config) => {
    // 從 localStorage 獲取 token
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 響應攔截器
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response?.status === 401) {
      // Token 過期或無效，清除本地儲存
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// API 服務類別
export class ApiService {
  // 認證相關 API
  static async login(credentials: LoginCredentials): Promise<LoginResponse> {
    try {
      const response: AxiosResponse<LoginResponse> = await api.post('/api/auth/login', credentials);
      const { token, user } = response.data;
      
      // 儲存 token 和用戶資訊
      localStorage.setItem('token', token);
      localStorage.setItem('user', JSON.stringify(user));
      
      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.message || '登入失敗');
    }
  }

  static logout(): void {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  }

  static getCurrentUser(): User | null {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
  }

  static isAuthenticated(): boolean {
    return !!localStorage.getItem('token');
  }

  // 上傳相關 API
  static async uploadData(formData: FormData): Promise<any> {
    try {
      const response = await api.post('/api/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.message || '上傳失敗');
    }
  }

  // 推薦相關 API
  static async getRecommendation(userId: string): Promise<RecommendationResponse> {
    try {
      const response: AxiosResponse<RecommendationResponse> = await api.get(`/api/recommendation/${userId}`);
      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.message || '獲取推薦失敗');
    }
  }

  // 資源管理 API (原有的)
  static async getResources(): Promise<Resource[]> {
    try {
      const response: AxiosResponse<Resource[]> = await api.get('/resources');
      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.message || '獲取資源失敗');
    }
  }

  static async getResource(id: number): Promise<Resource> {
    try {
      const response: AxiosResponse<Resource> = await api.get(`/resources/${id}`);
      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.message || '獲取資源失敗');
    }
  }

  static async createResource(resource: Omit<Resource, 'id'>): Promise<Resource> {
    try {
      const response: AxiosResponse<Resource> = await api.post('/resources', resource);
      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.message || '建立資源失敗');
    }
  }

  static async updateResource(id: number, resource: Partial<Resource>): Promise<Resource> {
    try {
      const response: AxiosResponse<Resource> = await api.put(`/resources/${id}`, resource);
      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.message || '更新資源失敗');
    }
  }

  static async deleteResource(id: number): Promise<void> {
    try {
      await api.delete(`/resources/${id}`);
    } catch (error: any) {
      throw new Error(error.response?.data?.message || '刪除資源失敗');
    }
  }
}

export default api;

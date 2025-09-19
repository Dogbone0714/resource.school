const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface Resource {
  id: number;
  title: string;
  description?: string;
  category?: string;
  url?: string;
  created_at: string;
  updated_at: string;
}

export interface CreateResource {
  title: string;
  description?: string;
  category?: string;
  url?: string;
}

export class ApiService {
  private static async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`;
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  }

  static async getResources(): Promise<Resource[]> {
    return this.request<Resource[]>('/resources');
  }

  static async getResource(id: number): Promise<Resource> {
    return this.request<Resource>(`/resources/${id}`);
  }

  static async createResource(resource: CreateResource): Promise<Resource> {
    return this.request<Resource>('/resources', {
      method: 'POST',
      body: JSON.stringify(resource),
    });
  }

  static async updateResource(id: number, resource: CreateResource): Promise<Resource> {
    return this.request<Resource>(`/resources/${id}`, {
      method: 'PUT',
      body: JSON.stringify(resource),
    });
  }

  static async deleteResource(id: number): Promise<void> {
    return this.request<void>(`/resources/${id}`, {
      method: 'DELETE',
    });
  }
}

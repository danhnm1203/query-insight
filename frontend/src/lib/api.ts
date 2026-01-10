import axios, { type AxiosInstance } from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

class ApiClient {
    private client: AxiosInstance

    constructor() {
        this.client = axios.create({
            baseURL: API_BASE_URL,
            headers: {
                'Content-Type': 'application/json',
            },
        })

        // Add auth token to requests
        this.client.interceptors.request.use((config) => {
            const token = localStorage.getItem('token')
            if (token) {
                config.headers.Authorization = `Bearer ${token}`
            }
            return config
        })

        // Handle auth errors
        this.client.interceptors.response.use(
            (response) => response,
            (error) => {
                if (error.response?.status === 401) {
                    localStorage.removeItem('token')
                    window.location.href = '/login'
                }
                return Promise.reject(error)
            }
        )
    }

    // Health check
    async healthCheck() {
        const { data } = await this.client.get('/health')
        return data
    }

    // Databases
    async getDatabases() {
        const { data } = await this.client.get('/api/v1/databases')
        return data
    }

    async createDatabase(database: any) {
        const { data } = await this.client.post('/api/v1/databases', database)
        return data
    }

    async getDatabase(id: string) {
        const { data } = await this.client.get(`/api/v1/databases/${id}`)
        return data
    }

    async deleteDatabase(id: string) {
        await this.client.delete(`/api/v1/databases/${id}`)
    }

    // Queries
    async getSlowQueries(databaseId: string, limit: number = 50) {
        const { data } = await this.client.get(
            `/api/v1/databases/${databaseId}/queries/slow?limit=${limit}`
        )
        return data
    }

    async getQueryDetails(id: string) {
        const { data } = await this.client.get(`/api/v1/queries/${id}`)
        return data
    }

    // Metrics
    async getMetrics(databaseId: string, timeRange: string = '1h') {
        const { data } = await this.client.get(
            `/api/v1/databases/${databaseId}/metrics?time_range=${timeRange}`
        )
        return data
    }

    // Recommendations
    async getRecommendations(queryId: string) {
        const { data } = await this.client.get(`/api/v1/queries/${queryId}/recommendations`)
        return data
    }

    async applyRecommendation(id: string) {
        const { data } = await this.client.post(`/api/v1/recommendations/${id}/apply`)
        return data
    }

    async dismissRecommendation(id: string) {
        const { data } = await this.client.post(`/api/v1/recommendations/${id}/dismiss`)
        return data
    }
}

export const api = new ApiClient()

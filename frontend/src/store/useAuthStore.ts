import { create } from 'zustand'
import { api } from '../lib/api'

interface User {
    id: string
    email: string
    full_name?: string
    plan_tier: string
    onboarding_completed: boolean
}

interface AuthState {
    user: User | null
    token: string | null
    isAuthenticated: boolean
    isLoading: boolean
    error: string | null
    register: (userData: any) => Promise<void>
    login: (credentials: any) => Promise<void>
    logout: () => void
    checkAuth: () => Promise<void>
}

export const useAuthStore = create<AuthState>((set) => ({
    user: null,
    token: localStorage.getItem('token'),
    isAuthenticated: !!localStorage.getItem('token'),
    isLoading: false,
    error: null,

    login: async (credentials) => {
        set({ isLoading: true, error: null })
        try {
            const data = await api.login(credentials)
            localStorage.setItem('token', data.access_token)
            set({
                token: data.access_token,
                isAuthenticated: true,
                isLoading: false
            })
            // Fetch user info after login
            const user = await api.getMe()
            set({ user })
        } catch (error: any) {
            const message = error.response?.data?.detail || 'Login failed'
            set({ error: message, isLoading: false, isAuthenticated: false })
            throw error
        }
    },

    register: async (userData) => {
        set({ isLoading: true, error: null })
        try {
            await api.register(userData)
            set({ isLoading: false })
        } catch (error: any) {
            const message = error.response?.data?.detail || 'Registration failed'
            set({ error: message, isLoading: false })
            throw error
        }
    },

    logout: () => {
        localStorage.removeItem('token')
        set({ user: null, token: null, isAuthenticated: false })
    },

    checkAuth: async () => {
        if (!localStorage.getItem('token')) {
            set({ isAuthenticated: false, user: null })
            return
        }

        set({ isLoading: true })
        try {
            const user = await api.getMe()
            set({ user, isAuthenticated: true, isLoading: false })
        } catch (error) {
            localStorage.removeItem('token')
            set({ user: null, token: null, isAuthenticated: false, isLoading: false })
        }
    }
}))

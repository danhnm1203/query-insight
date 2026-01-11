import { create } from 'zustand'
import { api } from '../lib/api'

interface Database {
    id: string
    name: string
    type: string
    is_active: boolean
    connection_status: 'online' | 'offline' | 'syncing' | 'unknown'
    connection_error?: string
    last_checked_at?: string
    created_at: string
    last_connected_at?: string
    last_collection_at?: string
}

interface DatabaseState {
    databases: Database[]
    selectedDatabaseId: string | null
    isLoading: boolean
    error: string | null
    fetchDatabases: () => Promise<void>
    setSelectedDatabaseId: (id: string | null) => void
    addDatabase: (database: any) => Promise<void>
    checkDatabaseConnection: (id: string) => Promise<void>
    deleteDatabase: (id: string) => Promise<void>
}

export const useDatabaseStore = create<DatabaseState>((set) => ({
    databases: [],
    selectedDatabaseId: null,
    isLoading: false,
    error: null,

    fetchDatabases: async () => {
        set({ isLoading: true, error: null })
        try {
            const databases = await api.getDatabases()
            set((state) => ({
                databases,
                isLoading: false,
                selectedDatabaseId: state.selectedDatabaseId || (databases.length > 0 ? databases[0].id : null)
            }))
        } catch (error: any) {
            set({ error: 'Failed to fetch databases', isLoading: false })
        }
    },

    setSelectedDatabaseId: (id: string | null) => {
        set({ selectedDatabaseId: id })
    },

    addDatabase: async (databaseData) => {
        set({ isLoading: true, error: null })
        try {
            const newDb = await api.createDatabase(databaseData)
            set((state) => ({
                databases: [newDb, ...state.databases],
                isLoading: false
            }))
        } catch (error: any) {
            const message = error.response?.data?.detail || 'Failed to add database'
            set({ error: message, isLoading: false })
            throw error
        }
    },

    checkDatabaseConnection: async (id) => {
        try {
            await api.triggerDatabaseCheck(id)
            // Optimistically update status to syncing
            set((state) => ({
                databases: state.databases.map(db =>
                    db.id === id ? { ...db, connection_status: 'syncing' } : db
                )
            }))
        } catch (error: any) {
            console.error('Failed to trigger connection check:', error)
        }
    },

    deleteDatabase: async (id) => {
        set({ isLoading: true, error: null })
        try {
            await api.deleteDatabase(id)
            set((state) => ({
                databases: state.databases.filter(db => db.id !== id),
                isLoading: false
            }))
        } catch (error: any) {
            set({ error: 'Failed to delete database', isLoading: false })
        }
    }
}))

import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Database, Plus, Trash2, RefreshCw, CheckCircle2, XCircle, Clock, Activity, BarChart3, List } from 'lucide-react'
import { formatDistanceToNow } from 'date-fns'
import { useDatabaseStore } from '../store/useDatabaseStore'
import AddDatabaseModal from '../components/databases/AddDatabaseModal'
import { Button } from '../components/ui/button'
import {
    AlertDialog,
    AlertDialogAction,
    AlertDialogCancel,
    AlertDialogContent,
    AlertDialogDescription,
    AlertDialogFooter,
    AlertDialogHeader,
    AlertDialogTitle,
} from '../components/ui/alert-dialog'

const DatabasesPage: React.FC = () => {
    const { databases, fetchDatabases, deleteDatabase, isLoading, error } = useDatabaseStore()
    const [isRefreshing, setIsRefreshing] = useState(false)
    const [isModalOpen, setIsModalOpen] = useState(false)
    const [deleteDialogOpen, setDeleteDialogOpen] = useState(false)
    const [databaseToDelete, setDatabaseToDelete] = useState<{ id: string; name: string } | null>(null)
    const navigate = useNavigate()

    useEffect(() => {
        fetchDatabases()
    }, [fetchDatabases])

    const handleRefresh = async () => {
        setIsRefreshing(true)
        await fetchDatabases()
        setIsRefreshing(false)
    }

    const handleDelete = async (id: string, name: string, e: React.MouseEvent) => {
        e.stopPropagation() // Prevent card click
        setDatabaseToDelete({ id, name })
        setDeleteDialogOpen(true)
    }

    const confirmDelete = async () => {
        if (databaseToDelete) {
            await deleteDatabase(databaseToDelete.id)
            setDeleteDialogOpen(false)
            setDatabaseToDelete(null)
        }
    }

    return (
        <div className="space-y-8 animate-in fade-in duration-500">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight">Databases</h1>
                    <p className="text-muted-foreground">
                        Manage your connected databases and monitoring status
                    </p>
                </div>
                <div className="flex gap-3">
                    <button
                        onClick={handleRefresh}
                        className="p-2 rounded-lg border border-border hover:bg-accent transition-colors disabled:opacity-50"
                        disabled={isLoading || isRefreshing}
                    >
                        <RefreshCw className={`w-5 h-5 ${isRefreshing ? 'animate-spin' : ''}`} />
                    </button>
                    <button
                        onClick={() => setIsModalOpen(true)}
                        className="flex items-center gap-2 bg-primary text-primary-foreground px-4 py-2 rounded-lg font-medium hover:opacity-90 transition-all shadow-sm"
                    >
                        <Plus className="w-5 h-5" />
                        Add Database
                    </button>
                </div>
            </div>

            {error && (
                <div className="p-4 bg-destructive/10 text-destructive rounded-lg border border-destructive/20 flex items-center gap-2">
                    <XCircle className="w-5 h-5" />
                    <span>{error}</span>
                </div>
            )}

            {isLoading && databases.length === 0 ? (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {[1, 2, 3].map((i) => (
                        <div key={i} className="h-48 rounded-2xl border border-border bg-card animate-pulse" />
                    ))}
                </div>
            ) : databases.length === 0 ? (
                <div className="text-center py-20 border-2 border-dashed border-border rounded-3xl space-y-4">
                    <div className="inline-flex p-4 rounded-2xl bg-primary/5 text-primary">
                        <Database className="w-12 h-12" />
                    </div>
                    <div className="space-y-1">
                        <h3 className="text-xl font-semibold">No databases connected</h3>
                        <p className="text-muted-foreground max-w-sm mx-auto">
                            Connect your first database to start monitoring query performance and getting optimization insights.
                        </p>
                    </div>
                    <button
                        onClick={() => setIsModalOpen(true)}
                        className="mt-4 bg-primary text-primary-foreground px-6 py-2.5 rounded-lg font-semibold hover:opacity-90 transition-all shadow-md"
                    >
                        Add My First Database
                    </button>
                </div>
            ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {databases.map((db) => (
                        <div
                            key={db.id}
                            onClick={() => navigate(`/databases/${db.id}/queries`)}
                            className="group relative rounded-2xl border border-border bg-card p-6 shadow-sm transition-all hover:shadow-md hover:border-primary/20 cursor-pointer"
                        >
                            <div className="flex items-start justify-between">
                                <div className="p-3 rounded-xl bg-primary/10 text-primary">
                                    <Database className="w-6 h-6" />
                                </div>
                                <div className="flex items-center gap-2">
                                    {db.is_active ? (
                                        <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-emerald-500/10 text-emerald-500 text-xs font-bold">
                                            <CheckCircle2 className="w-3.5 h-3.5" />
                                            Active
                                        </div>
                                    ) : (
                                        <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-destructive/10 text-destructive text-xs font-bold">
                                            <Clock className="w-3.5 h-3.5" />
                                            Inactive
                                        </div>
                                    )}
                                </div>
                            </div>

                            <div className="mt-4 space-y-1">
                                <h3 className="text-lg font-bold group-hover:text-primary transition-colors">{db.name}</h3>
                                <p className="text-sm text-muted-foreground uppercase tracking-wider font-semibold">{db.type}</p>
                            </div>

                            <div className="mt-6 pt-4 border-t border-border flex flex-col gap-3">
                                <div className="flex items-center justify-between text-xs">
                                    <span className="text-muted-foreground flex items-center gap-1">
                                        <Activity className="w-3 h-3" />
                                        Last collected:
                                    </span>
                                    <span className="font-medium">
                                        {db.last_collection_at
                                            ? formatDistanceToNow(new Date(db.last_collection_at), { addSuffix: true })
                                            : 'Waiting...'}
                                    </span>
                                </div>

                                {/* Quick Actions */}
                                <div className="flex items-center gap-2">
                                    <Button
                                        variant="outline"
                                        size="sm"
                                        className="flex-1 h-8 text-xs"
                                        onClick={(e) => {
                                            e.stopPropagation()
                                            navigate(`/dashboard?db=${db.id}`)
                                        }}
                                    >
                                        <BarChart3 className="w-3 h-3 mr-1.5" />
                                        Dashboard
                                    </Button>
                                    <Button
                                        variant="outline"
                                        size="sm"
                                        className="flex-1 h-8 text-xs"
                                        onClick={(e) => {
                                            e.stopPropagation()
                                            navigate(`/databases/${db.id}/queries`)
                                        }}
                                    >
                                        <List className="w-3 h-3 mr-1.5" />
                                        Queries
                                    </Button>
                                    <Button
                                        variant="ghost"
                                        size="sm"
                                        className="h-8 w-8 p-0 text-muted-foreground hover:text-destructive hover:bg-destructive/10"
                                        onClick={(e) => handleDelete(db.id, db.name, e)}
                                    >
                                        <Trash2 className="w-3.5 h-3.5" />
                                    </Button>
                                </div>

                                <span className="text-[10px] text-muted-foreground text-center">
                                    Added {formatDistanceToNow(new Date(db.created_at), { addSuffix: true })}
                                </span>
                            </div>
                        </div>
                    ))}
                </div>
            )}

            <AddDatabaseModal
                isOpen={isModalOpen}
                onClose={() => setIsModalOpen(false)}
            />

            <AlertDialog open={deleteDialogOpen} onOpenChange={setDeleteDialogOpen}>
                <AlertDialogContent>
                    <AlertDialogHeader>
                        <AlertDialogTitle>Delete Database Connection?</AlertDialogTitle>
                        <AlertDialogDescription>
                            Are you sure you want to remove <span className="font-semibold text-foreground">{databaseToDelete?.name}</span>?
                            This will stop monitoring this database and remove all collected data. This action cannot be undone.
                        </AlertDialogDescription>
                    </AlertDialogHeader>
                    <AlertDialogFooter>
                        <AlertDialogCancel>Cancel</AlertDialogCancel>
                        <AlertDialogAction
                            onClick={confirmDelete}
                            className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
                        >
                            Delete Database
                        </AlertDialogAction>
                    </AlertDialogFooter>
                </AlertDialogContent>
            </AlertDialog>
        </div>
    )
}

export default DatabasesPage

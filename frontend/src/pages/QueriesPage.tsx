import React, { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { api } from '../lib/api'
import {
    Search, Filter, ArrowUpDown, ChevronRight,
    ArrowLeft, CheckCircle2,
    AlertTriangle, Database
} from 'lucide-react'
import { format, formatDistanceToNow } from 'date-fns'

const QueriesPage: React.FC = () => {
    const { id } = useParams<{ id: string }>()
    const [queries, setQueries] = useState<any[]>([])
    const [isLoading, setIsLoading] = useState(true)
    const [search, setSearch] = useState('')

    useEffect(() => {
        const fetchQueries = async () => {
            if (!id) return
            setIsLoading(true)
            try {
                const data = await api.getSlowQueries(id, 50)
                setQueries(data)
            } catch (err) {
                console.error('Failed to fetch queries', err)
            } finally {
                setIsLoading(false)
            }
        }
        fetchQueries()
    }, [id])

    const filteredQueries = queries.filter(q =>
        q.sql_text.toLowerCase().includes(search.toLowerCase()) ||
        q.status.toLowerCase().includes(search.toLowerCase())
    )

    return (
        <div className="space-y-8 animate-in fade-in duration-500">
            <div className="flex items-center gap-4">
                <Link to="/dashboard" className="p-2 rounded-xl hover:bg-accent transition-all text-muted-foreground hover:text-foreground border border-border">
                    <ArrowLeft className="w-5 h-5" />
                </Link>
                <div>
                    <h1 className="text-3xl font-bold tracking-tight">Slow Queries</h1>
                    <p className="text-muted-foreground flex items-center gap-2">
                        <Database className="w-4 h-4" />
                        Historical analysis for selected database
                    </p>
                </div>
            </div>

            {/* Filters Bar */}
            <div className="flex flex-col md:flex-row gap-4 items-center justify-between p-4 bg-card border border-border rounded-2xl shadow-sm">
                <div className="relative w-full md:w-96">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                    <input
                        type="text"
                        placeholder="Search SQL text or status..."
                        value={search}
                        onChange={(e) => setSearch(e.target.value)}
                        className="w-full pl-10 h-10 bg-background border border-border rounded-xl text-sm focus:ring-2 focus:ring-primary/20 outline-none transition-all"
                    />
                </div>

                <div className="flex items-center gap-4 w-full md:w-auto">
                    <button className="flex items-center gap-2 px-4 py-2 border border-border rounded-xl text-xs font-bold hover:bg-accent transition-all">
                        <Filter className="w-4 h-4" />
                        Filters
                    </button>
                    <button className="flex items-center gap-2 px-4 py-2 border border-border rounded-xl text-xs font-bold hover:bg-accent transition-all">
                        <ArrowUpDown className="w-4 h-4" />
                        Sort by: Latency
                    </button>
                </div>
            </div>

            {/* Queries List */}
            <div className="rounded-2xl border border-border bg-card overflow-hidden shadow-sm">
                <table className="w-full text-left border-collapse">
                    <thead>
                        <tr className="bg-accent/30 border-b border-border">
                            <th className="px-6 py-4 text-xs font-bold uppercase tracking-wider text-muted-foreground">Status</th>
                            <th className="px-6 py-4 text-xs font-bold uppercase tracking-wider text-muted-foreground">SQL Query</th>
                            <th className="px-6 py-4 text-xs font-bold uppercase tracking-wider text-muted-foreground text-right">Latency</th>
                            <th className="px-6 py-4 text-xs font-bold uppercase tracking-wider text-muted-foreground text-right">Last Seen</th>
                            <th className="px-6 py-4"></th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-border">
                        {isLoading ? (
                            [1, 2, 3, 4, 5].map(i => (
                                <tr key={i} className="animate-pulse">
                                    <td colSpan={5} className="px-6 py-8"><div className="h-4 bg-accent/50 rounded w-full" /></td>
                                </tr>
                            ))
                        ) : filteredQueries.length === 0 ? (
                            <tr>
                                <td colSpan={5} className="py-20 text-center text-muted-foreground">
                                    No queries found matching your filters.
                                </td>
                            </tr>
                        ) : (
                            filteredQueries.map((query) => (
                                <tr key={query.id} className="group hover:bg-accent/20 transition-all">
                                    <td className="px-6 py-4">
                                        <div className={`inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-tighter ${query.status === 'SLOW'
                                            ? 'bg-rose-500/10 text-rose-500'
                                            : 'bg-emerald-500/10 text-emerald-500'
                                            }`}>
                                            {query.status === 'SLOW' ? <AlertTriangle className="w-3" /> : <CheckCircle2 className="w-3" />}
                                            {query.status}
                                        </div>
                                    </td>
                                    <td className="px-6 py-4 max-w-md">
                                        <p className="text-sm font-mono line-clamp-1 text-foreground group-hover:text-primary transition-colors">
                                            {query.sql_text}
                                        </p>
                                    </td>
                                    <td className="px-6 py-4 text-right">
                                        <span className="text-sm font-bold">{query.execution_time_ms.toFixed(2)}ms</span>
                                    </td>
                                    <td className="px-6 py-4 text-right">
                                        <div className="flex flex-col items-end">
                                            <span className="text-sm">{format(new Date(query.timestamp), 'MMM d, HH:mm')}</span>
                                            <span className="text-[10px] text-muted-foreground">{formatDistanceToNow(new Date(query.timestamp), { addSuffix: true })}</span>
                                        </div>
                                    </td>
                                    <td className="px-6 py-4 text-right">
                                        <Link to={`/queries/${query.id}`} className="p-2 rounded-lg hover:bg-primary/10 text-primary transition-all opacity-0 group-hover:opacity-100 flex items-center justify-center">
                                            <ChevronRight className="w-5 h-5" />
                                        </Link>
                                    </td>
                                </tr>
                            ))
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    )
}

export default QueriesPage

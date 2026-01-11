import React, { useEffect, useState, useMemo } from 'react'
import { useParams, Link } from 'react-router-dom'
import { api } from '../lib/api'
import {
    ChevronRight, ChevronUp, ChevronDown,
    ArrowLeft, CheckCircle2,
    AlertTriangle, Database
} from 'lucide-react'
import { format, formatDistanceToNow } from 'date-fns'
import { QuerySearch } from '../components/queries/QuerySearch'
import { QueryFilters, type QueryFilters as QueryFiltersType } from '../components/queries/QueryFilters'
import { QueryPagination } from '../components/queries/QueryPagination'

const QueriesPage: React.FC = () => {
    const { id } = useParams<{ id: string }>()
    const [queries, setQueries] = useState<any[]>([])
    const [isLoading, setIsLoading] = useState(true)
    const [searchQuery, setSearchQuery] = useState('')
    const [filters, setFilters] = useState<QueryFiltersType>({
        status: 'all',
        timeRange: '24h',
        executionTimeMax: 10000
    })
    const [sortBy, setSortBy] = useState<'execution_time' | 'timestamp'>('execution_time')
    const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc')
    const [pagination, setPagination] = useState({ currentPage: 1, pageSize: 25 })

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

    // Helper function to get time range in milliseconds
    const getTimeRangeMs = (range: string): number => {
        const ranges: Record<string, number> = {
            '1h': 60 * 60 * 1000,
            '6h': 6 * 60 * 60 * 1000,
            '24h': 24 * 60 * 60 * 1000,
            '7d': 7 * 24 * 60 * 60 * 1000,
            '30d': 30 * 24 * 60 * 60 * 1000
        }
        return ranges[range] || ranges['24h']
    }

    // Filter, search, and sort queries
    const filteredAndSortedQueries = useMemo(() => {
        let result = [...queries]

        // Search filter
        if (searchQuery) {
            result = result.filter(q =>
                q.sql_text.toLowerCase().includes(searchQuery.toLowerCase())
            )
        }

        // Status filter
        if (filters.status !== 'all') {
            result = result.filter(q => q.status.toLowerCase() === filters.status)
        }

        // Time range filter
        const timeRangeMs = getTimeRangeMs(filters.timeRange)
        result = result.filter(q =>
            Date.now() - new Date(q.timestamp).getTime() <= timeRangeMs
        )

        // Execution time filter
        result = result.filter(q =>
            q.execution_time_ms <= filters.executionTimeMax
        )

        // Sort
        result.sort((a, b) => {
            const order = sortOrder === 'asc' ? 1 : -1
            if (sortBy === 'execution_time') {
                return (a.execution_time_ms - b.execution_time_ms) * order
            } else {
                return (new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime()) * order
            }
        })

        return result
    }, [queries, searchQuery, filters, sortBy, sortOrder])

    // Paginate results
    const paginatedQueries = useMemo(() => {
        const start = (pagination.currentPage - 1) * pagination.pageSize
        const end = start + pagination.pageSize
        return filteredAndSortedQueries.slice(start, end)
    }, [filteredAndSortedQueries, pagination])

    const totalPages = Math.ceil(filteredAndSortedQueries.length / pagination.pageSize)

    const handleSort = (column: 'execution_time' | 'timestamp') => {
        if (sortBy === column) {
            setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')
        } else {
            setSortBy(column)
            setSortOrder('desc')
        }
    }

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

            {/* Search and Filters */}
            <div className="space-y-4">
                <QuerySearch
                    value={searchQuery}
                    onChange={setSearchQuery}
                    placeholder="Search queries by SQL text..."
                />

                <QueryFilters
                    filters={filters}
                    onChange={setFilters}
                />

                {filteredAndSortedQueries.length > 0 && (
                    <div className="text-sm text-muted-foreground">
                        Found <span className="font-medium text-foreground">{filteredAndSortedQueries.length}</span> queries
                    </div>
                )}
            </div>

            {/* Queries List */}
            <div className="rounded-2xl border border-border bg-card overflow-hidden shadow-sm">
                <table className="w-full text-left border-collapse">
                    <thead>
                        <tr className="bg-accent/30 border-b border-border">
                            <th className="px-6 py-4 text-xs font-bold uppercase tracking-wider text-muted-foreground">Status</th>
                            <th className="px-6 py-4 text-xs font-bold uppercase tracking-wider text-muted-foreground">SQL Query</th>
                            <th
                                className="px-6 py-4 text-xs font-bold uppercase tracking-wider text-muted-foreground text-right cursor-pointer hover:text-foreground transition-colors"
                                onClick={() => handleSort('execution_time')}
                            >
                                <div className="flex items-center justify-end gap-1">
                                    Latency
                                    {sortBy === 'execution_time' && (
                                        sortOrder === 'asc' ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />
                                    )}
                                </div>
                            </th>
                            <th
                                className="px-6 py-4 text-xs font-bold uppercase tracking-wider text-muted-foreground text-right cursor-pointer hover:text-foreground transition-colors"
                                onClick={() => handleSort('timestamp')}
                            >
                                <div className="flex items-center justify-end gap-1">
                                    Last Seen
                                    {sortBy === 'timestamp' && (
                                        sortOrder === 'asc' ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />
                                    )}
                                </div>
                            </th>
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
                        ) : filteredAndSortedQueries.length === 0 ? (
                            <tr>
                                <td colSpan={5} className="py-20 text-center">
                                    <div className="flex flex-col items-center gap-2">
                                        <Database className="w-12 h-12 text-muted-foreground/50" />
                                        <p className="text-muted-foreground font-medium">No queries found</p>
                                        <p className="text-sm text-muted-foreground">Try adjusting your search or filters</p>
                                    </div>
                                </td>
                            </tr>
                        ) : (
                            paginatedQueries.map((query) => (
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

            {/* Pagination */}
            {filteredAndSortedQueries.length > 0 && (
                <QueryPagination
                    currentPage={pagination.currentPage}
                    totalPages={totalPages}
                    pageSize={pagination.pageSize}
                    totalItems={filteredAndSortedQueries.length}
                    onPageChange={(page) => setPagination({ ...pagination, currentPage: page })}
                    onPageSizeChange={(size) => setPagination({ currentPage: 1, pageSize: size })}
                />
            )}
        </div>
    )
}

export default QueriesPage

import React, { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { api } from '../lib/api'
import {
    ArrowLeft, Clock, Zap, AlertTriangle, CheckCircle2,
    Share2, Copy, BarChart3, Info, Layout, Database
} from 'lucide-react'
import { format } from 'date-fns'

const QueryDetailsPage: React.FC = () => {
    const { queryId } = useParams<{ queryId: string }>()
    const [query, setQuery] = useState<any>(null)
    const [isLoading, setIsLoading] = useState(true)

    useEffect(() => {
        const fetchDetails = async () => {
            if (!queryId) return
            setIsLoading(true)
            try {
                const data = await api.getQueryDetails(queryId)
                setQuery(data)
            } catch (err) {
                console.error('Failed to fetch query details', err)
            } finally {
                setIsLoading(false)
            }
        }
        fetchDetails()
    }, [queryId])

    if (isLoading) {
        return (
            <div className="flex h-[60vh] items-center justify-center">
                <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent" />
            </div>
        )
    }

    if (!query) {
        return (
            <div className="text-center py-20">
                <h2 className="text-2xl font-bold">Query not found</h2>
                <Link to="/dashboard" className="text-primary hover:underline mt-4 inline-block">Return to Dashboard</Link>
            </div>
        )
    }

    return (
        <div className="space-y-8 animate-in fade-in duration-500">
            {/* Header */}
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div className="flex items-center gap-4">
                    <Link to={`/databases/${query.database_id}/queries`} className="p-2 rounded-xl hover:bg-accent transition-all text-muted-foreground border border-border">
                        <ArrowLeft className="w-5 h-5" />
                    </Link>
                    <div>
                        <div className="flex items-center gap-2 mb-1">
                            <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-tighter ${query.status === 'SLOW' ? 'bg-rose-500/10 text-rose-500' : 'bg-emerald-500/10 text-emerald-500'
                                }`}>
                                {query.status}
                            </span>
                            <span className="text-xs text-muted-foreground">{format(new Date(query.timestamp), 'MMM d, yyyy HH:mm:ss')}</span>
                        </div>
                        <h1 className="text-2xl font-bold tracking-tight line-clamp-1">Query Analysis</h1>
                    </div>
                </div>

                <div className="flex items-center gap-3">
                    <button className="flex items-center gap-2 px-4 py-2 border border-border rounded-xl text-xs font-bold hover:bg-accent transition-all">
                        <Copy className="w-4 h-4" />
                        Copy SQL
                    </button>
                    <button className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-xl text-xs font-bold hover:opacity-90 transition-all shadow-sm">
                        <Share2 className="w-4 h-4" />
                        Share Report
                    </button>
                </div>
            </div>

            {/* Main Content Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Left Side: SQL & Explain */}
                <div className="lg:col-span-2 space-y-8">
                    {/* SQL Editor/Viewer */}
                    <div className="rounded-3xl border border-border bg-card overflow-hidden shadow-sm">
                        <div className="px-6 py-4 border-b border-border bg-accent/30 flex items-center justify-between">
                            <h3 className="font-bold text-sm flex items-center gap-2">
                                <Layout className="w-4 h-4 text-primary" />
                                SQL statement
                            </h3>
                        </div>
                        <div className="p-6 bg-[#0d1117]">
                            <pre className="text-sm font-mono text-blue-300 overflow-x-auto whitespace-pre-wrap">
                                {query.sql_text}
                            </pre>
                        </div>
                    </div>

                    {/* Execution Stats Card */}
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <MetricBox
                            label="Execution Time"
                            value={`${query.execution_time_ms.toFixed(2)}ms`}
                            icon={<Clock className="w-4 h-4 text-rose-500" />}
                        />
                        <MetricBox
                            label="Rows affected"
                            value="--"
                            icon={<BarChart3 className="w-4 h-4 text-blue-500" />}
                        />
                        <MetricBox
                            label="Source Database"
                            value="Production"
                            icon={<Database className="w-4 h-4 text-emerald-500" />}
                        />
                    </div>

                    {/* Explain Plan (Placeholder) */}
                    <div className="rounded-3xl border border-border bg-card overflow-hidden shadow-sm">
                        <div className="px-6 py-4 border-b border-border bg-accent/30">
                            <h3 className="font-bold text-sm flex items-center gap-2">
                                <Zap className="w-4 h-4 text-amber-500" />
                                Execution Plan (EXPLAIN)
                            </h3>
                        </div>
                        <div className="p-8 text-center space-y-4">
                            {query.explain_plan ? (
                                <pre className="text-left text-xs font-mono bg-accent/50 p-4 rounded-xl overflow-x-auto">
                                    {JSON.stringify(query.explain_plan, null, 2)}
                                </pre>
                            ) : (
                                <>
                                    <div className="inline-flex p-4 rounded-full bg-accent/50">
                                        <Info className="w-8 h-8 text-muted-foreground" />
                                    </div>
                                    <div className="max-w-xs mx-auto space-y-2">
                                        <p className="font-bold">No explain plan collected</p>
                                        <p className="text-xs text-muted-foreground">
                                            The explain plan for this specific execution wasn't captured. Enable adaptive collection to capture plans for similar queries.
                                        </p>
                                    </div>
                                    <button className="text-sm font-bold text-primary hover:underline">
                                        Trigger Manual EXPLAIN
                                    </button>
                                </>
                            )}
                        </div>
                    </div>
                </div>

                {/* Right Side: Insights & Recommendations */}
                <div className="space-y-8">
                    <div className="rounded-3xl border border-border bg-card p-6 shadow-sm border-t-4 border-t-amber-500">
                        <h3 className="font-bold text-lg mb-4 flex items-center gap-2">
                            <AlertTriangle className="w-5 h-5 text-amber-500" />
                            Performance Insights
                        </h3>
                        <ul className="space-y-4">
                            <InsightItem
                                title="High Latency detected"
                                desc={`This query took ${query.execution_time_ms.toFixed(0)}ms to execute, which is 5x above the 95th percentile.`}
                            />
                            <InsightItem
                                title="Potential Sequential Scan"
                                desc="Based on the structure, this query might be performing a full table scan on 'users'."
                                type="warning"
                            />
                        </ul>

                        <div className="mt-8 pt-6 border-t border-border">
                            <h4 className="text-xs font-bold uppercase tracking-wider text-muted-foreground mb-4">Recommended Actions</h4>
                            <div className="p-4 rounded-2xl bg-primary/5 border border-primary/10 space-y-3">
                                <div className="flex items-center gap-2 text-primary">
                                    <CheckCircle2 className="w-4 h-4" />
                                    <span className="text-sm font-bold">Add Index</span>
                                </div>
                                <p className="text-xs text-muted-foreground">
                                    Adding an index on <code className="bg-accent px-1 rounded">users(email)</code> could reduce execution time by up to 90%.
                                </p>
                                <button className="w-full py-2 bg-primary text-primary-foreground rounded-lg text-xs font-bold hover:opacity-90 transition-all">
                                    View Index details
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

const MetricBox = ({ label, value, icon }: { label: string, value: string, icon: any }) => (
    <div className="p-4 rounded-2xl border border-border bg-card shadow-sm space-y-1">
        <div className="flex items-center gap-2 text-muted-foreground">
            {icon}
            <span className="text-[10px] font-bold uppercase tracking-wider">{label}</span>
        </div>
        <div className="text-xl font-bold">{value}</div>
    </div>
)

const InsightItem = ({ title, desc, type = 'info' }: { title: string, desc: string, type?: 'info' | 'warning' }) => (
    <li className="flex gap-3">
        <div className={`mt-1 h-2 w-2 rounded-full shrink-0 ${type === 'info' ? 'bg-blue-500' : 'bg-amber-500'}`} />
        <div className="space-y-1">
            <p className="text-sm font-bold">{title}</p>
            <p className="text-xs text-muted-foreground leading-relaxed">{desc}</p>
        </div>
    </li>
)

export default QueryDetailsPage

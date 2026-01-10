import React, { useEffect, useState, useMemo } from 'react'
import { Link } from 'react-router-dom'
import { useDatabaseStore } from '../store/useDatabaseStore'
import { api } from '../lib/api'
import {
    XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
    AreaChart, Area
} from 'recharts'
import {
    Clock, Activity, Zap, AlertTriangle, ChevronRight,
    RefreshCw, TrendingUp, Layout
} from 'lucide-react'
import { format, formatDistanceToNow } from 'date-fns'
import QueryPatternsCard from '../components/dashboard/QueryPatternsCard'
import PerformanceRegressionsCard from '../components/dashboard/PerformanceRegressionsCard'
import OnboardingFlow from '../components/onboarding/OnboardingFlow'
import { useAuthStore } from '../store/useAuthStore'

const DashboardPage: React.FC = () => {
    const { databases, fetchDatabases } = useDatabaseStore()
    const [selectedDbId, setSelectedDbId] = useState<string>('')
    const [metrics, setMetrics] = useState<any[]>([])
    const [slowQueries, setSlowQueries] = useState<any[]>([])
    const [patterns, setPatterns] = useState<any[]>([])
    const [regressions, setRegressions] = useState<any[]>([])
    const [isLoading, setIsLoading] = useState(false)
    const [timeRange, setTimeRange] = useState('1h')
    const { user, checkAuth } = useAuthStore()
    const [showOnboarding, setShowOnboarding] = useState(false)

    useEffect(() => {
        if (user && !user.onboarding_completed) {
            setShowOnboarding(true)
        }
    }, [user])

    const handleCompleteOnboarding = async () => {
        try {
            await api.completeOnboarding()
            setShowOnboarding(false)
            checkAuth() // Refresh user state
        } catch (error) {
            console.error('Failed to complete onboarding', error)
        }
    }

    useEffect(() => {
        fetchDatabases()
    }, [fetchDatabases])

    useEffect(() => {
        if (databases.length > 0 && !selectedDbId) {
            setSelectedDbId(databases[0].id)
        }
    }, [databases, selectedDbId])

    const fetchData = async () => {
        if (!selectedDbId) return
        setIsLoading(true)
        try {
            const [metricsData, queriesData, patternsData, trendsData] = await Promise.all([
                api.getMetrics(selectedDbId, timeRange),
                api.getSlowQueries(selectedDbId, 5),
                api.getQueryPatterns(selectedDbId, 24),
                api.getPerformanceTrends(selectedDbId)
            ])
            setMetrics(metricsData.metrics || [])
            setSlowQueries(queriesData || [])
            setPatterns(patternsData || [])
            setRegressions(trendsData || [])
        } catch (error) {
            console.error('Failed to fetch dashboard data', error)
        } finally {
            setIsLoading(false)
        }
    }

    useEffect(() => {
        fetchData()
        const interval = setInterval(fetchData, 30000) // Polling every 30s
        return () => clearInterval(interval)
    }, [selectedDbId, timeRange])

    const chartData = useMemo(() => {
        return metrics.map(m => ({
            time: format(new Date(m.timestamp), 'HH:mm'),
            value: m.value,
            type: m.metric_type
        }))
    }, [metrics])

    const stats = useMemo(() => {
        const qps = metrics.filter(m => m.metric_type === 'QPS')
        const avgQps = qps.length ? qps.reduce((acc, m) => acc + m.value, 0) / qps.length : 0
        const maxLatency = slowQueries.length ? Math.max(...slowQueries.map(q => q.execution_time_ms)) : 0

        return {
            avgQps: avgQps.toFixed(2),
            slowCount: slowQueries.length,
            maxLatency: maxLatency.toFixed(2),
            health: databases.find(d => d.id === selectedDbId)?.is_active ? 'Healthy' : 'Inactive'
        }
    }, [metrics, slowQueries, selectedDbId, databases])

    return (
        <div className="space-y-8 animate-in fade-in duration-500">
            {/* Header & Controls */}
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight">Performance Dashboard</h1>
                    <p className="text-muted-foreground">Real-time database performance monitoring</p>
                </div>

                <div className="flex items-center gap-3">
                    <select
                        value={selectedDbId}
                        onChange={(e) => setSelectedDbId(e.target.value)}
                        className="bg-card border border-border rounded-xl px-4 py-2 text-sm focus:ring-2 focus:ring-primary/20 outline-none min-w-[180px]"
                    >
                        {databases.map(db => (
                            <option key={db.id} value={db.id}>{db.name}</option>
                        ))}
                    </select>

                    <div className="flex bg-accent/50 p-1 rounded-xl border border-border">
                        {['1h', '6h', '24h'].map(range => (
                            <button
                                key={range}
                                onClick={() => setTimeRange(range)}
                                className={`px-4 py-1.5 text-xs font-bold rounded-lg transition-all ${timeRange === range
                                    ? 'bg-primary text-primary-foreground shadow-sm'
                                    : 'text-muted-foreground hover:text-foreground'
                                    }`}
                            >
                                {range.toUpperCase()}
                            </button>
                        ))}
                    </div>

                    <button
                        onClick={fetchData}
                        className="p-2 rounded-xl border border-border hover:bg-accent transition-all"
                    >
                        <RefreshCw className={`w-5 h-5 ${isLoading ? 'animate-spin' : ''}`} />
                    </button>
                </div>
            </div>

            {/* Stats Overview */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <StatCard
                    title="Avg throughput"
                    value={`${stats.avgQps} QPS`}
                    icon={<Activity className="w-5 h-5 text-blue-500" />}
                    trend="+12%"
                />
                <StatCard
                    title="Slow queries"
                    value={stats.slowCount}
                    icon={<AlertTriangle className="w-5 h-5 text-amber-500" />}
                    trend="-2"
                />
                <StatCard
                    title="Peak Latency"
                    value={`${stats.maxLatency} ms`}
                    icon={<Clock className="w-5 h-5 text-rose-500" />}
                    trend="+5ms"
                />
                <StatCard
                    title="Status"
                    value={stats.health}
                    icon={<Zap className="w-5 h-5 text-emerald-500" />}
                    trend="Stable"
                />
            </div>

            {/* Charts Section */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <div className="lg:col-span-2 rounded-3xl border border-border bg-card p-6 shadow-sm">
                    <div className="flex items-center justify-between mb-8">
                        <h3 className="font-bold text-lg flex items-center gap-2">
                            <Activity className="w-5 h-5 text-primary" />
                            Throughput (Queries Per Second)
                        </h3>
                    </div>
                    <div className="h-[300px] w-full">
                        <ResponsiveContainer width="100%" height="100%">
                            <AreaChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                                <defs>
                                    <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="5%" stopColor="hsl(var(--primary))" stopOpacity={0.1} />
                                        <stop offset="95%" stopColor="hsl(var(--primary))" stopOpacity={0} />
                                    </linearGradient>
                                </defs>
                                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="hsl(var(--border))" />
                                <XAxis dataKey="time" stroke="hsl(var(--muted-foreground))" fontSize={12} tickLine={false} axisLine={false} />
                                <YAxis stroke="hsl(var(--muted-foreground))" fontSize={12} tickLine={false} axisLine={false} />
                                <Tooltip
                                    contentStyle={{
                                        backgroundColor: 'hsl(var(--card))',
                                        borderColor: 'hsl(var(--border))',
                                        borderRadius: '12px',
                                        fontSize: '12px'
                                    }}
                                />
                                <Area type="monotone" dataKey="value" stroke="hsl(var(--primary))" strokeWidth={3} fillOpacity={1} fill="url(#colorValue)" />
                            </AreaChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                <div className="rounded-3xl border border-border bg-card p-6 shadow-sm flex flex-col">
                    <div className="flex items-center justify-between mb-6">
                        <h3 className="font-bold text-lg flex items-center gap-2">
                            <Clock className="w-5 h-5 text-rose-500" />
                            Recent Slow Queries
                        </h3>
                    </div>

                    <div className="space-y-4 flex-1">
                        {slowQueries.length === 0 ? (
                            <div className="h-full flex flex-col items-center justify-center text-center space-y-2 py-8">
                                <div className="p-3 rounded-full bg-accent text-muted-foreground italic text-xs">
                                    No slow queries detected
                                </div>
                            </div>
                        ) : (
                            slowQueries.map((query) => (
                                <div key={query.id} className="group p-4 rounded-2xl hover:bg-accent transition-all border border-border">
                                    <div className="flex justify-between items-start mb-2">
                                        <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-rose-500/10 text-rose-500 uppercase">
                                            {query.execution_time_ms.toFixed(0)}ms
                                        </span>
                                        <span className="text-[10px] text-muted-foreground font-medium">{format(new Date(query.timestamp), 'HH:mm')}</span>
                                    </div>
                                    <p className="text-xs font-mono line-clamp-2 text-muted-foreground group-hover:text-foreground">
                                        {query.sql_text}
                                    </p>
                                </div>
                            ))
                        )}
                    </div>

                    <Link
                        to={`/databases/${selectedDbId}/queries`}
                        className="mt-6 w-full py-3 text-sm font-bold text-primary hover:bg-primary/5 rounded-xl transition-all flex items-center justify-center gap-2"
                    >
                        View All Queries
                        <ChevronRight className="w-4 h-4" />
                    </Link>
                </div>
            </div>

            {/* Intelligence Row */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <QueryPatternsCard patterns={patterns.slice(0, 5)} />
                <PerformanceRegressionsCard regressions={regressions} />
            </div>

            {showOnboarding && <OnboardingFlow onComplete={handleCompleteOnboarding} />}
        </div>
    )
}

const StatCard = ({ title, value, icon, trend }: { title: string, value: any, icon: any, trend: string }) => (
    <div className="rounded-2xl border border-border bg-card p-6 shadow-sm flex flex-col gap-1 transition-all hover:border-primary/20">
        <div className="flex items-center justify-between">
            <span className="text-sm text-muted-foreground font-medium">{title}</span>
            <div className="p-2 rounded-lg bg-accent/50">{icon}</div>
        </div>
        <div className="flex items-baseline gap-2 mt-2">
            <span className="text-2xl font-bold">{value}</span>
            <span className={`text-[10px] font-bold px-1.5 py-0.5 rounded-md ${trend.startsWith('+') ? 'bg-rose-500/10 text-rose-500' : 'bg-emerald-500/10 text-emerald-500'
                }`}>
                {trend}
            </span>
        </div>
    </div>
)

export default DashboardPage

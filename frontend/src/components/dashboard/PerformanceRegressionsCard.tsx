import React from 'react'
import { TrendingUp, AlertTriangle, ArrowUpRight } from 'lucide-react'

interface PerformanceRegression {
    normalized_sql: string
    recent_avg_ms: number
    baseline_avg_ms: number
    increase_percentage: number
    count: number
    last_seen: string
}

interface PerformanceRegressionsCardProps {
    regressions: PerformanceRegression[]
}

const PerformanceRegressionsCard: React.FC<PerformanceRegressionsCardProps> = ({ regressions }) => {
    return (
        <div className="rounded-3xl border border-border bg-card p-6 shadow-sm flex flex-col h-full border-t-4 border-t-rose-500">
            <div className="flex items-center justify-between mb-6">
                <h3 className="font-bold text-lg flex items-center gap-2">
                    <TrendingUp className="w-5 h-5 text-rose-500" />
                    Performance Regressions
                </h3>
                <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-rose-500/10 text-rose-500 uppercase tracking-wider">
                    Degrading Now
                </span>
            </div>

            <div className="space-y-4 flex-1">
                {regressions.length === 0 ? (
                    <div className="flex flex-col items-center justify-center text-center py-12 text-muted-foreground italic text-sm">
                        No regressions detected in the last 24h
                    </div>
                ) : (
                    regressions.map((reg, idx) => (
                        <div key={idx} className="p-4 rounded-2xl bg-rose-500/5 border border-rose-500/10 hover:bg-rose-500/10 transition-all group">
                            <div className="flex justify-between items-start mb-3">
                                <div className="flex flex-col gap-1">
                                    <div className="flex items-center gap-2 text-rose-500">
                                        <AlertTriangle className="w-4 h-4" />
                                        <span className="text-xs font-bold">Latency increased by {reg.increase_percentage.toFixed(0)}%</span>
                                    </div>
                                    <div className="text-[10px] text-muted-foreground font-medium">
                                        Baseline: {reg.baseline_avg_ms.toFixed(1)}ms → Recent: {reg.recent_avg_ms.toFixed(1)}ms
                                    </div>
                                </div>
                                <div className="p-1.5 rounded-lg bg-rose-500/20 text-rose-500">
                                    <ArrowUpRight className="w-4 h-4" />
                                </div>
                            </div>
                            <code className="text-xs font-mono text-muted-foreground group-hover:text-foreground line-clamp-2 break-all">
                                {reg.normalized_sql}
                            </code>
                        </div>
                    ))
                )}
            </div>
        </div>
    )
}

export default PerformanceRegressionsCard

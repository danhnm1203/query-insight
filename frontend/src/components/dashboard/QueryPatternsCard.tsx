import React from 'react'
import { Layout, Clock, BarChart3 } from 'lucide-react'

interface QueryPattern {
    normalized_sql: string
    count: number
    avg_exec_time_ms: number
    max_exec_time_ms: number
    last_seen: string
}

interface QueryPatternsCardProps {
    patterns: QueryPattern[]
}

const QueryPatternsCard: React.FC<QueryPatternsCardProps> = ({ patterns }) => {
    return (
        <div className="rounded-3xl border border-border bg-card p-6 shadow-sm flex flex-col h-full">
            <div className="flex items-center justify-between mb-6">
                <h3 className="font-bold text-lg flex items-center gap-2">
                    <Layout className="w-5 h-5 text-primary" />
                    Top Query Patterns
                </h3>
                <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-primary/10 text-primary uppercase tracking-wider">
                    Last 24h
                </span>
            </div>

            <div className="space-y-4 flex-1">
                {patterns.length === 0 ? (
                    <div className="flex flex-col items-center justify-center text-center py-12 text-muted-foreground italic text-sm">
                        No pattern data available
                    </div>
                ) : (
                    patterns.map((pattern, idx) => (
                        <div key={idx} className="p-4 rounded-2xl border border-border hover:bg-accent hover:border-primary/20 transition-all group">
                            <div className="flex justify-between items-start mb-2">
                                <div className="flex items-center gap-2">
                                    <span className="w-5 h-5 flex items-center justify-center rounded-md bg-accent text-[10px] font-bold">
                                        #{idx + 1}
                                    </span>
                                    <div className="flex items-center gap-3">
                                        <div className="flex items-center gap-1 text-[10px] font-bold text-muted-foreground">
                                            <BarChart3 className="w-3 h-3" />
                                            {pattern.count} calls
                                        </div>
                                        <div className="flex items-center gap-1 text-[10px] font-bold text-muted-foreground">
                                            <Clock className="w-3 h-3" />
                                            {pattern.avg_exec_time_ms.toFixed(1)}ms avg
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <code className="text-xs font-mono text-muted-foreground group-hover:text-foreground line-clamp-2 break-all">
                                {pattern.normalized_sql}
                            </code>
                        </div>
                    ))
                )}
            </div>
        </div>
    )
}

export default QueryPatternsCard

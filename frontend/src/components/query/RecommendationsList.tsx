import { CheckCircle2, TrendingUp, Lightbulb, AlertTriangle } from 'lucide-react'
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism'

interface RecommendationListProps {
    recommendations: any[]
    onApply?: (id: string) => void
    onDismiss?: (id: string) => void
}

const getTypeIcon = (type: string) => {
    switch (type.toLowerCase()) {
        case 'index':
            return <TrendingUp className="w-4 h-4" />
        case 'rewrite':
            return <Lightbulb className="w-4 h-4" />
        case 'limit':
            return <AlertTriangle className="w-4 h-4" />
        default:
            return <CheckCircle2 className="w-4 h-4" />
    }
}

const getSeverityVariant = (impact: number): "default" | "warning" | "destructive" => {
    if (impact >= 50) return "destructive"
    if (impact >= 25) return "warning"
    return "default"
}

export function RecommendationsList({ recommendations, onApply, onDismiss }: RecommendationListProps) {
    if (!recommendations || recommendations.length === 0) {
        return (
            <div className="py-10 text-center space-y-3">
                <div className="inline-flex p-3 rounded-full bg-emerald-500/10 text-emerald-500">
                    <CheckCircle2 className="w-6 h-6" />
                </div>
                <p className="text-sm font-bold">No issues detected</p>
                <p className="text-xs text-muted-foreground max-w-[300px] mx-auto">
                    We couldn't find any obvious performance bottlenecks for this query.
                </p>
            </div>
        )
    }

    return (
        <div className="space-y-4">
            {recommendations.map((rec) => (
                <Card key={rec.id} className="hover:shadow-md transition-shadow">
                    <CardHeader className="pb-3">
                        <div className="flex items-start justify-between gap-4">
                            <div className="flex items-center gap-2 flex-1">
                                <div className="p-2 rounded-lg bg-primary/10 text-primary">
                                    {getTypeIcon(rec.type)}
                                </div>
                                <CardTitle className="text-base">{rec.title}</CardTitle>
                            </div>
                            <div className="flex flex-col items-end gap-2">
                                <Badge variant={getSeverityVariant(rec.estimated_impact)}>
                                    {rec.estimated_impact.toFixed(0)}% Impact
                                </Badge>
                                <span className="text-xs text-muted-foreground">
                                    {(rec.confidence * 100).toFixed(0)}% confidence
                                </span>
                            </div>
                        </div>
                    </CardHeader>

                    <CardContent className="space-y-3">
                        <p className="text-sm text-muted-foreground leading-relaxed">
                            {rec.description}
                        </p>

                        {rec.sql_suggestion && (
                            <div className="rounded-lg overflow-hidden border border-border">
                                <div className="bg-muted px-3 py-2 border-b border-border">
                                    <span className="text-xs font-semibold text-muted-foreground uppercase">
                                        Suggested SQL
                                    </span>
                                </div>
                                <SyntaxHighlighter
                                    language="sql"
                                    style={vscDarkPlus}
                                    customStyle={{
                                        margin: 0,
                                        fontSize: '0.75rem',
                                        padding: '0.75rem',
                                    }}
                                >
                                    {rec.sql_suggestion}
                                </SyntaxHighlighter>
                            </div>
                        )}

                        {/* Impact Progress Bar */}
                        <div className="space-y-1">
                            <div className="flex items-center justify-between text-xs">
                                <span className="text-muted-foreground">Estimated Performance Gain</span>
                                <span className="font-semibold">{rec.estimated_impact.toFixed(0)}%</span>
                            </div>
                            <div className="h-2 bg-muted rounded-full overflow-hidden">
                                <div
                                    className={`h-full transition-all ${rec.estimated_impact >= 50
                                        ? 'bg-destructive'
                                        : rec.estimated_impact >= 25
                                            ? 'bg-yellow-500'
                                            : 'bg-primary'
                                        }`}
                                    style={{ width: `${Math.min(rec.estimated_impact, 100)}%` }}
                                />
                            </div>
                        </div>
                    </CardContent>

                    {rec.status === 'PENDING' && (onApply || onDismiss) && (
                        <CardFooter className="pt-0 gap-2">
                            {onApply && (
                                <Button
                                    onClick={() => onApply(rec.id)}
                                    className="flex-1"
                                    size="sm"
                                >
                                    Apply
                                </Button>
                            )}
                            {onDismiss && (
                                <Button
                                    onClick={() => onDismiss(rec.id)}
                                    variant="outline"
                                    className="flex-1"
                                    size="sm"
                                >
                                    Dismiss
                                </Button>
                            )}
                        </CardFooter>
                    )}
                </Card>
            ))}
        </div>
    )
}

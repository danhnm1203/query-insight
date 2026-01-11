import React from 'react'
import { CheckCircle2, AlertTriangle, Lightbulb, TrendingUp } from 'lucide-react'
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'

interface RecommendationCardProps {
    recommendation: {
        id: string
        type: string
        title: string
        description: string
        sql_suggestion?: string
        estimated_impact: number
        confidence: number
        status: string
    }
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

export function RecommendationCard({ recommendation, onApply, onDismiss }: RecommendationCardProps) {
    const { id, type, title, description, sql_suggestion, estimated_impact, confidence, status } = recommendation

    return (
        <Card className="hover:shadow-md transition-shadow">
            <CardHeader className="pb-3">
                <div className="flex items-start justify-between gap-4">
                    <div className="flex items-center gap-2 flex-1">
                        <div className="p-2 rounded-lg bg-primary/10 text-primary">
                            {getTypeIcon(type)}
                        </div>
                        <CardTitle className="text-base">{title}</CardTitle>
                    </div>
                    <div className="flex flex-col items-end gap-2">
                        <Badge variant={getSeverityVariant(estimated_impact)}>
                            {estimated_impact.toFixed(0)}% Impact
                        </Badge>
                        <span className="text-xs text-muted-foreground">
                            {(confidence * 100).toFixed(0)}% confidence
                        </span>
                    </div>
                </div>
            </CardHeader>

            <CardContent className="space-y-3">
                <p className="text-sm text-muted-foreground leading-relaxed">
                    {description}
                </p>

                {sql_suggestion && (
                    <div className="rounded-lg bg-muted p-3 border border-border">
                        <div className="flex items-center gap-2 mb-2">
                            <span className="text-xs font-semibold text-muted-foreground uppercase">
                                Suggested SQL
                            </span>
                        </div>
                        <pre className="text-xs font-mono overflow-x-auto whitespace-pre-wrap break-all">
                            <code>{sql_suggestion}</code>
                        </pre>
                    </div>
                )}

                {/* Impact Progress Bar */}
                <div className="space-y-1">
                    <div className="flex items-center justify-between text-xs">
                        <span className="text-muted-foreground">Estimated Performance Gain</span>
                        <span className="font-semibold">{estimated_impact.toFixed(0)}%</span>
                    </div>
                    <div className="h-2 bg-muted rounded-full overflow-hidden">
                        <div
                            className={`h-full transition-all ${estimated_impact >= 50
                                    ? 'bg-destructive'
                                    : estimated_impact >= 25
                                        ? 'bg-yellow-500'
                                        : 'bg-primary'
                                }`}
                            style={{ width: `${Math.min(estimated_impact, 100)}%` }}
                        />
                    </div>
                </div>
            </CardContent>

            {status === 'PENDING' && (onApply || onDismiss) && (
                <CardFooter className="pt-0 gap-2">
                    {onApply && (
                        <Button
                            onClick={() => onApply(id)}
                            className="flex-1"
                            size="sm"
                        >
                            Apply
                        </Button>
                    )}
                    {onDismiss && (
                        <Button
                            onClick={() => onDismiss(id)}
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
    )
}

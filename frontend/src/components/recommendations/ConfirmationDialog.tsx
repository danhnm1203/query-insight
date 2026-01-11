import {
    AlertDialog,
    AlertDialogAction,
    AlertDialogCancel,
    AlertDialogContent,
    AlertDialogDescription,
    AlertDialogFooter,
    AlertDialogHeader,
    AlertDialogTitle,
} from '@/components/ui/alert-dialog'
import { Badge } from '@/components/ui/badge'
import { Loader2 } from 'lucide-react'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism'

interface ConfirmationDialogProps {
    open: boolean
    onOpenChange: (open: boolean) => void
    actionType: 'apply' | 'dismiss'
    recommendation: {
        title: string
        estimated_impact: number
        confidence: number
        sql_suggestion?: string
        description: string
    } | null
    onConfirm: () => void | Promise<void>
    isLoading?: boolean
}

export function ConfirmationDialog({
    open,
    onOpenChange,
    actionType,
    recommendation,
    onConfirm,
    isLoading = false
}: ConfirmationDialogProps) {
    if (!recommendation) return null

    const isApply = actionType === 'apply'

    return (
        <AlertDialog open={open} onOpenChange={onOpenChange}>
            <AlertDialogContent className="max-w-2xl max-h-[80vh] overflow-y-auto">
                <AlertDialogHeader>
                    <AlertDialogTitle>
                        {isApply ? 'Apply Recommendation?' : 'Dismiss Recommendation?'}
                    </AlertDialogTitle>
                    <AlertDialogDescription asChild>
                        <div className="space-y-4">
                            <p className="text-sm text-muted-foreground">
                                {isApply
                                    ? 'Are you sure you want to apply this recommendation?'
                                    : 'Are you sure you want to dismiss this recommendation?'}
                            </p>

                            {/* Recommendation Details */}
                            <div className="space-y-3 pt-2">
                                <div>
                                    <p className="text-xs font-semibold text-muted-foreground uppercase mb-1">
                                        Recommendation
                                    </p>
                                    <p className="text-sm font-medium text-foreground">
                                        {recommendation.title}
                                    </p>
                                </div>

                                {isApply && (
                                    <>
                                        {/* Impact & Confidence */}
                                        <div className="flex gap-4">
                                            <div>
                                                <p className="text-xs font-semibold text-muted-foreground uppercase mb-1">
                                                    Estimated Impact
                                                </p>
                                                <Badge
                                                    variant={
                                                        recommendation.estimated_impact >= 50
                                                            ? 'destructive'
                                                            : recommendation.estimated_impact >= 25
                                                                ? 'default'
                                                                : 'default'
                                                    }
                                                >
                                                    {recommendation.estimated_impact.toFixed(0)}% improvement
                                                </Badge>
                                            </div>
                                            <div>
                                                <p className="text-xs font-semibold text-muted-foreground uppercase mb-1">
                                                    Confidence
                                                </p>
                                                <Badge variant="outline">
                                                    {(recommendation.confidence * 100).toFixed(0)}%
                                                </Badge>
                                            </div>
                                        </div>

                                        {/* SQL Suggestion */}
                                        {recommendation.sql_suggestion && (
                                            <div>
                                                <p className="text-xs font-semibold text-muted-foreground uppercase mb-2">
                                                    SQL Suggestion
                                                </p>
                                                <div className="rounded-lg overflow-hidden border border-border">
                                                    <SyntaxHighlighter
                                                        language="sql"
                                                        style={vscDarkPlus}
                                                        customStyle={{
                                                            margin: 0,
                                                            fontSize: '0.75rem',
                                                            padding: '0.75rem',
                                                            maxHeight: '200px',
                                                        }}
                                                    >
                                                        {recommendation.sql_suggestion}
                                                    </SyntaxHighlighter>
                                                </div>
                                            </div>
                                        )}
                                    </>
                                )}

                                {/* Warning */}
                                <div className="bg-muted/50 border border-border rounded-lg p-3">
                                    <p className="text-xs text-muted-foreground">
                                        {isApply ? (
                                            <>
                                                ⚠️ <strong>This action cannot be undone.</strong> The
                                                recommendation will be marked as applied.
                                            </>
                                        ) : (
                                            <>
                                                This will hide the recommendation from your list. You can view
                                                dismissed recommendations in the history.
                                            </>
                                        )}
                                    </p>
                                </div>
                            </div>
                        </div>
                    </AlertDialogDescription>
                </AlertDialogHeader>
                <AlertDialogFooter>
                    <AlertDialogCancel disabled={isLoading}>Cancel</AlertDialogCancel>
                    <AlertDialogAction
                        onClick={(e) => {
                            e.preventDefault()
                            onConfirm()
                        }}
                        disabled={isLoading}
                        className={isApply ? '' : 'bg-destructive text-destructive-foreground hover:bg-destructive/90'}
                    >
                        {isLoading ? (
                            <>
                                <Loader2 className="w-4 h-4 animate-spin mr-2" />
                                {isApply ? 'Applying...' : 'Dismissing...'}
                            </>
                        ) : (
                            <>{isApply ? 'Apply' : 'Dismiss'}</>
                        )}
                    </AlertDialogAction>
                </AlertDialogFooter>
            </AlertDialogContent>
        </AlertDialog>
    )
}

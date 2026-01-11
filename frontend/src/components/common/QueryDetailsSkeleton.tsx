import { Card, CardContent, CardHeader } from '@/components/ui/card'
import { Skeleton } from '@/components/ui/skeleton'

export function QueryDetailsSkeleton() {
    return (
        <div className="space-y-6 p-8">
            {/* Header with Back Button */}
            <div className="flex items-center gap-4">
                <Skeleton className="h-8 w-8 rounded" />
                <Skeleton className="h-8 w-64" />
            </div>

            {/* Main Content Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Left Column - Query Details */}
                <div className="lg:col-span-2 space-y-6">
                    {/* Query Info Card */}
                    <Card>
                        <CardHeader>
                            <Skeleton className="h-6 w-32" />
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <div>
                                <Skeleton className="h-4 w-24 mb-2" />
                                <Skeleton className="h-32 w-full rounded-lg" />
                            </div>
                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                    <Skeleton className="h-3 w-20 mb-2" />
                                    <Skeleton className="h-4 w-32" />
                                </div>
                                <div>
                                    <Skeleton className="h-3 w-20 mb-2" />
                                    <Skeleton className="h-4 w-24" />
                                </div>
                            </div>
                        </CardContent>
                    </Card>

                    {/* Metrics Cards */}
                    <div className="grid grid-cols-3 gap-4">
                        {[...Array(3)].map((_, i) => (
                            <Card key={i}>
                                <CardContent className="p-4">
                                    <Skeleton className="h-3 w-20 mb-2" />
                                    <Skeleton className="h-6 w-16" />
                                </CardContent>
                            </Card>
                        ))}
                    </div>

                    {/* Execution Plan */}
                    <Card>
                        <CardHeader>
                            <Skeleton className="h-6 w-40" />
                        </CardHeader>
                        <CardContent>
                            <Skeleton className="h-48 w-full rounded-lg" />
                        </CardContent>
                    </Card>
                </div>

                {/* Right Column - Recommendations */}
                <div className="space-y-6">
                    <Card className="border-t-4 border-t-amber-500">
                        <CardHeader>
                            <Skeleton className="h-6 w-48" />
                        </CardHeader>
                        <CardContent className="space-y-4">
                            {[...Array(2)].map((_, i) => (
                                <div key={i} className="space-y-3 p-4 border rounded-lg">
                                    <div className="flex justify-between">
                                        <Skeleton className="h-5 w-40" />
                                        <Skeleton className="h-5 w-20" />
                                    </div>
                                    <Skeleton className="h-16 w-full" />
                                    <div className="flex gap-2">
                                        <Skeleton className="h-8 flex-1" />
                                        <Skeleton className="h-8 flex-1" />
                                    </div>
                                </div>
                            ))}
                        </CardContent>
                    </Card>
                </div>
            </div>
        </div>
    )
}

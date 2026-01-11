import { Card, CardContent } from '@/components/ui/card'
import { Skeleton } from '@/components/ui/skeleton'

export function QueriesSkeleton() {
    return (
        <div className="space-y-6 p-8">
            {/* Header */}
            <Skeleton className="h-8 w-48" />

            {/* Search and Filters */}
            <div className="flex flex-col md:flex-row gap-4">
                <Skeleton className="h-10 flex-1" />
                <Skeleton className="h-10 w-32" />
                <Skeleton className="h-10 w-32" />
            </div>

            {/* Filters Row */}
            <div className="flex gap-4">
                <Skeleton className="h-10 w-40" />
                <Skeleton className="h-10 w-40" />
                <Skeleton className="h-10 flex-1" />
            </div>

            {/* Table */}
            <Card>
                <CardContent className="p-6">
                    <div className="space-y-3">
                        {/* Table Header */}
                        <div className="flex gap-4 pb-3 border-b">
                            <Skeleton className="h-4 w-1/3" />
                            <Skeleton className="h-4 w-24" />
                            <Skeleton className="h-4 w-24" />
                            <Skeleton className="h-4 w-24" />
                        </div>

                        {/* Table Rows */}
                        {[...Array(10)].map((_, i) => (
                            <div key={i} className="flex items-center gap-4 py-3">
                                <Skeleton className="h-16 flex-1" />
                                <Skeleton className="h-6 w-20" />
                                <Skeleton className="h-6 w-24" />
                                <Skeleton className="h-6 w-24" />
                            </div>
                        ))}
                    </div>
                </CardContent>
            </Card>

            {/* Pagination */}
            <div className="flex justify-between items-center">
                <Skeleton className="h-8 w-32" />
                <div className="flex gap-2">
                    <Skeleton className="h-8 w-8" />
                    <Skeleton className="h-8 w-8" />
                    <Skeleton className="h-8 w-8" />
                </div>
                <Skeleton className="h-8 w-32" />
            </div>
        </div>
    )
}

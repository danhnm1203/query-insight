import { ChevronLeft, ChevronRight } from 'lucide-react'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../ui/select'
import { Button } from '../ui/button'

interface QueryPaginationProps {
    currentPage: number
    totalPages: number
    pageSize: number
    totalItems: number
    onPageChange: (page: number) => void
    onPageSizeChange: (size: number) => void
}

export function QueryPagination({
    currentPage,
    totalPages,
    pageSize,
    totalItems,
    onPageChange,
    onPageSizeChange
}: QueryPaginationProps) {
    const startItem = totalItems === 0 ? 0 : (currentPage - 1) * pageSize + 1
    const endItem = Math.min(currentPage * pageSize, totalItems)

    if (totalItems === 0) {
        return null
    }

    return (
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4 py-4">
            <div className="text-sm text-muted-foreground">
                Showing <span className="font-medium text-foreground">{startItem}-{endItem}</span> of{' '}
                <span className="font-medium text-foreground">{totalItems}</span> queries
            </div>

            <div className="flex items-center gap-4">
                {/* Page Size Selector */}
                <div className="flex items-center gap-2">
                    <span className="text-sm text-muted-foreground">Rows:</span>
                    <Select
                        value={pageSize.toString()}
                        onValueChange={(value) => onPageSizeChange(Number(value))}
                    >
                        <SelectTrigger className="w-20 h-9">
                            <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectItem value="10">10</SelectItem>
                            <SelectItem value="25">25</SelectItem>
                            <SelectItem value="50">50</SelectItem>
                            <SelectItem value="100">100</SelectItem>
                        </SelectContent>
                    </Select>
                </div>

                {/* Page Navigation */}
                <div className="flex items-center gap-2">
                    <Button
                        variant="outline"
                        size="sm"
                        onClick={() => onPageChange(currentPage - 1)}
                        disabled={currentPage === 1}
                        className="h-9"
                    >
                        <ChevronLeft className="w-4 h-4" />
                        <span className="hidden sm:inline ml-1">Prev</span>
                    </Button>

                    <span className="text-sm font-medium px-2">
                        Page {currentPage} of {totalPages}
                    </span>

                    <Button
                        variant="outline"
                        size="sm"
                        onClick={() => onPageChange(currentPage + 1)}
                        disabled={currentPage === totalPages}
                        className="h-9"
                    >
                        <span className="hidden sm:inline mr-1">Next</span>
                        <ChevronRight className="w-4 h-4" />
                    </Button>
                </div>
            </div>
        </div>
    )
}

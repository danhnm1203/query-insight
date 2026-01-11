import { Filter, X } from 'lucide-react'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../ui/select'
import { Button } from '../ui/button'
import { Slider } from '../ui/slider'

export interface QueryFilters {
    status: 'all' | 'slow' | 'normal'
    timeRange: '1h' | '6h' | '24h' | '7d' | '30d'
    executionTimeMax: number
}

interface QueryFiltersProps {
    filters: QueryFilters
    onChange: (filters: QueryFilters) => void
}

export function QueryFilters({ filters, onChange }: QueryFiltersProps) {
    const hasActiveFilters = filters.status !== 'all' || filters.timeRange !== '24h' || filters.executionTimeMax !== 10000

    const handleClearFilters = () => {
        onChange({
            status: 'all',
            timeRange: '24h',
            executionTimeMax: 10000
        })
    }

    return (
        <div className="flex flex-wrap items-center gap-3 p-4 bg-accent/50 rounded-xl border border-border">
            <div className="flex items-center gap-2 text-sm font-semibold">
                <Filter className="w-4 h-4" />
                Filters:
            </div>

            {/* Status Filter */}
            <Select
                value={filters.status}
                onValueChange={(value: any) => onChange({ ...filters, status: value })}
            >
                <SelectTrigger className="w-36 h-9">
                    <SelectValue />
                </SelectTrigger>
                <SelectContent>
                    <SelectItem value="all">All Queries</SelectItem>
                    <SelectItem value="slow">
                        <div className="flex items-center gap-2">
                            <span className="w-2 h-2 rounded-full bg-rose-500"></span>
                            Slow Only
                        </div>
                    </SelectItem>
                    <SelectItem value="normal">
                        <div className="flex items-center gap-2">
                            <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
                            Normal Only
                        </div>
                    </SelectItem>
                </SelectContent>
            </Select>

            {/* Time Range Filter */}
            <Select
                value={filters.timeRange}
                onValueChange={(value: any) => onChange({ ...filters, timeRange: value })}
            >
                <SelectTrigger className="w-32 h-9">
                    <SelectValue />
                </SelectTrigger>
                <SelectContent>
                    <SelectItem value="1h">Last 1 hour</SelectItem>
                    <SelectItem value="6h">Last 6 hours</SelectItem>
                    <SelectItem value="24h">Last 24 hours</SelectItem>
                    <SelectItem value="7d">Last 7 days</SelectItem>
                    <SelectItem value="30d">Last 30 days</SelectItem>
                </SelectContent>
            </Select>

            {/* Execution Time Filter */}
            <div className="flex items-center gap-3 min-w-[200px]">
                <span className="text-xs text-muted-foreground whitespace-nowrap">
                    Max: {filters.executionTimeMax}ms
                </span>
                <Slider
                    value={[filters.executionTimeMax]}
                    onValueChange={([value]) => onChange({ ...filters, executionTimeMax: value })}
                    min={0}
                    max={10000}
                    step={100}
                    className="flex-1"
                />
            </div>

            {/* Clear Filters */}
            {hasActiveFilters && (
                <Button
                    variant="ghost"
                    size="sm"
                    onClick={handleClearFilters}
                    className="h-9"
                >
                    <X className="w-4 h-4 mr-1" />
                    Clear Filters
                </Button>
            )}
        </div>
    )
}

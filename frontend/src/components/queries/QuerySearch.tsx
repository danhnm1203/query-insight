import { useState, useEffect } from 'react'
import { Search, X } from 'lucide-react'
import { Input } from '../ui/input'

interface QuerySearchProps {
    value: string
    onChange: (value: string) => void
    placeholder?: string
}

export function QuerySearch({ value, onChange, placeholder = "Search queries by SQL text..." }: QuerySearchProps) {
    const [localValue, setLocalValue] = useState(value)

    // Debounce search - wait 300ms after user stops typing
    useEffect(() => {
        const timer = setTimeout(() => {
            onChange(localValue)
        }, 300)

        return () => clearTimeout(timer)
    }, [localValue, onChange])

    // Sync with external value changes
    useEffect(() => {
        setLocalValue(value)
    }, [value])

    const handleClear = () => {
        setLocalValue('')
        onChange('')
    }

    return (
        <div className="relative w-full max-w-md">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
            <Input
                value={localValue}
                onChange={(e) => setLocalValue(e.target.value)}
                placeholder={placeholder}
                className="pl-10 pr-10"
            />
            {localValue && (
                <button
                    onClick={handleClear}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors"
                >
                    <X className="w-4 h-4" />
                </button>
            )}
        </div>
    )
}

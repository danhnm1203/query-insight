import React, { useState } from 'react'
import { Check, ChevronsUpDown, Database, Database as DbIcon, Clock } from 'lucide-react'
import { useDatabaseStore } from '../../store/useDatabaseStore'
import { cn } from '../../lib/utils'
import { Button } from '../ui/button'
import {
    Command,
    CommandEmpty,
    CommandGroup,
    CommandInput,
    CommandItem,
    CommandList,
} from '../ui/command'
import {
    Popover,
    PopoverContent,
    PopoverTrigger,
} from '../ui/popover'
import { formatDistanceToNow } from 'date-fns'

interface DatabaseSelectorProps {
    className?: string
}

const DatabaseSelector: React.FC<DatabaseSelectorProps> = ({ className }) => {
    const [open, setOpen] = useState(false)
    const { databases, selectedDatabaseId, setSelectedDatabaseId } = useDatabaseStore()

    const selectedDatabase = databases.find((db) => db.id === selectedDatabaseId)

    const getDbIcon = (_type?: string) => {
        // You can add brand specific icons here if you have them
        return <DbIcon className="w-4 h-4" />
    }

    return (
        <Popover open={open} onOpenChange={setOpen}>
            <PopoverTrigger asChild>
                <Button
                    variant="outline"
                    role="combobox"
                    aria-expanded={open}
                    className={cn(
                        "w-[280px] justify-between h-12 rounded-xl border-border bg-card hover:bg-accent transition-all pl-3 pr-2",
                        className
                    )}
                >
                    <div className="flex items-center gap-3 overflow-hidden">
                        <div className="p-2 rounded-lg bg-primary/10 text-primary shrink-0">
                            {selectedDatabase ? getDbIcon(selectedDatabase.type) : <Database className="w-4 h-4" />}
                        </div>
                        <div className="flex flex-col items-start overflow-hidden">
                            <span className="font-bold text-sm truncate w-full">
                                {selectedDatabase ? selectedDatabase.name : "Select database..."}
                            </span>
                            {selectedDatabase && (
                                <span className="text-[10px] text-muted-foreground uppercase tracking-wider font-medium">
                                    {selectedDatabase.type}
                                </span>
                            )}
                        </div>
                    </div>
                    <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
                </Button>
            </PopoverTrigger>
            <PopoverContent
                className="w-[320px] p-0 rounded-2xl border border-border bg-white dark:bg-slate-950 shadow-[0_20px_50px_rgba(0,0,0,0.2)] overflow-hidden animate-in fade-in-0 zoom-in-95 duration-200"
                align="start"
                sideOffset={8}
            >
                <Command className="rounded-2xl bg-transparent">
                    <div className="flex items-center border-b border-border px-3">
                        <CommandInput
                            placeholder="Search databases..."
                            className="flex h-12 w-full rounded-md bg-transparent py-3 text-sm outline-none placeholder:text-muted-foreground disabled:cursor-not-allowed disabled:opacity-50 border-none focus:ring-0"
                        />
                    </div>
                    <CommandList className="max-h-[400px]">
                        <CommandEmpty className="py-6 text-center text-sm text-muted-foreground">
                            No database found.
                        </CommandEmpty>
                        <CommandGroup heading="Connections" className="p-2">
                            {databases.map((db) => (
                                <CommandItem
                                    key={db.id}
                                    value={db.name}
                                    onSelect={() => {
                                        setSelectedDatabaseId(db.id)
                                        setOpen(false)
                                    }}
                                    className="px-4 py-3 cursor-pointer"
                                >
                                    <div className="flex items-center gap-3 flex-1 overflow-hidden">
                                        <div className={cn(
                                            "p-2 rounded-lg shrink-0",
                                            selectedDatabaseId === db.id ? "bg-primary text-primary-foreground" : "bg-accent text-accent-foreground"
                                        )}>
                                            {getDbIcon(db.type)}
                                        </div>
                                        <div className="flex flex-col flex-1 overflow-hidden">
                                            <div className="flex items-center gap-2">
                                                <span className="font-bold text-sm truncate">{db.name}</span>
                                                {db.is_active && (
                                                    <div className="w-2 h-2 rounded-full bg-emerald-500" />
                                                )}
                                            </div>
                                            <div className="flex items-center gap-3 text-[10px] text-muted-foreground/80 font-medium">
                                                <span className="flex items-center gap-1.5">
                                                    <Clock className="w-3 h-3 opacity-70" />
                                                    {db.last_collection_at
                                                        ? formatDistanceToNow(new Date(db.last_collection_at), { addSuffix: true })
                                                        : 'No sync data'
                                                    }
                                                </span>
                                            </div>
                                        </div>
                                        {selectedDatabaseId === db.id && (
                                            <Check className="h-4 w-4 text-primary shrink-0" />
                                        )}
                                    </div>
                                </CommandItem>
                            ))}
                        </CommandGroup>
                    </CommandList>
                </Command>
            </PopoverContent>
        </Popover>
    )
}

export default DatabaseSelector

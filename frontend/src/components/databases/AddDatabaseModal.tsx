import React, { useState } from 'react'
import { useDatabaseStore } from '../../store/useDatabaseStore'
import { api } from '../../lib/api'
import { X, Loader2, Database, Shield, Zap, Sparkles } from 'lucide-react'
import { DATABASE_PRESETS, type DatabasePresetKey } from '../../lib/database-presets'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../ui/select'

interface AddDatabaseModalProps {
    isOpen: boolean
    onClose: () => void
}

const AddDatabaseModal: React.FC<AddDatabaseModalProps> = ({ isOpen, onClose }) => {
    const { addDatabase, isLoading, error } = useDatabaseStore()
    const [name, setName] = useState('')
    const [type, setType] = useState('postgres')
    const [connectionString, setConnectionString] = useState('')
    const [isTesting, setIsTesting] = useState(false)
    const [testResult, setTestResult] = useState<{ success: boolean; message: string } | null>(null)
    const [selectedPreset, setSelectedPreset] = useState<DatabasePresetKey | ''>('')

    const handleTestConnection = async () => {
        setIsTesting(true)
        setTestResult(null)
        try {
            await api.testConnection({ type, connection_string: connectionString })
            setTestResult({ success: true, message: 'Connection successful!' })
        } catch (err: any) {
            const message = err.response?.data?.detail || 'Connection failed'
            setTestResult({ success: false, message })
        } finally {
            setIsTesting(false)
        }
    }

    const handlePresetSelect = (presetKey: string) => {
        if (!presetKey) {
            setSelectedPreset('')
            return
        }

        const preset = DATABASE_PRESETS[presetKey as DatabasePresetKey]
        if (preset) {
            setSelectedPreset(presetKey as DatabasePresetKey)
            setType(preset.type)
            setConnectionString(preset.defaultConnectionString)
            setTestResult(null)
        }
    }

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        try {
            await addDatabase({
                name,
                type,
                connection_string: connectionString
            })
            onClose()
            setName('')
            setConnectionString('')
            setTestResult(null)
        } catch (err) {
            // Error is handled by store
        }
    }

    if (!isOpen) return null

    return (
        <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-background/80 backdrop-blur-sm animate-in fade-in duration-300">
            <div className="w-full max-w-lg bg-card border border-border rounded-3xl shadow-2xl overflow-hidden animate-in zoom-in-95 duration-300">
                <div className="px-6 py-4 border-b border-border flex items-center justify-between bg-accent/50">
                    <h2 className="text-xl font-bold flex items-center gap-2">
                        <Database className="w-5 h-5 text-primary" />
                        Connect New Database
                    </h2>
                    <button
                        onClick={onClose}
                        className="p-1 rounded-lg hover:bg-accent text-muted-foreground transition-colors"
                    >
                        <X className="w-6 h-6" />
                    </button>
                </div>

                <form onSubmit={handleSubmit} className="p-6 space-y-6">
                    {error && (
                        <div className="p-4 bg-destructive/10 text-destructive rounded-xl border border-destructive/20 text-sm">
                            {error}
                        </div>
                    )}

                    {testResult && (
                        <div className={`p-4 rounded-xl border text-sm animate-in fade-in slide-in-from-top-2 ${testResult.success
                            ? 'bg-emerald-500/10 text-emerald-500 border-emerald-500/20'
                            : 'bg-destructive/10 text-destructive border-destructive/20'
                            }`}>
                            {testResult.message}
                        </div>
                    )}

                    <div className="space-y-4">
                        {/* Connection Preset Selector */}
                        <div className="space-y-2">
                            <label className="text-sm font-semibold flex items-center gap-2">
                                <Sparkles className="w-4 h-4 text-primary" />
                                Quick Start (Optional)
                            </label>
                            <Select value={selectedPreset} onValueChange={handlePresetSelect}>
                                <SelectTrigger className="w-full h-11">
                                    <SelectValue placeholder="Choose a database preset..." />
                                </SelectTrigger>
                                <SelectContent>
                                    <SelectItem value="">None (Manual Setup)</SelectItem>
                                    {Object.entries(DATABASE_PRESETS).map(([key, preset]) => (
                                        <SelectItem key={key} value={key}>
                                            {`${preset.name} - ${preset.description}`}
                                        </SelectItem>
                                    ))}
                                </SelectContent>
                            </Select>
                            {selectedPreset && (
                                <p className="text-xs text-muted-foreground flex items-center gap-1">
                                    ✨ Auto-filled connection template for {DATABASE_PRESETS[selectedPreset].name}
                                </p>
                            )}
                        </div>

                        <div className="space-y-2">
                            <label className="text-sm font-semibold">Database Name</label>
                            <input
                                required
                                value={name}
                                onChange={(e) => setName(e.target.value)}
                                className="w-full h-11 bg-background border border-input rounded-xl px-4 text-sm focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all outline-none"
                                placeholder="e.g. Production PostgreSQL"
                            />
                        </div>

                        <div className="space-y-2">
                            <label className="text-sm font-semibold">Database Type</label>
                            <div className="grid grid-cols-3 gap-3">
                                {['postgres', 'mysql', 'mongodb'].map((dbType) => (
                                    <button
                                        key={dbType}
                                        type="button"
                                        onClick={() => setType(dbType)}
                                        className={`py-2 rounded-xl text-xs font-bold uppercase tracking-wider border transition-all ${type === dbType
                                            ? 'bg-primary/10 border-primary text-primary shadow-sm'
                                            : 'border-border hover:border-primary/50 text-muted-foreground'
                                            }`}
                                    >
                                        {dbType}
                                    </button>
                                ))}
                            </div>
                        </div>

                        <div className="space-y-2">
                            <label className="text-sm font-semibold">Connection String</label>
                            <div className="relative">
                                <textarea
                                    required
                                    value={connectionString}
                                    onChange={(e) => setConnectionString(e.target.value)}
                                    className="w-full bg-background border border-input rounded-xl px-4 py-3 text-sm focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all outline-none min-h-[100px] font-mono"
                                    placeholder="postgresql://user:password@host:port/dbname"
                                />
                            </div>
                            <div className="flex items-start gap-2 p-3 bg-accent rounded-xl">
                                <Shield className="w-4 h-4 text-emerald-500 mt-0.5 shrink-0" />
                                <p className="text-[12px] text-muted-foreground">
                                    Your connection strings are encrypted before being stored. We only use them to collect performance statistics and metadata.
                                </p>
                            </div>
                        </div>
                    </div>

                    <div className="flex gap-3 pt-2">
                        <button
                            type="button"
                            onClick={handleTestConnection}
                            disabled={isTesting || !connectionString}
                            className="flex-1 h-12 rounded-xl font-bold border border-border hover:bg-accent transition-all flex items-center justify-center gap-2 disabled:opacity-50"
                        >
                            {isTesting ? (
                                <Loader2 className="w-5 h-5 animate-spin" />
                            ) : (
                                'Test'
                            )}
                        </button>
                        <button
                            type="submit"
                            disabled={isLoading}
                            className="flex-[2] h-12 bg-primary text-primary-foreground rounded-xl font-bold shadow-lg shadow-primary/20 hover:opacity-90 disabled:opacity-50 transition-all flex items-center justify-center gap-2"
                        >
                            {isLoading ? (
                                <Loader2 className="w-5 h-5 animate-spin" />
                            ) : (
                                <>
                                    <Zap className="w-5 h-5" />
                                    Connect
                                </>
                            )}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    )
}

export default AddDatabaseModal

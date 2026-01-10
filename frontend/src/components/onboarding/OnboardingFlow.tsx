import React, { useState } from 'react'
import { Check, Database, Activity, Info, X } from 'lucide-react'

interface OnboardingFlowProps {
    onComplete: () => void
}

const OnboardingFlow: React.FC<OnboardingFlowProps> = ({ onComplete }) => {
    const [step, setStep] = useState(1)

    const steps = [
        {
            id: 1,
            title: 'Welcome to QueryInsight',
            description: 'The intelligent layer for your database performance. Follow this quick guide to get started.',
            icon: <Info className="w-12 h-12 text-blue-400" />,
            content: (
                <div className="space-y-4 text-slate-300">
                    <p>QueryInsight helps you identify bottlenecks in your database by:</p>
                    <ul className="space-y-2">
                        <li className="flex items-start gap-2">
                            <Check className="w-5 h-5 text-emerald-400 mt-0.5 shrink-0" />
                            <span>Automatically detecting slow queries using SQL fingerprinting.</span>
                        </li>
                        <li className="flex items-start gap-2">
                            <Check className="w-5 h-5 text-emerald-400 mt-0.5 shrink-0" />
                            <span>Providing AI-powered indexing recommendations.</span>
                        </li>
                        <li className="flex items-start gap-2">
                            <Check className="w-5 h-5 text-emerald-400 mt-0.5 shrink-0" />
                            <span>Tracking performance trends over time.</span>
                        </li>
                    </ul>
                </div>
            )
        },
        {
            id: 2,
            title: 'Connect Your Database',
            description: 'We support PostgreSQL, MySQL, and MongoDB. You just need a connection string.',
            icon: <Database className="w-12 h-12 text-purple-400" />,
            content: (
                <div className="space-y-4 text-slate-300">
                    <p>To connect a database, go to the <strong>Databases</strong> tab and click "Add Database".</p>
                    <div className="p-4 bg-slate-800 rounded-lg border border-slate-700">
                        <p className="text-sm font-mono text-slate-400">
                            postgresql://user:password@host:port/dbname
                        </p>
                    </div>
                    <p className="text-sm italic">QueryInsight uses read-only access where possible and encrypts all connection strings at rest.</p>
                </div>
            )
        },
        {
            id: 3,
            title: 'Monitor & Optimize',
            description: 'Once connected, our collectors will start analyzing your slow query logs.',
            icon: <Activity className="w-12 h-12 text-emerald-400" />,
            content: (
                <div className="space-y-4 text-slate-300">
                    <p>Visit your <strong>Dashboard</strong> to see real-time metrics and the <strong>Intelligence</strong> section for detected patterns and regressions.</p>
                    <div className="flex justify-center py-4">
                        <div className="grid grid-cols-2 gap-4 w-full max-w-sm">
                            <div className="h-24 bg-slate-800 rounded-lg animate-pulse"></div>
                            <div className="h-24 bg-slate-800 rounded-lg animate-pulse delay-75"></div>
                        </div>
                    </div>
                    <p>Ready to boost your database performance?</p>
                </div>
            )
        }
    ]

    const currentStep = steps[step - 1]

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/80 backdrop-blur-sm p-4">
            <div className="bg-slate-900 border border-slate-800 rounded-3xl w-full max-w-2xl overflow-hidden shadow-2xl">
                <div className="p-8">
                    <div className="flex justify-between items-start mb-8">
                        <div>
                            <div className="mb-4">{currentStep.icon}</div>
                            <h2 className="text-3xl font-bold mb-2">{currentStep.title}</h2>
                            <p className="text-slate-400">{currentStep.description}</p>
                        </div>
                        <button
                            onClick={onComplete}
                            className="p-2 hover:bg-slate-800 rounded-full transition-colors"
                        >
                            <X className="w-6 h-6 text-slate-500" />
                        </button>
                    </div>

                    <div className="min-h-[200px] mb-12">
                        {currentStep.content}
                    </div>

                    <div className="flex items-center justify-between">
                        <div className="flex gap-2">
                            {steps.map((s) => (
                                <div
                                    key={s.id}
                                    className={`h-1.5 rounded-full transition-all ${s.id === step ? 'w-8 bg-blue-500' : 'w-2 bg-slate-700'
                                        }`}
                                />
                            ))}
                        </div>

                        <div className="flex gap-4">
                            {step > 1 && (
                                <button
                                    onClick={() => setStep(step - 1)}
                                    className="px-6 py-2 rounded-xl text-slate-400 hover:text-white font-medium transition-colors"
                                >
                                    Previous
                                </button>
                            )}
                            <button
                                onClick={() => {
                                    if (step < steps.length) {
                                        setStep(step + 1)
                                    } else {
                                        onComplete()
                                    }
                                }}
                                className="px-8 py-2 bg-blue-600 hover:bg-blue-500 rounded-xl font-bold transition-all shadow-lg shadow-blue-500/20"
                            >
                                {step === steps.length ? 'Get Started' : 'Next'}
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default OnboardingFlow

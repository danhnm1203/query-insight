import React from 'react'
import { Check, Zap, Globe, Shield } from 'lucide-react'
import { api } from '../lib/api'

const PricingPage: React.FC = () => {
    const plans = [
        {
            name: 'Free',
            price: '$0',
            description: 'For hobbyists and small projects',
            features: ['1 Database connection', 'Basic query patterns', '24h retention', 'Community support'],
            icon: <Zap className="w-6 h-6 text-blue-400" />,
            tier: 'free',
            buttonText: 'Current Plan',
            popular: false
        },
        {
            name: 'Starter',
            price: '$49',
            description: 'For growing applications',
            features: ['3 Database connections', 'Advanced trend analysis', '7-day retention', 'Email support'],
            icon: <Shield className="w-6 h-6 text-indigo-400" />,
            tier: 'starter',
            buttonText: 'Get Started',
            popular: true
        },
        {
            name: 'Pro',
            price: '$149',
            description: 'For professional teams',
            features: ['10 Database connections', 'AI recommendations (Beta)', '30-day retention', 'Priority support'],
            icon: <Globe className="w-6 h-6 text-purple-400" />,
            tier: 'pro',
            buttonText: 'Upgrade to Pro',
            popular: false
        }
    ]

    const handleUpgrade = async (tier: string) => {
        if (tier === 'free') return

        try {
            const { checkout_url } = await api.createCheckoutSession(
                tier,
                window.location.origin + '/dashboard?checkout=success',
                window.location.origin + '/pricing?checkout=cancel'
            )
            window.location.href = checkout_url
        } catch (error) {
            console.error('Failed to create checkout session:', error)
            alert('Failed to initiate checkout. Please try again.')
        }
    }

    return (
        <div className="min-h-screen bg-slate-950 text-white py-20 px-4">
            <div className="max-w-6xl mx-auto text-center mb-16">
                <h1 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent mb-4">
                    Simple, Transparent Pricing
                </h1>
                <p className="text-slate-400 text-lg">
                    Choose the plan that's right for your database needs.
                </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
                {plans.map((plan) => (
                    <div
                        key={plan.name}
                        className={`relative p-8 rounded-2xl bg-slate-900 border ${plan.popular ? 'border-blue-500' : 'border-slate-800'
                            } flex flex-col`}
                    >
                        {plan.popular && (
                            <div className="absolute top-0 right-8 -translate-y-1/2 bg-blue-500 text-white px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider">
                                Most Popular
                            </div>
                        )}

                        <div className="mb-8">
                            <div className="mb-4">{plan.icon}</div>
                            <h3 className="text-2xl font-bold mb-2">{plan.name}</h3>
                            <p className="text-slate-400 text-sm">{plan.description}</p>
                        </div>

                        <div className="mb-8 flex items-baseline gap-1">
                            <span className="text-4xl font-bold">{plan.price}</span>
                            <span className="text-slate-500">/month</span>
                        </div>

                        <ul className="space-y-4 mb-8 flex-grow text-sm">
                            {plan.features.map((feature) => (
                                <li key={feature} className="flex items-center gap-3 text-slate-300">
                                    <Check className="w-4 h-4 text-emerald-400" />
                                    {feature}
                                </li>
                            ))}
                        </ul>

                        <button
                            onClick={() => handleUpgrade(plan.tier)}
                            disabled={plan.tier === 'free'}
                            className={`w-full py-3 px-4 rounded-xl font-semibold transition-all ${plan.popular
                                    ? 'bg-blue-600 hover:bg-blue-500 text-white shadow-lg shadow-blue-500/20'
                                    : plan.tier === 'free'
                                        ? 'bg-slate-800 text-slate-500 cursor-default'
                                        : 'bg-white text-slate-950 hover:bg-slate-100'
                                }`}
                        >
                            {plan.buttonText}
                        </button>
                    </div>
                ))}
            </div>

            <div className="mt-16 text-center text-slate-500 text-sm">
                Need more? <a href="mailto:sales@queryinsight.com" className="text-blue-400 hover:underline">Contact Sales</a> for Enterprise options.
            </div>
        </div>
    )
}

export default PricingPage

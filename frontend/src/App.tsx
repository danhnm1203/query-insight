import { BrowserRouter as Router, Routes, Route, Navigate, Link } from 'react-router-dom'
import { useEffect } from 'react'
import { useAuthStore } from './store/useAuthStore'

import Navbar from './components/layout/Navbar'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import PrivateRoute from './components/auth/PrivateRoute'
import DatabasesPage from './pages/DatabasesPage'
import DashboardPage from './pages/DashboardPage'
import QueriesPage from './pages/QueriesPage'
import QueryDetailsPage from './pages/QueryDetailsPage'
import PricingPage from './pages/PricingPage'

function App() {
    const { checkAuth, isAuthenticated, isLoading } = useAuthStore()

    useEffect(() => {
        checkAuth()
    }, [checkAuth])

    return (
        <Router>
            <div className="min-h-screen bg-background">
                <Navbar />
                <main className="container mx-auto px-4 py-8">
                    <Routes>
                        <Route path="/" element={<Home />} />
                        <Route path="/login" element={!isAuthenticated ? <LoginPage /> : <Navigate to="/dashboard" />} />
                        <Route path="/register" element={!isAuthenticated ? <RegisterPage /> : <Navigate to="/dashboard" />} />
                        <Route path="/pricing" element={<PricingPage />} />
                        <Route
                            path="/dashboard"
                            element={
                                <PrivateRoute>
                                    <DashboardPage />
                                </PrivateRoute>
                            }
                        />
                        <Route
                            path="/databases"
                            element={
                                <PrivateRoute>
                                    <DatabasesPage />
                                </PrivateRoute>
                            }
                        />
                        <Route
                            path="/databases/:id/queries"
                            element={
                                <PrivateRoute>
                                    <QueriesPage />
                                </PrivateRoute>
                            }
                        />
                        <Route
                            path="/queries/:queryId"
                            element={
                                <PrivateRoute>
                                    <QueryDetailsPage />
                                </PrivateRoute>
                            }
                        />
                    </Routes>
                </main>
            </div>
        </Router>
    )
}

function Home() {
    return (
        <div className="max-w-4xl mx-auto text-center space-y-8 py-12 md:py-24">
            <div className="space-y-4">
                <h1 className="text-4xl md:text-6xl font-extrabold tracking-tight">
                    Optimize Your Database <br />
                    <span className="text-primary italic">Automatically</span>
                </h1>
                <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
                    Identify slow queries, get AI-powered index recommendations, and monitor metrics across all your databases in one place.
                </p>
            </div>

            <div className="flex gap-4 justify-center">
                <Link to="/register" className="px-8 py-4 bg-primary text-primary-foreground rounded-xl font-bold text-lg hover:opacity-90 transition-all shadow-lg hover:shadow-primary/20">
                    Get Started Free
                </Link>
                <button className="px-8 py-4 border border-border rounded-xl font-bold text-lg hover:bg-accent transition-all">
                    View Demo
                </button>
            </div>

            <div className="pt-24 grid md:grid-cols-3 gap-8">
                {[
                    { title: 'Any Database', desc: 'Connect PostgreSQL, MySQL, or MongoDB in seconds.' },
                    { title: 'Real-time Metrics', desc: 'Monitor QPS, execution time, and more.' },
                    { title: 'Smart Indexes', desc: 'Get proven index recommendations for slow queries.' }
                ].map((feature, i) => (
                    <div key={i} className="p-6 rounded-2xl bg-card border border-border shadow-sm text-left space-y-2">
                        <h3 className="text-lg font-bold">{feature.title}</h3>
                        <p className="text-sm text-muted-foreground">{feature.desc}</p>
                    </div>
                ))}
            </div>
        </div>
    )
}

function DashboardPlaceholder() {
    return (
        <div className="space-y-4">
            <h1 className="text-3xl font-bold">Dashboard</h1>
            <p className="text-muted-foreground">Coming soon...</p>
        </div>
    )
}

function DatabasesPlaceholder() {
    return (
        <div className="space-y-4">
            <h1 className="text-3xl font-bold">Databases</h1>
            <p className="text-muted-foreground">Coming soon...</p>
        </div>
    )
}

export default App

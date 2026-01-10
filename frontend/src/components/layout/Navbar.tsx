import React from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuthStore } from '../../store/useAuthStore'
import { LogOut, LayoutDashboard, Database, User, Menu, X, Zap } from 'lucide-react'

const Navbar: React.FC = () => {
    const { isAuthenticated, user, logout } = useAuthStore()
    const navigate = useNavigate()
    const [isMenuOpen, setIsMenuOpen] = React.useState(false)

    const handleLogout = () => {
        logout()
        navigate('/')
    }

    return (
        <nav className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
            <div className="container mx-auto px-4 h-16 flex items-center justify-between">
                <div className="flex items-center gap-8">
                    <Link to="/" className="flex items-center gap-2 font-bold text-xl text-primary transition-opacity hover:opacity-90">
                        <Database className="w-6 h-6" />
                        <span>QueryInsight</span>
                    </Link>

                    {isAuthenticated && (
                        <div className="hidden md:flex items-center gap-6">
                            <Link
                                to="/dashboard"
                                className="flex items-center gap-2 text-sm font-medium text-muted-foreground hover:text-primary transition-colors"
                            >
                                <LayoutDashboard className="w-4 h-4" />
                                Dashboard
                            </Link>
                            <Link
                                to="/databases"
                                className="flex items-center gap-2 text-sm font-medium text-muted-foreground hover:text-primary transition-colors"
                            >
                                <Database className="w-4 h-4" />
                                Databases
                            </Link>
                            <Link
                                to="/pricing"
                                className="flex items-center gap-2 text-sm font-medium text-muted-foreground hover:text-primary transition-colors"
                            >
                                <Zap className="w-4 h-4 text-amber-400" />
                                Pricing
                            </Link>
                        </div>
                    )}
                </div>

                <div className="flex items-center gap-4">
                    {isAuthenticated ? (
                        <div className="flex items-center gap-4">
                            <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-full bg-accent text-accent-foreground">
                                <User className="w-4 h-4" />
                                <span className="text-sm font-medium">{user?.email}</span>
                            </div>
                            <button
                                onClick={handleLogout}
                                className="p-2 rounded-lg text-muted-foreground hover:text-destructive hover:bg-destructive/10 transition-all"
                                title="Sign out"
                            >
                                <LogOut className="w-5 h-5" />
                            </button>
                        </div>
                    ) : (
                        <div className="flex items-center gap-3">
                            <Link
                                to="/login"
                                className="text-sm font-medium hover:text-primary transition-colors"
                            >
                                Sign In
                            </Link>
                            <Link
                                to="/pricing"
                                className="text-sm font-medium hover:text-primary transition-colors mr-4"
                            >
                                Pricing
                            </Link>
                            <Link
                                to="/register"
                                className="inline-flex h-9 items-center justify-center rounded-lg bg-primary px-4 py-2 text-sm font-medium text-primary-foreground shadow transition-colors hover:bg-primary/90 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
                            >
                                Get Started
                            </Link>
                        </div>
                    )}

                    <button
                        className="md:hidden p-2 text-muted-foreground"
                        onClick={() => setIsMenuOpen(!isMenuOpen)}
                    >
                        {isMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
                    </button>
                </div>
            </div>

            {/* Mobile Menu */}
            {isMenuOpen && isAuthenticated && (
                <div className="md:hidden border-b bg-background p-4 space-y-4 animate-in slide-in-from-top-2">
                    <Link
                        to="/dashboard"
                        className="flex items-center gap-3 text-sm font-medium p-2 rounded-lg hover:bg-accent"
                        onClick={() => setIsMenuOpen(false)}
                    >
                        <LayoutDashboard className="w-4 h-4" />
                        Dashboard
                    </Link>
                    <Link
                        to="/databases"
                        className="flex items-center gap-3 text-sm font-medium p-2 rounded-lg hover:bg-accent"
                        onClick={() => setIsMenuOpen(false)}
                    >
                        <Database className="w-4 h-4" />
                        Databases
                    </Link>
                    <Link
                        to="/pricing"
                        className="flex items-center gap-3 text-sm font-medium p-2 rounded-lg hover:bg-accent"
                        onClick={() => setIsMenuOpen(false)}
                    >
                        <Zap className="w-4 h-4 text-amber-400" />
                        Pricing
                    </Link>
                </div>
            )}
        </nav>
    )
}

export default Navbar

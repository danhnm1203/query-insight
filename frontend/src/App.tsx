import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'

function App() {
    return (
        <Router>
            <div className="min-h-screen bg-background">
                <nav className="border-b">
                    <div className="container mx-auto px-4 py-4">
                        <h1 className="text-2xl font-bold text-primary">
                            QueryInsight
                        </h1>
                    </div>
                </nav>

                <main className="container mx-auto px-4 py-8">
                    <Routes>
                        <Route path="/" element={<Home />} />
                    </Routes>
                </main>
            </div>
        </Router>
    )
}

function Home() {
    return (
        <div className="max-w-4xl mx-auto text-center space-y-6">
            <h1 className="text-4xl font-bold">
                Welcome to QueryInsight
            </h1>
            <p className="text-xl text-muted-foreground">
                Database Query Performance Analyzer
            </p>
            <p className="text-lg">
                Optimize your database queries automatically with AI-powered recommendations.
            </p>
            <div className="flex gap-4 justify-center mt-8">
                <button className="px-6 py-3 bg-primary text-primary-foreground rounded-lg font-semibold hover:opacity-90">
                    Get Started
                </button>
                <button className="px-6 py-3 border border-border rounded-lg font-semibold hover:bg-accent">
                    Learn More
                </button>
            </div>
        </div>
    )
}

export default App

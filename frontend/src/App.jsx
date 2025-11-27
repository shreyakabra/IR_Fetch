import { useState } from 'react'
import SearchForm from './components/SearchForm'
import ResultsDisplay from './components/ResultsDisplay'
import './App.css'

const API_URL = 'http://localhost:8008'

function App() {
    const [results, setResults] = useState(null)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)

    const handleSearch = async (searchData) => {
        setLoading(true)
        setError(null)
        setResults(null)

        try {
            const response = await fetch(`${API_URL}/download`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(searchData),
            })

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ detail: response.statusText }));
                let detail = errorData.detail || 'Search failed';
                if (typeof detail === 'object') {
                    detail = JSON.stringify(detail, null, 2);
                }
                throw new Error(`${detail} (${response.status})`)
            }

            const data = await response.json()
            setResults(data)
        } catch (err) {
            setError(err.message)
        } finally {
            setLoading(false)
        }
    }

    const handleReset = () => {
        setResults(null)
        setError(null)
    }

    return (
        <div className="app">
            <div className="container">
                <header className="header">
                    <h1>🔍 AI-IR_Founder</h1>
                    <p>Find annual and quarterly reports for public companies</p>
                </header>

                <SearchForm
                    onSearch={handleSearch}
                    onReset={handleReset}
                    loading={loading}
                />

                {error && (
                    <div className="error-message">
                        <strong>❌ Error:</strong> {error}
                    </div>
                )}

                {loading && (
                    <div className="loading">
                        <div className="spinner"></div>
                        <p>Searching for reports...</p>
                    </div>
                )}

                {results && !loading && (
                    <ResultsDisplay results={results} />
                )}
            </div>
        </div>
    )
}

export default App

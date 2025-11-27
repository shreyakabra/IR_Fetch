import { useState } from 'react'

function SearchForm({ onSearch, onReset, loading }) {
    const [ticker, setTicker] = useState('')
    const [reportType, setReportType] = useState('annual')
    const [startYear, setStartYear] = useState(2020)
    const [endYear, setEndYear] = useState(2024)

    const handleSubmit = (e) => {
        e.preventDefault()

        if (!ticker.trim()) {
            alert('Please enter a company ticker symbol')
            return
        }

        // Map frontend report type to backend document type
        const docTypeMap = {
            'annual': 'annual report',
            'quarterly': 'earnings release'
        }
        const docType = docTypeMap[reportType] || 'annual report'

        const prompt = `Find ${docType} for ${ticker} from ${startYear} to ${endYear}`

        onSearch({
            prompt: prompt,
            ticker: ticker.toUpperCase(),
        })
    }

    const handleReset = () => {
        setTicker('')
        setReportType('annual')
        setStartYear(2020)
        setEndYear(2024)
        onReset()
    }

    return (
        <form className="search-form" onSubmit={handleSubmit}>
            <div className="form-row">
                <div className="form-group">
                    <label htmlFor="ticker">Company Ticker *</label>
                    <input
                        id="ticker"
                        type="text"
                        placeholder="e.g., AAPL, MSFT, GOOGL"
                        value={ticker}
                        onChange={(e) => setTicker(e.target.value)}
                        disabled={loading}
                        required
                    />
                    <small>Enter the stock ticker symbol</small>
                </div>

                <div className="form-group">
                    <label htmlFor="reportType">Report Type</label>
                    <select
                        id="reportType"
                        value={reportType}
                        onChange={(e) => setReportType(e.target.value)}
                        disabled={loading}
                    >
                        <option value="annual">Annual (10-K)</option>
                        <option value="quarterly">Quarterly (10-Q)</option>
                    </select>
                </div>
            </div>

            <div className="form-row">
                <div className="form-group">
                    <label htmlFor="startYear">Start Year</label>
                    <input
                        id="startYear"
                        type="number"
                        min="2000"
                        max="2030"
                        value={startYear}
                        onChange={(e) => setStartYear(e.target.value)}
                        disabled={loading}
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="endYear">End Year</label>
                    <input
                        id="endYear"
                        type="number"
                        min="2000"
                        max="2030"
                        value={endYear}
                        onChange={(e) => setEndYear(e.target.value)}
                        disabled={loading}
                    />
                </div>
            </div>

            <div className="form-actions">
                <button
                    type="submit"
                    className="btn btn-primary"
                    disabled={loading}
                >
                    {loading ? 'Searching...' : '🔍 Search Reports'}
                </button>
                <button
                    type="button"
                    className="btn btn-secondary"
                    onClick={handleReset}
                    disabled={loading}
                >
                    Reset
                </button>
            </div>
        </form>
    )
}

export default SearchForm

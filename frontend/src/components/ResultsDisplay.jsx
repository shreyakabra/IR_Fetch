function ResultsDisplay({ results }) {
    // Backend returns: { intent: {...}, results: [...] }
    const { intent, results: downloadedFiles } = results
    const count = downloadedFiles?.length || 0

    if (count === 0) {
        return (
            <div className="results">
                <div className="results-header">
                    <h2>Search Results</h2>
                    <p className="query-info">
                        <strong>{intent.company}</strong> • {intent.doc_type} reports •
                        {intent.years?.join(', ') || 'All years'}
                    </p>
                </div>

                <div className="empty-state">
                    <p>📄 No reports found</p>
                    <small>
                        This could be because:
                        <ul>
                            <li>The company's IR page blocks scraping (robots.txt)</li>
                            <li>No reports match your search criteria</li>
                            <li>The IR page has a non-standard structure</li>
                        </ul>
                    </small>
                </div>
            </div>
        )
    }

    return (
        <div className="results">
            <div className="results-header">
                <h2>✅ Found {count} Report{count !== 1 ? 's' : ''}</h2>
                <p className="query-info">
                    <strong>{intent.company}</strong>
                    {' • '}
                    {intent.doc_type} reports • {intent.years?.join(', ') || 'All years'}
                </p>
            </div>

            <div className="reports-table">
                <table>
                    <thead>
                        <tr>
                            <th>Year</th>
                            <th>Type</th>
                            <th>Filename</th>
                            <th>Source</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        {downloadedFiles.map((file, index) => (
                            <tr key={index}>
                                <td className="year-cell">{file.year || 'N/A'}</td>
                                <td className="type-cell">
                                    <span className={`badge badge-${file.doc_type.replace(/\s+/g, '-')}`}>
                                        {file.doc_type.toUpperCase()}
                                    </span>
                                </td>
                                <td className="title-cell">{file.filename}</td>
                                <td className="source-cell">{file.source}</td>
                                <td className="action-cell">
                                    <a
                                        href={file.url}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="btn btn-small"
                                    >
                                        📑 Open PDF
                                    </a>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    )
}

export default ResultsDisplay


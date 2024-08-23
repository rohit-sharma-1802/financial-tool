import React, { useState } from 'react';
import FileUpload from './components/FileUpload';
import Results from './components/Results';

const App = () => {
    const [results, setResults] = useState(null);

    const handleResults = (data) => {
        setResults(data);
    };

    return (
        <div>
            <h1>Financial Analysis Tool</h1>
            <FileUpload onResult={handleResults} />
            {results && <Results results={results} />}
        </div>
    );
};

export default App;

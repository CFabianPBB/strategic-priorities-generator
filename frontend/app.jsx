import React from "react";
import { useState } from "react";
import ReactDOM from "react-dom/client";
import "./styles.css"; // Make sure you have this file

function App() {
  const [orgName, setOrgName] = useState("");
  const [orgWebsite, setOrgWebsite] = useState("");
  const [priorities, setPriorities] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      const apiUrl = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";
      const response = await fetch(`${apiUrl}/generate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ org_name: orgName, org_website: orgWebsite }),
      });
      const data = await response.json();
      setPriorities(data.priorities);
    } catch (error) {
      console.error("Error generating priorities:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>Strategic Priorities Generator</h1>
      <form onSubmit={handleSubmit} className="input-form">
        <input
          type="text"
          placeholder="Organization Name"
          value={orgName}
          onChange={(e) => setOrgName(e.target.value)}
          required
          className="form-input"
        />
        <input
          type="text"
          placeholder="Organization Website"
          value={orgWebsite}
          onChange={(e) => setOrgWebsite(e.target.value)}
          className="form-input"
        />
        <button type="submit" className="generate-btn">Generate</button>
      </form>
      
      {isLoading && <div className="loading">Generating priorities...</div>}
      
      {priorities.length > 0 && (
        <>
          <div className="priorities-container">
            <h2>Generated Strategic Priorities</h2>
            
            {/* Download buttons */}
            <div className="download-buttons">
              <a href={`${apiUrl}/download/word`} className="download-btn">
                Download as Word
              </a>
              <a href={`${apiUrl}/download/excel`} className="download-btn">
                Download as Excel
              </a>
            </div>
            
            {priorities.map((priority, index) => (
              <div key={index} className="priority-card">
                <h3 className="priority-title">Priority {index + 1}: {priority.priority}</h3>
                <p className="priority-description">{priority.description}</p>
                
                <h4>Key Initiatives:</h4>
                <ul className="definitions-list">
                  {priority.definitions.map((def, i) => (
                    <li key={i} className="definition-item">
                      <strong>{def.title}</strong> {def.description}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}

// Ensure React is mounting the app correctly
const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<App />);

export default App;
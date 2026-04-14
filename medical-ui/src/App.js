import React, { useState } from "react";
import axios from "axios";

function App() {
  const [file, setFile] = useState(null);
  const [summary, setSummary] = useState("");
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setSummary(""); 
  };

  const summarizePDF = async () => {
    if (!file) return;
    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post("http://127.0.0.1:5000/summarize", formData, {
        timeout: 300000 
      });
      setSummary(response.data.summary);
    } catch (error) {
      alert("Analysis failed. Please ensure the backend is active.");
    }
    setLoading(false);
  };

  const copyToClipboard = () => {
    navigator.clipboard.writeText(summary);
    alert("Clinical summary copied!");
  };

  return (
    <div style={styles.container}>
      {/* Animation Styles */}
      <style>
        {`
          @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
          }
        `}
      </style>

      <div style={styles.card}>
        <header style={{ textAlign: "center", marginBottom: "40px" }}>
          <h1 style={{ color: "#1e293b", fontSize: "32px", marginBottom: "10px" }}>Medical AI Summarizer</h1>
          <p style={{ color: "#64748b" }}>Advanced clinical record analysis powered by BioBART</p>
        </header>

        {/* Upload Area */}
        <div style={styles.uploadArea}>
          <input 
            type="file" 
            id="file-upload" 
            onChange={handleFileChange} 
            accept=".pdf" 
            style={{ display: "none" }} 
          />
          <label htmlFor="file-upload" style={{ cursor: "pointer", display: "block" }}>
            <div style={{ fontSize: "40px", marginBottom: "10px" }}>📄</div>
            {file ? (
              <span style={{ color: "#2563eb", fontWeight: "600" }}>{file.name}</span>
            ) : (
              <span style={{ color: "#64748b" }}>Click to upload patient PDF report</span>
            )}
          </label>
        </div>

        <button 
          onClick={summarizePDF} 
          disabled={loading || !file} 
          style={{
            ...styles.generateBtn,
            opacity: loading || !file ? 0.6 : 1,
            cursor: loading || !file ? "not-allowed" : "pointer",
            width: "100%"
          }}
        >
          {loading ? "Processing Document..." : "Generate AI Summary"}
        </button>

        {/* Results Container */}
        {summary && (
          <div style={styles.resultContainer}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "20px" }}>
              <h3 style={{ color: "#1e293b", margin: 0 }}>Analysis Findings</h3>
              <button onClick={copyToClipboard} style={{ background: "none", border: "none", color: "#2563eb", fontWeight: "bold", cursor: "pointer" }}>
                Copy Text
              </button>
            </div>
            
            <div style={styles.gridContainer}>
              {/* Splitting logic to create categorized cards */}
              {summary.split(/(?=Diagnosis:|Medications:|Symptoms:|Patient Name:|Age:|Gender:|Remarks:)/g).map((section, index) => (
                <div key={index} style={styles.infoCard}>
                  <p style={{ margin: 0, color: "#334155", lineHeight: "1.6" }}>{section.trim()}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

// --- Your Custom Professional Styles ---
const styles = {
  container: {
    padding: "60px 20px",
    backgroundColor: "#f0f4f8", 
    minHeight: "100vh",
    fontFamily: "'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
  },
  card: {
    maxWidth: "900px",
    margin: "0 auto",
    backgroundColor: "#ffffff",
    borderRadius: "24px",
    padding: "40px",
    boxShadow: "0 10px 40px rgba(29, 78, 216, 0.1)", 
    border: "1px solid #e2e8f0"
  },
  uploadArea: {
    border: "2px dashed #3b82f6",
    borderRadius: "16px",
    padding: "50px",
    backgroundColor: "#eff6ff",
    transition: "all 0.3s ease",
    marginBottom: "30px",
    textAlign: "center"
  },
  generateBtn: {
    background: "linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%)",
    color: "white",
    padding: "16px 32px",
    borderRadius: "12px",
    fontSize: "18px",
    fontWeight: "600",
    border: "none",
    boxShadow: "0 4px 14px 0 rgba(37, 99, 235, 0.39)"
  },
  resultContainer: {
    marginTop: "40px",
    textAlign: "left",
    animation: "fadeIn 0.5s ease-in"
  },
  gridContainer: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(300px, 1fr))",
    gap: "15px"
  },
  infoCard: {
    padding: "20px",
    backgroundColor: "#f8fafc",
    borderRadius: "12px",
    borderLeft: "4px solid #3b82f6",
    marginBottom: "15px",
    boxShadow: "0 2px 4px rgba(0,0,0,0.02)"
  }
};

export default App;
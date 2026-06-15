import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function NovabiteDashboard() {
  // Navigation State
  const [activeTab, setActiveTab] = useState('dashboard');

  // Dashboard Metrics State
  const [summary, setSummary] = useState({
    total_net_revenue: 0,
    gross_profit_margin_pct: 0,
    top_region: 'Loading...'
  });
  const [trends, setTrends] = useState([]);
  const [dashLoading, setDashLoading] = useState(true);

  // Chat Screen State
  const [question, setQuestion] = useState('');
  const [chatResults, setChatResults] = useState(null);
  const [chatLoading, setChatLoading] = useState(false);
  const [chatError, setChatError] = useState('');

  // Fetch Dashboard Data on Mount
  useEffect(() => {
    async function fetchDashboardData() {
      try {
        const [summaryRes, trendsRes] = await Promise.all([
          fetch('http://127.0.0.1:8000/api/summary'),
          fetch('http://127.0.0.1:8000/api/trends')
        ]);
        
        const summaryData = await summaryRes.json();
        const trendsData = await trendsRes.json();

        setSummary(summaryData);
        setTrends(trendsData);
      } catch (err) {
        console.error("Failed to load dashboard core metrics:", err);
      } finally {
        setDashLoading(false);
      }
    }
    fetchDashboardData();
  }, []);

  // Handle Chat Input Submit
  const handleChatSubmit = async (e) => {
    e.preventDefault();
    
    // Clean strip trailing quotes or whitespace characters from the text box
    const cleanQuestion = question.trim().replace(/^["']|["']$/g, '');
    if (!cleanQuestion) return;

    setChatLoading(true);
    setChatError('');
    setChatResults(null);

    try {
      const response = await fetch('http://127.0.0.1:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: cleanQuestion })
      });

      const resData = await response.json();
      console.log("📥 Backend Payload Arrived:", resData);
      
      if (resData.error) {
        setChatError(resData.error);
      } else if (resData.answer) {
        // Correctly save the conversational sentence string to state
        setChatResults(resData.answer);
      } else {
        setChatError("Received an unrecognized structure from the analytical server.");
      }
    } catch (err) {
      setChatError('Could not establish connection with the Text-to-SQL backend service.');
    } finally {
      setChatLoading(false);
    }
  };

  return (
    <div style={{ fontFamily: 'Segoe UI, sans-serif', backgroundColor: '#f8f9fa', minHeight: '100vh', padding: '20px', boxSizing: 'border-box' }}>
      
      {/* HEADER NAVIGATION BAR */}
      <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', backgroundColor: '#fff', padding: '15px 30px', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.05)', marginBottom: '25px' }}>
        <h2 style={{ margin: 0, color: '#1e293b' }}>🍕 Novabite Executive Portal</h2>
        <nav>
          <button 
            onClick={() => setActiveTab('dashboard')} 
            style={{ marginRight: '15px', padding: '8px 16px', borderRadius: '5px', border: 'none', backgroundColor: activeTab === 'dashboard' ? '#2563eb' : 'transparent', color: activeTab === 'dashboard' ? '#fff' : '#475569', fontWeight: 'bold', cursor: 'pointer' }}
          >
            Dashboard
          </button>
          <button 
            onClick={() => setActiveTab('chat')} 
            style={{ padding: '8px 16px', borderRadius: '5px', border: 'none', backgroundColor: activeTab === 'chat' ? '#2563eb' : 'transparent', color: activeTab === 'chat' ? '#fff' : '#475569', fontWeight: 'bold', cursor: 'pointer' }}
          >
            AI Chat Analyst
          </button>
        </nav>
      </header>

      {/* SCREEN 1: CORE DASHBOARD */}
      {activeTab === 'dashboard' && (
        <div>
          {dashLoading ? (
            <div style={{ textAlign: 'center', padding: '50px', color: '#64748b' }}>Loading dashboard analytics...</div>
          ) : (
            <>
              {/* 3 REQUIRED KPI CARDS */}
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '20px', marginBottom: '30px' }}>
                
                <div style={{ backgroundColor: '#fff', padding: '20px', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.02)', borderLeft: '5px solid #2563eb' }}>
                  <div style={{ fontSize: '14px', color: '#64748b', textTransform: 'uppercase', fontWeight: 600 }}>Total Net Revenue</div>
                  <div style={{ fontSize: '28px', fontWeight: 'bold', color: '#1e293b', marginTop: '5px' }}>
                    ${summary.total_net_revenue?.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                  </div>
                </div>

                <div style={{ backgroundColor: '#fff', padding: '20px', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.02)', borderLeft: '5px solid #10b981' }}>
                  <div style={{ fontSize: '14px', color: '#64748b', textTransform: 'uppercase', fontWeight: 600 }}>Gross Profit Margin %</div>
                  <div style={{ fontSize: '28px', fontWeight: 'bold', color: '#1e293b', marginTop: '5px' }}>
                    {summary.gross_profit_margin_pct}%
                  </div>
                </div>

                <div style={{ backgroundColor: '#fff', padding: '20px', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.02)', borderLeft: '5px solid #f59e0b' }}>
                  <div style={{ fontSize: '14px', color: '#64748b', textTransform: 'uppercase', fontWeight: 600 }}>Top Region</div>
                  <div style={{ fontSize: '28px', fontWeight: 'bold', color: '#1e293b', marginTop: '5px' }}>
                    {summary.top_region}
                  </div>
                </div>

              </div>

              {/* MONTHLY REVENUE TREND CHART */}
              <div style={{ backgroundColor: '#fff', padding: '20px', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.02)' }}>
                <h4 style={{ margin: '0 0 20px 0', color: '#334155' }}>📈 Monthly Net Revenue Performance Trend</h4>
                <div style={{ width: '100%', height: 300 }}>
                  <ResponsiveContainer>
                    <BarChart data={trends} margin={{ top: 10, right: 30, left: 20, bottom: 5 }}>
                      <CartesianGrid strokeDasharray="3 3" vertical={false} />
                      <XAxis dataKey="month" stroke="#64748b" fontSize={12} />
                      <YAxis stroke="#64748b" fontSize={12} tickFormatter={(v) => `$${v}`} />
                      <Tooltip formatter={(value) => [`$${value.toLocaleString()}`, 'Net Revenue']} />
                      <Bar dataKey="net_revenue_usd" fill="#2563eb" radius={[4, 4, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </>
          )}
        </div>
      )}

      {/* SCREEN 2: CHAT INTERFACE SCREEN */}
      {activeTab === 'chat' && (
        <div style={{ backgroundColor: '#fff', padding: '30px', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.02)', maxWidth: '800px', margin: '0 auto' }}>
          <h3 style={{ margin: '0 0 10px 0', color: '#1e293b' }}>🤖 Interactive Text-to-SQL Terminal</h3>
          <p style={{ color: '#64748b', fontSize: '14px', marginBottom: '20px' }}>
            Type any plain-English analytics question below. The background agent converts it to an active SQL statement and queries your data file safely.
          </p>

          {/* REQUIRED TEXT INPUT FIELD */}
          <form onSubmit={handleChatSubmit} style={{ display: 'flex', gap: '10px', marginBottom: '20px' }}>
            <input
              type="text"
              placeholder="Ask an analysis metric... (e.g., Show total net revenue for every region in Q1 2024)"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              disabled={chatLoading}
              style={{ flex: 1, padding: '12px 15px', borderRadius: '6px', border: '1px solid #cbd5e1', fontSize: '14px', outline: 'none' }}
            />
            <button 
              type="submit" 
              disabled={chatLoading}
              style={{ backgroundColor: '#2563eb', color: '#fff', border: 'none', padding: '0 24px', borderRadius: '6px', fontWeight: 'bold', cursor: 'pointer', fontSize: '14px', transition: 'background 0.2s' }}
            >
              {chatLoading ? 'Processing...' : 'Ask Engine'}
            </button>
          </form>

          {/* REQUIRED LOADING STATE */}
          {chatLoading && (
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', color: '#2563eb', fontSize: '14px', padding: '10px 0' }}>
              <div className="spinner" style={{ width: '18px', height: '18px', border: '3px solid #f3f3f3', borderTop: '3px solid #2563eb', borderRadius: '50%', animation: 'spin 1s linear infinite' }}></div>
              <span>Querying local SQLite instance securely via OpenRouter...</span>
              <style>{`@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }`}</style>
            </div>
          )}

          {chatError && <div style={{ color: '#ef4444', fontSize: '14px', marginTop: '15px' }}>⚠️ Error: {chatError}</div>}

          {/* CLEAN READABLE RESPONSE DISPLAY SECTION */}
          {chatResults && typeof chatResults === 'string' && (
            <div style={{ marginTop: '25px', backgroundColor: '#f8fafc', padding: '20px', borderRadius: '6px', border: '1px solid #e2e8f0', boxShadow: 'inset 0 1px 2px rgba(0,0,0,0.02)' }}>
              <div style={{ fontSize: '13px', fontWeight: 'bold', color: '#475569', textTransform: 'uppercase', marginBottom: '8px', display: 'flex', alignItems: 'center', gap: '6px' }}>
                📊 Executive Data Summary:
              </div>
              <p style={{ color: '#0f172a', margin: 0, fontSize: '15px', lineHeight: '1.6', fontWeight: '500', color: '#1e293b' }}>
                {chatResults}
              </p>
            </div>
          )}

          {/* FALLBACK IN CASE OF EMPTY VALUE */}
          {chatResults && chatResults.length === 0 && (
            <p style={{ color: '#64748b', fontSize: '14px', fontStyle: 'italic', marginTop: '20px' }}>
              The query completed successfully but no records matched your filter keys.
            </p>
          )}
        </div>
      )}

    </div>
  );
}
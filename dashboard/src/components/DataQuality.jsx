import React, { useState, useEffect } from 'react';

const DataQuality = () => {
  const [qualityData, setQualityData] = useState(null);
  const [etlSummary, setEtlSummary] = useState(null);
  const [loading, setLoading] = useState(true);

  // Note: For a static build, these JSONs should ideally be in the public/ or src/ folder as well.
  // We'll mock the fetch slightly if it fails, but assuming they are accessible via relative paths.
  
  useEffect(() => {
    // In a real deployed static site we would need these copied as well.
    // For the demo we simulate their content based on expected structure.
    setQualityData({
      initial_rows: 3060,
      missing_values_by_column: { color: 42, mileage_km: 13, customer_type: 55, discount_percent: 21 },
      duplicates_removed: 60,
      invalid_dates: 31,
      invalid_numerics: 16,
      final_rows: 2953,
      rejected_rows: 107
    });
    setEtlSummary({
      status: 'SUCCESS',
      timestamp: new Date().toISOString(),
      duration_seconds: 3.25,
      records_processed: 3060,
      records_loaded: 2953,
      mysql_load_successful: false
    });
    setLoading(false);
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      <div className="kpi-grid">
        <div className="kpi-card">
          <div className="kpi-header">
            <span>Pipeline Status</span>
          </div>
          <div className={`kpi-value ${etlSummary?.status === 'SUCCESS' ? 'text-success' : 'text-danger'}`}>
            {etlSummary?.status || 'UNKNOWN'}
          </div>
        </div>
        <div className="kpi-card">
          <div className="kpi-header">
            <span>Records Processed</span>
          </div>
          <div className="kpi-value">{qualityData?.initial_rows}</div>
        </div>
        <div className="kpi-card">
          <div className="kpi-header">
            <span>Rejected Records</span>
          </div>
          <div className="kpi-value text-danger">{qualityData?.rejected_rows}</div>
        </div>
      </div>

      <div className="chart-grid">
        <div className="chart-card">
          <h3 className="chart-title">Data Quality Report</h3>
          <ul style={{ listStyle: 'none', color: 'var(--text-muted)' }}>
            <li style={{ padding: '0.5rem 0', borderBottom: '1px solid var(--border-color)' }}>
              <strong>Duplicates Removed:</strong> {qualityData?.duplicates_removed}
            </li>
            <li style={{ padding: '0.5rem 0', borderBottom: '1px solid var(--border-color)' }}>
              <strong>Invalid Dates:</strong> {qualityData?.invalid_dates}
            </li>
            <li style={{ padding: '0.5rem 0', borderBottom: '1px solid var(--border-color)' }}>
              <strong>Invalid Numerics:</strong> {qualityData?.invalid_numerics}
            </li>
          </ul>
        </div>
        <div className="chart-card">
          <h3 className="chart-title">ETL Summary</h3>
          <ul style={{ listStyle: 'none', color: 'var(--text-muted)' }}>
            <li style={{ padding: '0.5rem 0', borderBottom: '1px solid var(--border-color)' }}>
              <strong>Execution Time:</strong> {etlSummary?.duration_seconds}s
            </li>
            <li style={{ padding: '0.5rem 0', borderBottom: '1px solid var(--border-color)' }}>
              <strong>MySQL Load:</strong> {etlSummary?.mysql_load_successful ? 'Success' : 'Skipped (No Config)'}
            </li>
            <li style={{ padding: '0.5rem 0', borderBottom: '1px solid var(--border-color)' }}>
              <strong>Timestamp:</strong> {new Date(etlSummary?.timestamp).toLocaleString()}
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default DataQuality;

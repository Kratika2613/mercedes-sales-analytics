import React, { useMemo } from 'react';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer
} from 'recharts';

const ModelPerformance = ({ data }) => {
  const modelsData = useMemo(() => {
    const grouped = {};
    data.forEach(item => {
      const model = item.model || 'Unknown';
      if (!grouped[model]) grouped[model] = { model, revenue: 0, units: 0, avgPrice: 0 };
      grouped[model].revenue += item.sale_price_inr || 0;
      grouped[model].units += 1;
    });
    
    return Object.values(grouped).map(g => {
      g.avgPrice = g.revenue / g.units;
      return g;
    }).sort((a, b) => b.revenue - a.revenue);
  }, [data]);

  const formatCurrency = (val) => new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format(val);

  return (
    <div>
      <div className="chart-grid">
        <div className="chart-card">
          <h3 className="chart-title">Revenue by Model</h3>
          <div style={{ height: 400 }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={modelsData} layout="vertical" margin={{ left: 40 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" horizontal={false} />
                <XAxis type="number" stroke="#94a3b8" tickFormatter={(val) => `₹${(val/10000000).toFixed(0)}Cr`} />
                <YAxis dataKey="model" type="category" stroke="#94a3b8" />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#151a25', border: '1px solid #1e293b' }}
                  formatter={(value) => formatCurrency(value)}
                />
                <Bar dataKey="revenue" fill="#3b82f6" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      <div className="data-table-container">
        <table className="data-table">
          <thead>
            <tr>
              <th>Model</th>
              <th>Units Sold</th>
              <th>Total Revenue</th>
              <th>Avg Selling Price</th>
            </tr>
          </thead>
          <tbody>
            {modelsData.map(m => (
              <tr key={m.model}>
                <td><strong>{m.model}</strong></td>
                <td>{m.units}</td>
                <td>{formatCurrency(m.revenue)}</td>
                <td>{formatCurrency(m.avgPrice)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default ModelPerformance;

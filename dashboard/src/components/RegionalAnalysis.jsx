import React, { useMemo } from 'react';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer
} from 'recharts';

const RegionalAnalysis = ({ data }) => {
  const regionsData = useMemo(() => {
    const grouped = {};
    data.forEach(item => {
      const region = item.region || 'Unknown';
      if (!grouped[region]) grouped[region] = { region, revenue: 0, units: 0 };
      grouped[region].revenue += item.sale_price_inr || 0;
      grouped[region].units += 1;
    });
    
    return Object.values(grouped).sort((a, b) => b.revenue - a.revenue);
  }, [data]);

  const formatCurrency = (val) => new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format(val);

  return (
    <div>
      <div className="chart-grid">
        <div className="chart-card">
          <h3 className="chart-title">Revenue by Region</h3>
          <div style={{ height: 400 }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={regionsData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
                <XAxis dataKey="region" stroke="#94a3b8" />
                <YAxis stroke="#94a3b8" tickFormatter={(val) => `₹${(val/10000000).toFixed(0)}Cr`} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#151a25', border: '1px solid #1e293b' }}
                  formatter={(value) => formatCurrency(value)}
                />
                <Bar dataKey="revenue" fill="#10b981" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RegionalAnalysis;

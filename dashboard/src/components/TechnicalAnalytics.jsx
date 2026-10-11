import React, { useMemo } from 'react';
import { 
  PieChart, Pie, Cell, Tooltip, ResponsiveContainer, Legend
} from 'recharts';

const COLORS = ['#3b82f6', '#8b5cf6', '#10b981', '#f59e0b', '#ef4444'];

const TechnicalAnalytics = ({ data }) => {
  const { fuelData, transmissionData } = useMemo(() => {
    const fuel = {};
    const trans = {};

    data.forEach(item => {
      const f = item.fuel_type || 'Unknown';
      const t = item.transmission || 'Unknown';

      if (!fuel[f]) fuel[f] = { name: f, value: 0 };
      if (!trans[t]) trans[t] = { name: t, value: 0 };

      fuel[f].value += 1;
      trans[t].value += 1;
    });

    return {
      fuelData: Object.values(fuel),
      transmissionData: Object.values(trans)
    };
  }, [data]);

  return (
    <div>
      <div className="chart-grid">
        <div className="chart-card">
          <h3 className="chart-title">Sales by Fuel Type</h3>
          <div style={{ height: 350 }}>
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={fuelData}
                  cx="50%"
                  cy="50%"
                  innerRadius={80}
                  outerRadius={120}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {fuelData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip contentStyle={{ backgroundColor: '#151a25', border: '1px solid #1e293b' }} />
                <Legend verticalAlign="bottom" height={36} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="chart-card">
          <h3 className="chart-title">Sales by Transmission</h3>
          <div style={{ height: 350 }}>
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={transmissionData}
                  cx="50%"
                  cy="50%"
                  innerRadius={80}
                  outerRadius={120}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {transmissionData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[(index + 2) % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip contentStyle={{ backgroundColor: '#151a25', border: '1px solid #1e293b' }} />
                <Legend verticalAlign="bottom" height={36} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TechnicalAnalytics;

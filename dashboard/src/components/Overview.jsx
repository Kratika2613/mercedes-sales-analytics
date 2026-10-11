import React, { useMemo } from 'react';
import { 
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer,
  PieChart, Pie, Cell, Legend
} from 'recharts';
import { TrendingUp, TrendingDown, DollarSign, Car, Users } from 'lucide-react';

const COLORS = ['#66fcf1', '#45a29e', '#7b2cbf', '#f87171', '#fbbf24', '#4ade80'];

const Overview = ({ data }) => {
  const { kpis, monthlyTrends, bodyStyleData, recentSales } = useMemo(() => {
    let totalRevenue = 0;
    let maxRevenue = 0;
    const monthlyData = {};
    const bodyStyle = {};
    
    data.forEach(item => {
      const price = item.sale_price_inr || 0;
      totalRevenue += price;
      
      const month = item.sale_date.substring(0, 7);
      if (!monthlyData[month]) monthlyData[month] = { month, revenue: 0, units: 0 };
      monthlyData[month].revenue += price;
      monthlyData[month].units += 1;
      
      const vClass = item.vehicle_class || 'Unknown';
      if (!bodyStyle[vClass]) bodyStyle[vClass] = { name: vClass, value: 0 };
      bodyStyle[vClass].value += 1;
    });

    const monthlyArray = Object.values(monthlyData).sort((a, b) => a.month.localeCompare(b.month));
    
    const recent = [...data]
      .filter(d => d.sale_price_inr > 0)
      .sort((a, b) => new Date(b.sale_date) - new Date(a.sale_date))
      .slice(0, 5);

    return { 
      kpis: {
        totalRecords: data.length,
        totalRevenue,
        avgPrice: totalRevenue / (data.length || 1),
        dealers: new Set(data.map(d => d.dealer_id)).size
      },
      monthlyTrends: monthlyArray,
      bodyStyleData: Object.values(bodyStyle).sort((a,b) => b.value - a.value),
      recentSales: recent
    };
  }, [data]);

  const formatCurrency = (val) => new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format(val);
  const formatShortCurrency = (val) => `₹${(val/10000000).toFixed(1)}Cr`;

  return (
    <div>
      {/* Top KPIs */}
      <div className="kpi-grid">
        <div className="kpi-card">
          <div className="kpi-header">
            <span>Total Sales</span>
            <DollarSign size={18} color="var(--accent-primary)" />
          </div>
          <div className="kpi-value text-primary">{formatShortCurrency(kpis.totalRevenue)}</div>
          <div className="kpi-trend text-success">
            <TrendingUp size={14} /> <span>+12.5% vs last year</span>
          </div>
        </div>

        <div className="kpi-card">
          <div className="kpi-header">
            <span>Avg Price</span>
            <DollarSign size={18} color="var(--accent-secondary)" />
          </div>
          <div className="kpi-value">{formatCurrency(kpis.avgPrice)}</div>
          <div className="kpi-trend text-danger">
            <TrendingDown size={14} /> <span>-2.1% vs last year</span>
          </div>
        </div>

        <div className="kpi-card">
          <div className="kpi-header">
            <span>Cars Sold</span>
            <Car size={18} color="var(--accent-success)" />
          </div>
          <div className="kpi-value">{kpis.totalRecords.toLocaleString()}</div>
          <div className="kpi-trend text-success">
            <TrendingUp size={14} /> <span>+5.4% vs last year</span>
          </div>
        </div>

        <div className="kpi-card">
          <div className="kpi-header">
            <span>Active Dealers</span>
            <Users size={18} color="var(--accent-warning)" />
          </div>
          <div className="kpi-value">{kpis.dealers}</div>
          <div className="kpi-trend text-success">
            <TrendingUp size={14} /> <span>Stable</span>
          </div>
        </div>
      </div>

      {/* Charts Row 1 */}
      <div className="chart-grid">
        <div className="chart-card">
          <h3 className="chart-title">Sales Weekly/Monthly Trends</h3>
          <div style={{ height: 320 }}>
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={monthlyTrends}>
                <defs>
                  <linearGradient id="colorRev" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="var(--accent-primary)" stopOpacity={0.4}/>
                    <stop offset="95%" stopColor="var(--accent-primary)" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--border-color)" vertical={false} />
                <XAxis dataKey="month" stroke="var(--text-muted)" tick={{fontSize: 12}} dy={10} />
                <YAxis stroke="var(--text-muted)" tickFormatter={(val) => `₹${(val/10000000).toFixed(0)}Cr`} tick={{fontSize: 12}} />
                <RechartsTooltip 
                  contentStyle={{ backgroundColor: 'var(--bg-card)', border: '1px solid var(--border-color)', borderRadius: '8px' }}
                  formatter={(value) => formatCurrency(value)}
                  labelStyle={{ color: 'var(--text-muted)' }}
                />
                <Area type="monotone" dataKey="revenue" stroke="var(--accent-primary)" strokeWidth={3} fillOpacity={1} fill="url(#colorRev)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="chart-card">
          <h3 className="chart-title">Sales by Body Style</h3>
          <div style={{ height: 320 }}>
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={bodyStyleData}
                  cx="50%"
                  cy="45%"
                  innerRadius={70}
                  outerRadius={100}
                  paddingAngle={2}
                  dataKey="value"
                  stroke="none"
                >
                  {bodyStyleData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <RechartsTooltip contentStyle={{ backgroundColor: 'var(--bg-card)', border: '1px solid var(--border-color)', borderRadius: '8px' }} />
                <Legend verticalAlign="bottom" height={36} iconType="circle" wrapperStyle={{ fontSize: '12px', color: 'var(--text-muted)' }} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Recent Sales Table */}
      <div className="data-table-container">
        <div className="data-table-header">
          <h3 className="chart-title" style={{ marginBottom: 0 }}>Recent Selling Cars</h3>
        </div>
        <table className="data-table">
          <thead>
            <tr>
              <th>Car Model</th>
              <th>Class</th>
              <th>Date</th>
              <th>Location</th>
              <th>Price</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {recentSales.map((sale, i) => (
              <tr key={sale.sale_id || i}>
                <td>
                  <div style={{ fontWeight: 600, color: 'var(--text-bright)' }}>{sale.model}</div>
                  <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>{sale.manufacturing_year} • {sale.color}</div>
                </td>
                <td>{sale.vehicle_class}</td>
                <td>{sale.sale_date}</td>
                <td>{sale.city}, {sale.state}</td>
                <td style={{ fontWeight: 600 }}>{formatCurrency(sale.sale_price_inr)}</td>
                <td>
                  <span className="pill success">Delivered</span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Overview;

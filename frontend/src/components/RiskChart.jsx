import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell, ReferenceLine } from 'recharts'
import './RiskChart.css'

/**
 * Risk comparison chart showing the user's risk vs population average.
 */
function RiskChart({ probability, disease, populationAverage = 0.15 }) {
    const userRisk = Math.round(probability * 100)
    const avgRisk = Math.round(populationAverage * 100)

    const data = [
        { name: 'Your Risk', value: userRisk, fill: userRisk > avgRisk ? '#ef4444' : '#10b981' },
        { name: 'Population Avg', value: avgRisk, fill: '#6b7280' },
    ]

    return (
        <div className="risk-chart-container">
            <h4>Risk Comparison</h4>
            <ResponsiveContainer width="100%" height={150}>
                <BarChart data={data} layout="vertical" margin={{ top: 10, right: 30, left: 80, bottom: 10 }}>
                    <XAxis type="number" domain={[0, 100]} tickFormatter={(v) => `${v}%`} />
                    <YAxis type="category" dataKey="name" width={80} />
                    <Tooltip formatter={(value) => `${value}%`} />
                    <Bar dataKey="value" radius={[0, 4, 4, 0]} barSize={24}>
                        {data.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={entry.fill} />
                        ))}
                    </Bar>
                    <ReferenceLine x={50} stroke="#d1d5db" strokeDasharray="3 3" />
                </BarChart>
            </ResponsiveContainer>
            <p className="risk-chart-caption">
                {userRisk > avgRisk
                    ? `Your assessed risk is ${userRisk - avgRisk}% higher than average.`
                    : `Your assessed risk is ${avgRisk - userRisk}% lower than average.`
                }
            </p>
        </div>
    )
}

export default RiskChart

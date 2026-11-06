import type { CaseReport } from '@/entities/report/model/types';
import {
  CartesianGrid,
  LabelList,
  ReferenceLine,
  ResponsiveContainer,
  Scatter,
  ScatterChart,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';

export function CompMap({ data }: { data: CaseReport['competitors'] }) {
  const otherCompetitors = data.items.filter((item) => !item.isProduct);
  const ourProduct = data.items.filter((item) => item.isProduct);

  return (
    <div style={{ width: '100%', height: 360 }}>
      <ResponsiveContainer width="100%" height="100%">
        <ScatterChart margin={{ top: 20, right: 100, bottom: 36, left: 20 }}>
          <CartesianGrid />

          <XAxis
            type="number"
            dataKey="x"
            domain={[0, 10]}
            name={data.axes.x}
            label={{ value: data.axes.x, position: 'bottom', offset: 12 }}
          />

          <YAxis
            type="number"
            dataKey="y"
            domain={[0, 10]}
            name={data.axes.y}
            label={{ value: data.axes.y, angle: -90, position: 'insideLeft' }}
          />

          <ReferenceLine x={5} stroke="#999" strokeDasharray="4 4" />
          <ReferenceLine y={5} stroke="#999" strokeDasharray="4 4" />

          <Tooltip
            contentStyle={{
              color: '#000',
              backgroundColor: '#fff',
              border: '1px solid #ccc',
            }}
            itemStyle={{ color: '#000' }}
            labelStyle={{ color: '#000' }}
          />

          <Scatter data={otherCompetitors} fill="#bfbfbf" shape={<circle r={7} />}>
            <LabelList dataKey="name" position="right" />
          </Scatter>

          <Scatter data={ourProduct} fill="#000" shape={<circle r={7} />}>
            <LabelList dataKey="name" position="right" />
          </Scatter>
        </ScatterChart>
      </ResponsiveContainer>
    </div>
  );
}

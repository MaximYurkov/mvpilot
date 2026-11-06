import ReactECharts from 'echarts-for-react';
import type { CaseReport } from '@/entities/report/model/types';

export function MetricsTree({ data }: { data: CaseReport['metrics']['tree'] }) {
  const option = {
    tooltip: {
      trigger: 'item',
      triggerOn: 'mousemove',
    },
    series: [
      {
        type: 'tree',
        data: [data],
        top: '8%',
        left: '20%',
        bottom: '8%',
        right: '20%',
        orient: 'LR',
        symbol: 'circle',
        symbolSize: 8,
        edgeShape: 'curve',
        expandAndCollapse: false,
        initialTreeDepth: -1,
        lineStyle: {
          color: '#d9d9d9',
          width: 2,
        },
        label: {
          position: 'left',
          verticalAlign: 'middle',
          align: 'right',
          color: '#000',
          fontSize: 12,
        },
        leaves: {
          label: {
            position: 'right',
            verticalAlign: 'middle',
            align: 'left',
            color: '#000',
            fontSize: 12,
          },
        },
        emphasis: {
          focus: 'descendant',
        },
        animationDuration: 350,
        animationDurationUpdate: 500,
      },
    ],
  };

  return (
    <div style={{ width: '100%', height: 360 }}>
      <ReactECharts option={option} style={{ width: '100%', height: '100%' }} notMerge />
    </div>
  );
}

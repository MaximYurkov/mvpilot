import { Popover, Tag } from 'antd';

import type { CaseReport } from '@/entities/report/model/types';

export function Cell({
  risks,
  cellNumber,
}: {
  risks: CaseReport['risks']['items'];
  cellNumber: number;
}) {
  return (
    <>
      {risks
        .filter((risk) => risk.cell === cellNumber)
        .map((risk, index) => (
          <Popover
            key={risk.description}
            content={
              <>
                <p>{risk.description}</p>
                <p>Как снизить: {risk.mitigation}</p>
                <p>Как проверить: {risk.cheapCheck}</p>
              </>
            }
          >
            <Tag>{index + 1}</Tag>
          </Popover>
        ))}
    </>
  );
}

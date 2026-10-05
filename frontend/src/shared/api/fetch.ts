import type { Case, CaseReport } from './types';

export async function fetchCasesCard(): Promise<Case[]> {
  const response = await fetch('/cases.json');

  if (!response.ok) {
    throw new Error(`Сервер ответил ${response.status}`);
  }

  return response.json();
}

export async function getCaseReport(caseId: string): Promise<CaseReport | null> {
  const response = await fetch('/reports.json');

  if (!response.ok) {
    throw new Error(`Сервер ответил ${response.status}`);
  }

  const data = await response.json();

  return data[caseId] ?? null;
}

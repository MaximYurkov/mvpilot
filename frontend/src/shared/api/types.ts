export type CaseReport = {
  overview: {
    summary: string;
    problem: string;
    audience: string;
    value: string;
  };
  market: {
    segments: { name: string; description: string; needs: string[] }[];
    competitors: string[];
  };
  jtbd: { situation: string; motivation: string; outcome: string }[];
  leanCanvas: {
    problems: string[];
    segments: string[];
    value: string;
    solutions: string[];
    channels: string[];
    revenue: string[];
    costs: string[];
    metrics: string[];
    advantage: string;
  };
  mvp: { name: string; description: string; priority: Priority }[];
  backlog: { epic: string; story: string; criteria: string[]; priority: Priority }[];
  roadmap: { name: string; goal: string; results: string[] }[];
  metricsAndRisks: {
    metrics: string[];
    risks: { description: string; level: RiskLevel; mitigation: string }[];
  };
  critic: {
    issues: string[];
    recommendations: string[];
  };
  markdown: string;
};

type Priority = 'must' | 'should' | 'could';
type RiskLevel = 'high' | 'medium' | 'low';

export type Case = {
  id: number;
  title: string;
  description: string;
  audience: string;
  createdAt: string;
  updatedAt: string;
};

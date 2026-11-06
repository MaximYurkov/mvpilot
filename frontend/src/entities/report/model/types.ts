export type Score = 1 | 2 | 3;
export type Priority = 'must' | 'should' | 'could' | 'wont';
export type JtbdPriority = 'high' | 'medium' | 'low';
export type SectionStatus = 'ready' | 'partial' | 'insufficient_data' | 'not_applicable';

export type Source = {
  id: string;
  title: string;
  url: string | null;
  publisher: string | null;
  publishedAt: string | null;
};

export type SectionMeta = {
  status: SectionStatus;
  note: string | null;
  sources: Source[];
};

export type MetricNode = {
  name: string;
  children?: MetricNode[];
};

export type MarketSize = {
  value: number;
  unit: string;
  label: string;
};

export type Competitor = {
  name: string;
  x: number | null;
  y: number | null;
  isProduct: boolean;
  url: string | null;
  strengths: string[];
  weaknesses: string[];
};

export type FeatureComparison = {
  feature: string;
  product: boolean;
  competitor1: boolean;
  competitor2: boolean;
  competitor3: boolean;
};

export type Risk = {
  cell: 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9;
  description: string;
  mitigation: string;
  cheapCheck: string;
};

export type FinanceFigure = {
  key: string;
  label: string;
  value: number | null;
  unit: string;
  note: string | null;
};

export type BudgetSection = {
  name: string;
  recommended: number;
  minimum: number;
};

export type CaseReport = {
  overview: SectionMeta & {
    idea: string;
    readiness: {
      axis: string;
      score: number;
      comment: string;
    }[];
    tiles: {
      label: string;
      value: number;
      unit: string;
    }[];
  };

  market: SectionMeta & {
    tam: MarketSize | null;
    sam: MarketSize | null;
    som: MarketSize | null;
    method: 'bottom-up' | 'top-down' | null;
    methodComment: string | null;
    assumptions: string[];
    dynamics: {
      year: number;
      value: number;
    }[];
    dynamicsSource: string | null;
    trends: {
      name: string;
      direction: 'up' | 'flat' | 'down';
      comment: string;
    }[];
  };

  audience: SectionMeta & {
    primarySegment: string | null;
    segments: {
      name: string;
      estimatedShare: number | null;
      description: string;
      needs: string[];
    }[];
    jtbd: {
      situation: string;
      motivation: string;
      outcome: string;
      priority: JtbdPriority;
    }[];
  };

  competitors: SectionMeta & {
    axes: {
      x: string;
      y: string;
    };
    items: Competitor[];
    comparison: FeatureComparison[];
    swot: {
      strengths: string[];
      weaknesses: string[];
      opportunities: string[];
      threats: string[];
    };
  };

  leanCanvas: SectionMeta & {
    problems: string[];
    solutions: string[];
    value: string;
    advantage: string;
    segments: string[];
    metrics: string[];
    channels: string[];
    costs: string[];
    revenue: string[];
  };

  mvp: SectionMeta & {
    features: {
      name: string;
      description: string;
      priority: Priority;
    }[];
    userFlow: {
      step: string;
      description: string;
    }[];
  };

  roadmap: SectionMeta & {
    stages: {
      name: string;
      goal: string;
      startMonth: number;
      duration: number;
      results: string[];
    }[];
  };

  metrics: SectionMeta & {
    northStar: {
      name: string;
      value: number | null;
      unit: string;
    };
    tree: MetricNode | null;
    funnel: {
      stage: string;
      value: number;
      target: number | null;
    }[];
  };

  finance: SectionMeta & {
    figures: FinanceFigure[];
    recommendedTotal: number | null;
    budgetSections: BudgetSection[];
    note: string | null;
  };

  risks: SectionMeta & {
    items: Risk[];
  };

  nextSteps: SectionMeta & {
    items: {
      title: string;
      description: string;
      priority: Priority;
      effort: 'low' | 'medium' | 'high';
      partner: {
        name: string;
        note: string;
        url: string | null;
      } | null;
    }[];
  };

  markdown: string | null;
};

export type Case = {
  id: number;
  title: string;
  description: string;
  audience: string;
  createdAt: string;
  updatedAt: string;
};

export type CaseFormValues = Omit<Case, 'id' | 'createdAt' | 'updatedAt'>;

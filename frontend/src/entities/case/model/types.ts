export type Case = {
  id: number;
  title: string;
  description: string;
  audience: string;
  createdAt: string;
  updatedAt: string;
};

export type CaseFormValues = Omit<Case, 'id' | 'createdAt' | 'updatedAt'>;

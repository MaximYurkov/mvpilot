import { Navigate, Route, Routes } from 'react-router-dom';

import { AppLayout } from '../layouts/AppLayout';
import { CasesPage } from '../../pages/cases/ui/CasesPage';
import { CreateCasePage } from '../../pages/create-case/ui/CreateCasePage';
import { CaseDetailsPage } from '../../pages/case-details/ui/CaseDetailsPage';
import { NotFoundPage } from '../../pages/not-found/ui/NotFoundPage';

export function AppRouter() {
  return (
    <Routes>
      <Route element={<AppLayout />}>
        <Route path="/" element={<Navigate to="/cases" replace />} />
        <Route path="/cases" element={<CasesPage />} />
        <Route path="/cases/new" element={<CreateCasePage />} />
        <Route path="/cases/:caseId" element={<CaseDetailsPage />} />
        <Route path="*" element={<NotFoundPage />} />
      </Route>
    </Routes>
  );
}

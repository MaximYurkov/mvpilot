import { existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import ts from 'typescript';

const backendDir = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const frontendDir = path.resolve(backendDir, process.argv[2] ?? '../frontend');
const reportTypes = path.join(frontendDir, 'src/entities/report/model/types.ts');
const caseTypes = path.join(frontendDir, 'src/entities/case/model/types.ts');
const generatedTypes = path.join(backendDir, 'generated/types.gen.ts');

for (const file of [reportTypes, caseTypes, generatedTypes]) {
  if (!existsSync(file)) {
    console.error(`File not found: ${file}`);
    console.error('Generate types first; pass the reference frontend directory as an argument.');
    process.exit(1);
  }
}

const sharedNames = [
  'CaseReport', 'Source', 'MetricNode', 'MarketSize', 'Competitor',
  'FeatureComparison', 'Risk', 'FinanceFigure', 'BudgetSection',
  'Priority', 'JtbdPriority', 'SectionStatus',
];
const importPath = (file) => JSON.stringify(file.replaceAll('\\', '/'));
const checkSource = [
  `import type * as Backend from ${importPath(generatedTypes)};`,
  `import type * as Reports from ${importPath(reportTypes)};`,
  `import type * as Cases from ${importPath(caseTypes)};`,
  'type Expect<T extends true> = T;',
  'type Compatible<A, B> = [A] extends [B] ? [B] extends [A] ? true : false : false;',
  ...sharedNames.map((name) =>
    `type Check${name} = Expect<Compatible<Backend.${name}, Reports.${name}>>;`,
  ),
  'type CheckCase = Expect<Compatible<Backend.Case, Cases.Case>>;',
  'type CheckForm = Expect<Compatible<Backend.CaseFormValues, Cases.CaseFormValues>>;',
  "type BackendMeta = Pick<Backend.CaseReport['overview'], 'status' | 'note' | 'sources'>;",
  'type CheckMeta = Expect<Compatible<BackendMeta, Reports.SectionMeta>>;',
].join('\n');

// Supply the comparison file in memory: nothing is written to the frontend.
const virtualFile = path.join(backendDir, 'contract-check.virtual.ts');
const options = {
  strict: true,
  noEmit: true,
  skipLibCheck: true,
  types: [],
  target: ts.ScriptTarget.ES2023,
  module: ts.ModuleKind.ESNext,
  moduleResolution: ts.ModuleResolutionKind.Bundler,
  allowImportingTsExtensions: true,
};
const host = ts.createCompilerHost(options);
const getSourceFile = host.getSourceFile.bind(host);
const fileExists = host.fileExists.bind(host);
host.fileExists = (file) => path.resolve(file) === virtualFile || fileExists(file);
host.getSourceFile = (file, languageVersion, onError, shouldCreateNewSourceFile) =>
  path.resolve(file) === virtualFile
    ? ts.createSourceFile(file, checkSource, languageVersion, true)
    : getSourceFile(file, languageVersion, onError, shouldCreateNewSourceFile);

const program = ts.createProgram([virtualFile], options, host);
const diagnostics = ts.getPreEmitDiagnostics(program);
if (diagnostics.length > 0) {
  console.error(ts.formatDiagnosticsWithColorAndContext(diagnostics, {
    getCurrentDirectory: () => backendDir,
    getCanonicalFileName: (file) => file,
    getNewLine: () => '\n',
  }));
  process.exit(1);
}
console.log('Generated API types match the reference frontend types in both directions.');

import React from 'react';
import { AlertCircle, Hash, FileWarning, Terminal, AlertTriangle } from 'lucide-react';
import { HLX_SPEC_JSON } from '../data';

const ErrorTaxonomy: React.FC = () => {
  const taxonomy = HLX_SPEC_JSON?.components?.A_formal_canonical_specification?.error_taxonomy || { lexical_errors: [], syntactic_errors: [], constraint_errors: [], semantic_errors: [] };
  const ranges = HLX_SPEC_JSON?.components?.A_formal_canonical_specification?.canonical_format_rules?.error_model_ranges || { "1000-1099": "N/A", "1100-1199": "N/A", "1300-1399": "N/A", "1400-1499": "N/A" };

  const renderCategory = (title: string, range: string, icon: React.ReactNode, errors: any[]) => (
    <div className="mb-8">
      <h3 className="text-lg font-bold text-white mb-2 flex items-center gap-2">
        {icon}
        {title}
      </h3>
      <div className="text-xs font-mono text-hlx-muted mb-4 ml-7">Range: {range}</div>
      <div className="bg-hlx-surface border border-hlx-border rounded-xl overflow-hidden">
        <table className="w-full text-sm text-left">
          <thead className="bg-hlx-bg text-hlx-muted font-mono text-xs uppercase">
            <tr>
              <th className="p-4 w-24">Code</th>
              <th className="p-4 w-64">Identifier</th>
              <th className="p-4">Description</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-hlx-border/50">
            {errors.map((err) => (
              <tr key={err.code} className="hover:bg-hlx-bg/50">
                <td className="p-4 font-mono text-red-400 font-bold">{err.code}</td>
                <td className="p-4 font-mono text-white">{err.name}</td>
                <td className="p-4 text-hlx-muted">{err.desc}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );

  return (
    <div className="space-y-6 h-[calc(100vh-4rem)] flex flex-col">
      <header>
        <h2 className="text-2xl font-bold text-white flex items-center gap-3">
          <AlertCircle className="text-red-500" />
          Error Taxonomy (v1.0)
        </h2>
        <p className="text-hlx-muted text-sm mt-1">
          Complete error specification. Every invalid byte sequence produces one of these codes.
        </p>
      </header>

      <div className="flex-1 overflow-auto pr-2 pb-12">
        {renderCategory("Lexical Errors", ranges["1000-1099"], <Terminal size={18} className="text-hlx-accent" />, taxonomy.lexical_errors)}
        {renderCategory("Syntactic Errors", ranges["1100-1199"], <Hash size={18} className="text-purple-400" />, taxonomy.syntactic_errors)}
        {renderCategory("Constraint Errors", ranges["1300-1399"], <AlertTriangle size={18} className="text-yellow-400" />, taxonomy.constraint_errors)}
        {renderCategory("Semantic Errors", ranges["1400-1499"], <FileWarning size={18} className="text-orange-400" />, taxonomy.semantic_errors)}
      </div>
    </div>
  );
};

export default ErrorTaxonomy;
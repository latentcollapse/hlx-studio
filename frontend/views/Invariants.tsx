
import React from 'react';
import { ShieldCheck, Scale, Lock, RefreshCcw, Network, AlertTriangle, FileCheck } from 'lucide-react';
import { HLX_SPEC_JSON } from '../data';

const Invariants: React.FC = () => {
  const formalSpec = HLX_SPEC_JSON?.components?.A_formal_canonical_specification || {} as any;
  const limits = formalSpec.resource_limits || {};
  const principles = formalSpec.canonical_principles || {};
  const rules = formalSpec.canonical_format_rules || { whitespace: {}, integers: {}, floats: {}, bytes: {}, arrays: {}, objects: {} };
  const invariantList = formalSpec.invariants?.invariants || [];

  return (
    <div className="space-y-8 animate-fade-in pb-12">
      <header>
        <h2 className="text-2xl font-bold text-white flex items-center gap-3">
          <ShieldCheck className="text-green-400" />
          Canonical Principles & Invariants
        </h2>
        <p className="text-hlx-muted text-sm mt-1">
          {formalSpec.description}
        </p>
      </header>

      {/* Abstract Principles */}
      <section>
        <h3 className="text-xl font-bold text-white flex items-center gap-2 mb-4">
          <Network className="text-hlx-accent" size={20} />
          Canonical Principles
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {Object.entries(principles).map(([key, rule]: [string, any]) => (
            <div key={key} className="bg-hlx-surface border border-hlx-border p-4 rounded-lg">
              <div className="text-sm font-bold text-hlx-accent uppercase mb-2 tracking-wider">{key.replace(/_/g, ' ')}</div>
              <p className="text-sm text-hlx-text leading-relaxed">{rule}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Formal Invariants (Must Pass) */}
      <section>
        <h3 className="text-xl font-bold text-white flex items-center gap-2 mb-4">
          <FileCheck className="text-blue-400" size={20} />
          Formal Invariants (Must Pass)
        </h3>
        <div className="grid grid-cols-1 gap-4">
          {invariantList.map((inv: any) => (
            <div key={inv.id} className="bg-[#09090b] border border-hlx-border rounded-xl p-6 relative overflow-hidden group hover:border-blue-500/30 transition-colors">
               <div className="absolute top-0 right-0 p-3 opacity-10 group-hover:opacity-20 transition-opacity">
                 <ShieldCheck size={64} />
               </div>
               <div className="flex items-start gap-4 relative z-10">
                 <div className="mt-1">
                    <span className="font-mono text-xs font-bold text-blue-400 border border-blue-500/30 bg-blue-500/10 px-2 py-1 rounded">
                      {inv.id}
                    </span>
                 </div>
                 <div>
                   <h3 className="text-lg font-bold text-white mb-1">{inv.name}</h3>
                   <div className="font-mono text-sm text-hlx-accent mb-2 bg-hlx-bg/50 p-2 rounded border border-hlx-border inline-block">
                     {inv.rule}
                   </div>
                   <p className="text-sm text-hlx-muted">{inv.description}</p>
                 </div>
               </div>
            </div>
          ))}
        </div>
      </section>

      {/* Resource Limits */}
      <section>
        <h3 className="text-xl font-bold text-white flex items-center gap-2 mb-4">
          <AlertTriangle className="text-yellow-400" size={20} />
          Resource Limits (Hard Constraint)
        </h3>
        <div className="bg-hlx-surface border border-hlx-border rounded-xl overflow-hidden">
          <table className="w-full text-sm text-left">
            <thead className="bg-hlx-bg text-hlx-muted font-mono text-xs uppercase">
              <tr>
                <th className="p-4">Limit Name</th>
                <th className="p-4">Maximum Value</th>
                <th className="p-4">Violation Error</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-hlx-border/50">
              {Object.entries(limits).map(([key, limit]: [string, any]) => (
                <tr key={key} className="hover:bg-hlx-bg/50">
                  <td className="p-4 font-mono text-white">{key}</td>
                  <td className="p-4 font-mono text-hlx-accent">{limit.value}</td>
                  <td className="p-4 font-mono text-red-400 text-xs">{limit.error}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      {/* Canonical Format Summary */}
      <section>
        <h3 className="text-xl font-bold text-white flex items-center gap-2 mb-4">
          <Scale className="text-purple-400" size={20} />
          Canonical Format Rules (Subset)
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
             <RuleCard title="Whitespace" rule={rules.whitespace.rule} />
             <RuleCard title="Integers" rule={rules.integers.rule} />
             <RuleCard title="Floats" rule={rules.floats.rule} />
             <RuleCard title="Bytes" rule={rules.bytes.rule} />
             <RuleCard title="Arrays" rule={rules.arrays.rule} />
             <RuleCard title="Objects" rule={rules.objects.rule} />
        </div>
      </section>
    </div>
  );
};

const RuleCard = ({ title, rule }: { title: string, rule: string }) => (
  <div className="bg-hlx-surface border border-hlx-border p-4 rounded-lg">
    <div className="flex justify-between items-start mb-2">
        <span className="font-bold text-white">{title}</span>
    </div>
    <p className="text-sm text-hlx-muted mb-2">{rule}</p>
  </div>
);

export default Invariants;

import React from 'react';
import { Box } from 'lucide-react';
import { HLX_SPEC_JSON } from '../data';

const BinaryExplainer: React.FC = () => {
  const binarySpec = HLX_SPEC_JSON.components.A_formal_canonical_specification.binary_lite_spec;
  const opcodes = Object.entries(binarySpec.opcodes).map(([byte, info]: [string, any]) => ({
    byte,
    name: info.name,
    payload: info.payload
  }));

  return (
    <div className="space-y-6">
      <header>
        <h2 className="text-2xl font-bold text-white flex items-center gap-3">
          <Box className="text-purple-400" />
          HLX-B-Lite Binary
        </h2>
        <p className="text-hlx-muted text-sm mt-1">
          Binary encoding rules for the v1.0 Canonical Specification.
        </p>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Hex Dump Simulation */}
        <div className="bg-[#09090b] border border-hlx-border rounded-xl p-6 font-mono text-sm">
          <div className="text-xs text-hlx-muted mb-4 border-b border-hlx-border pb-2">SAMPLE: HLXDocument (Root Null)</div>
          <div className="grid grid-cols-[auto_1fr] gap-6">
            <div className="text-hlx-muted select-none opacity-50 text-right">
              0000<br/>0010
            </div>
            <div className="space-y-1">
              {/* {4:{@0:null,@1:{5:{@0:"hlx-lite-1.0"}}}} */}
              <div className="flex gap-2 flex-wrap">
                <span className="text-hlx-secondary font-bold hover:bg-white/10 cursor-help" title="OBJECT (0x07)">07</span>
                <span className="text-orange-300 hover:bg-white/10 cursor-help" title="Contract ID: 4">04</span>
                <span className="text-gray-500" title="Field Count: 2">02</span>
                
                <span className="text-pink-400 hover:bg-white/10 cursor-help" title="Field Index: 0">00</span>
                <span className="text-red-400 hover:bg-white/10 cursor-help" title="NULL (0x00)">00</span>

                <span className="text-pink-400 hover:bg-white/10 cursor-help" title="Field Index: 1">01</span>
                <span className="text-hlx-secondary font-bold hover:bg-white/10 cursor-help" title="OBJECT (0x07)">07</span>
                <span className="text-orange-300 hover:bg-white/10 cursor-help" title="Contract ID: 5">05</span>
                <span className="text-gray-500" title="Field Count: 1">01</span>
                
                <span className="text-pink-400 hover:bg-white/10 cursor-help" title="Field Index: 0">00</span>
                <span className="text-green-400 hover:bg-white/10 cursor-help" title="TEXT (0x04)">04</span>
                <span className="text-gray-500" title="Length: 12">0C</span>
                <span className="text-gray-300 text-xs tracking-tighter opacity-70">"hlx-lite-1.0"</span>
              </div>
            </div>
          </div>
          <div className="mt-6 text-xs text-hlx-muted">
             <p className="mb-2 font-bold">Encoding Rules:</p>
             <ul className="list-disc pl-4 space-y-1">
               {binarySpec.canonical_binary_rules.map((rule, i) => (
                 <li key={i}>{rule}</li>
               ))}
             </ul>
          </div>
        </div>

        {/* Opcode Table */}
        <div className="space-y-4">
           <h3 className="font-bold text-white">Opcode Reference</h3>
           <div className="overflow-hidden rounded-lg border border-hlx-border bg-hlx-surface">
             <table className="w-full text-sm text-left">
               <thead className="bg-hlx-bg text-hlx-muted font-mono text-xs">
                 <tr>
                   <th className="p-3">Byte</th>
                   <th className="p-3">Name</th>
                   <th className="p-3">Payload Structure</th>
                 </tr>
               </thead>
               <tbody className="divide-y divide-hlx-border/50">
                 {opcodes.map(op => (
                   <tr key={op.byte} className="hover:bg-hlx-bg/50">
                     <td className="p-3 font-mono text-hlx-accent">{op.byte}</td>
                     <td className="p-3 font-bold text-white">{op.name}</td>
                     <td className="p-3 text-hlx-muted font-mono text-xs">{op.payload}</td>
                   </tr>
                 ))}
               </tbody>
             </table>
           </div>
        </div>
      </div>
    </div>
  );
};

export default BinaryExplainer;
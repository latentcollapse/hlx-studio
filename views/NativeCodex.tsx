import React, { useMemo } from 'react';
import { Cpu, FileCode } from 'lucide-react';
import { HLX_SPEC_JSON } from '../data';
import { generateNativeCodex } from '../utils/serializer';
import HLXVisualizer from './HLXVisualizer';

const NativeCodex: React.FC = () => {
  // Memoize the heavy serialization operation
  const nativeSpec = useMemo(() => {
    return generateNativeCodex(HLX_SPEC_JSON);
  }, []);

  return (
    <div className="space-y-6 h-[calc(100vh-4rem)] flex flex-col">
      <header>
        <h2 className="text-2xl font-bold text-white flex items-center gap-3">
          <Cpu className="text-hlx-accent" />
          Native HLX Codex
        </h2>
        <p className="text-hlx-muted text-sm mt-1">
          The "Entirely HLX Based Version". This is the full JSON specification, bootstrapped into self-describing HLX-Lite contracts (ID 1, 2, 3).
        </p>
      </header>
      
      {/* We reuse the Visualizer but in 'ReadOnly' / 'Preset' mode implicitly by passing initial state */}
      <div className="flex-1 border border-hlx-border rounded-xl overflow-hidden bg-[#09090b]">
        <HLXVisualizer initialInput={nativeSpec} readOnly={false} />
      </div>
    </div>
  );
};

export default NativeCodex;
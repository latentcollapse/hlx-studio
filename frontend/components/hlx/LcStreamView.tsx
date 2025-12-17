import React from 'react';

interface LcStreamViewProps {
  stream: string;
}

const GLYPH_COLORS: Record<string, string> = {
  '🜊': '#39F5E5', // Cyan
  '🜁': '#A44DFB', // Violet
  '🜇': '#C77DFF', // Light Violet
  '🜂': '#FF3AF0', // Magenta
  '🜋': '#9B5CFF', // Purple
  '🜃': '#39F5E5', // Cyan (Array)
  '🜄': '#39F5E5', // Cyan (Array)
};

const LcStreamView: React.FC<LcStreamViewProps> = ({ stream }) => {
  if (!stream) return <div className="text-[#333] italic">No active stream</div>;

  const renderChar = (char: string, index: number) => {
    const color = GLYPH_COLORS[char];
    if (color) {
      return <span key={index} style={{ color, fontWeight: 'bold', fontSize: '1.2em' }}>{char}</span>;
    }
    return <span key={index} className="text-gray-300">{char}</span>;
  };

  return (
    <div className="font-mono text-sm break-all leading-relaxed bg-[#050208] p-4 rounded border border-[#333]">
      {stream.split('').map((c, i) => renderChar(c, i))}
    </div>
  );
};

export default LcStreamView;
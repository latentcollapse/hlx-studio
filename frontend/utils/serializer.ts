// HLX-Lite Canonical Serializer
// Transcodes arbitrary JSON into HLX-Lite Foundation Contracts (1, 2, 3)

export const HLX_KINDS = {
  NULL: 0,
  BOOL: 1,
  INT: 2,
  FLOAT: 3,
  TEXT: 4,
  BYTES: 5,
  ARRAY: 6,
  OBJECT: 7
};

const formatText = (str: string) => `"${str.replace(/"/g, '\\"')}"`; // Simplified escaping for internal use

// Wraps a raw value in HLXLiteValue (Contract 1)
const wrapValue = (kind: number, fieldIndex: number, valueStr: string): string => {
  return `{1:{@0:${kind},@${fieldIndex}:${valueStr}}}`;
};

export const toHLX = (data: any): string => {
  // Recursively convert to HLXLiteValue string
  
  if (data === null) {
    return `{1:{@0:${HLX_KINDS.NULL}}}`;
  }

  if (typeof data === 'boolean') {
    return wrapValue(HLX_KINDS.BOOL, 1, data ? 'true' : 'false');
  }

  if (typeof data === 'number') {
    if (Number.isInteger(data)) {
      return wrapValue(HLX_KINDS.INT, 2, data.toString());
    }
    return wrapValue(HLX_KINDS.FLOAT, 3, data.toString());
  }

  if (typeof data === 'string') {
    // Check for byte-string heuristic (starts with 0x) -> simple heuristic for this demo
    // The spec uses x"..." for bytes.
    if (data.startsWith('x"') && data.endsWith('"')) {
       return wrapValue(HLX_KINDS.BYTES, 5, data);
    }
    return wrapValue(HLX_KINDS.TEXT, 4, formatText(data));
  }

  if (Array.isArray(data)) {
    const items = data.map(item => toHLX(item)).join(',');
    const arrayStr = `[${items}]`;
    return wrapValue(HLX_KINDS.ARRAY, 6, arrayStr);
  }

  if (typeof data === 'object') {
    // Generic Object -> HLXLiteObject (Contract 3)
    // We map JSON keys to HLXLiteField (Contract 2)
    // Field 0: Index (auto-increment)
    // Field 1: Name (original JSON key)
    // Field 2: Value (Recursive HLXLiteValue)

    const keys = Object.keys(data).sort(); // Canonical Rule: Sorted Keys
    
    const fields = keys.map((key, idx) => {
      const val = toHLX(data[key]);
      // HLXLiteField: {2:{@0:idx, @1:key, @2:val}}
      return `{2:{@0:${idx},@1:${formatText(key)},@2:${val}}}`;
    });

    const fieldsArray = `[${fields.join(',')}]`;
    
    // HLXLiteObject: {3:{@0:0, @1:fields}} (ID 0 for Anonymous)
    const objStr = `{3:{@0:0,@1:${fieldsArray}}}`;
    
    return wrapValue(HLX_KINDS.OBJECT, 7, objStr);
  }

  return `{1:{@0:${HLX_KINDS.NULL}}}`; // Fallback
};

export const generateNativeCodex = (rootJson: any): string => {
  // Wrap the whole thing in HLXLiteDocument (Contract 4)
  // Field 0: Root (The generic object)
  // Field 1: Provenance (Contract 5)

  const rootValue = toHLX(rootJson);
  
  const provenance = `{5:{@0:"hlx-lite-1.0",@1:"${new Date().toISOString()}",@2:"HLX-NEXUS-ENGINE",@4:"Native Generation"}}`;

  return `{4:{@0:${rootValue},@1:${provenance}}}`;
};
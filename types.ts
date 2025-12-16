
export interface HLXField {
  index: number;
  name: string;
  type: string;
  description?: string;
  is_recursive?: boolean;
  cycle_rules?: string[];
}

export interface HLXContract {
  id: number;
  name: string;
  layer: string;
  fields: HLXField[] | Record<string, any>;
  description?: string;
  purpose?: string;
}

export interface HLXLayer {
  name: string;
  id_range: string;
  contracts: HLXContract[];
}

export interface HLXToken {
  name: string;
  symbol: string;
  hex: string;
  description: string;
}

export enum ViewMode {
  HELIX = 'HELIX',
  HLX_ENGINE = 'HLX_ENGINE',
  CRUCIBLE = 'CRUCIBLE',
  TTY1 = 'TTY1',
  ARCHIVE = 'ARCHIVE',
  JSON_SPEC = 'JSON_SPEC',
  NATIVE_CODEX = 'NATIVE_CODEX',
  HLX_NATIVE = 'HLX_NATIVE'
}

export interface HLXPacks {
  [key: string]: {
    [contractName: string]: {
      id: number;
      fields: Record<string, string | { name: string; type: string }>;
    };
  };
}

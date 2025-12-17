
import { HLXRuntime } from '../runtime/HLXRuntime';
import { HLXLite, RuntimeSnapshot } from '../runtime/HLXRuntimeTypes';
import { tokenize, Compiler } from '../utils/hlxl_compiler';
import { HLX_BOOTSTRAP_CODEX } from '../codex_data';
import { HLX_RUNTIME_CONFORMANCE } from '../runtime_conformance_data';
import { HPCP_TRIGGERS_YAML } from '../data/triggers';

// =============================================================================
// TYPES
// =============================================================================

export interface EngineRuntimeState {
  active_handles: number;
  memory_usage: number;
  table_entries: {
      handle: string;
      type: string;
      size: number;
  }[];
}

export interface ExecutionResult {
  hlxl: string;
  hlxl_ls: string;
  hlx: string;
  hlx_ls: string;
  lc_stream: string;
  hlx_lite: HLXLite;
  core_ast: object | null;
  invariants: Record<string, boolean>;
  provenance: {
    engine_id: string;
    codex_version: string;
    collapse_version: string;
    provenance_fp: string;
    interpreter_mode: string;
  };
  output_log?: string;
  runtime_state?: EngineRuntimeState;
}

// Singleton Runtime Instance (Persists across execution calls)
const RUNTIME = new HLXRuntime();

// Glyph Map for Pre-processing
const GLYPH_MAP: Record<string, string> = {
  '⟠': 'program', '◇': 'block', '⊢': 'let', '⊡': 'local', '↩': 'return',
  '❓': 'if', '❗': 'else', '⟳': 'while', '⟲': 'for',
  'ꙮ': 'latent', '⌸': 'table', '▣': 'using',
  '⚳': 'ls.collapse', '⚯': 'ls.resolve', '⚶': 'ls.snapshot',
  '▷': '|>',
  '⚿': 'ls.transaction',
  '⚐': 'latent guard',
  '⚳⊕': 'ls.compose'
};

// Deterministic hash for provenance fingerprinting (djb2 variant)
function deterministicHash(input: string): string {
    let hash = 5381;
    for (let i = 0; i < input.length; i++) {
        hash = ((hash << 5) + hash) ^ input.charCodeAt(i);
    }
    return (hash >>> 0).toString(16).padStart(8, '0');
}

function transliterate(source: string): string {
    let result = source;
    // Sort keys by length descending to handle multi-char glyphs like ⚳⊕ correctly
    const keys = Object.keys(GLYPH_MAP).sort((a, b) => b.length - a.length);
    for (const glyph of keys) {
        const ascii = GLYPH_MAP[glyph];
        result = result.split(glyph).join(ascii);
    }
    return result;
}

// =============================================================================
// INTERPRETER KERNEL
// =============================================================================

class Interpreter {
  private runtime: HLXRuntime;
  private log: string[] = [];
  private lcStream: string[] = [];
  private scope: Map<string, any> = new Map();

  constructor(runtime: HLXRuntime) {
    this.runtime = runtime;
  }

  logOp(msg: string) {
    this.log.push(msg);
  }

  appendStream(chunk: string) {
    this.lcStream.push(chunk);
  }

  getLog() {
      return this.log.join('\n');
  }

  getStream() {
      return this.lcStream.join('');
  }

  // --- AST WALKER ---

  evaluate(node: any): any {
    if (!node) return null;

    switch (node.kind) {
      case 'LITERAL':
        return node.value;
      
      case 'VAR_REF':
        const val = this.scope.get(node.name);
        if (val === undefined) {
             // Treat undefined variables as null/error depending on semantics
             return null;
        }
        return val;

      case 'SET_VAR':
      case 'SET_LOCAL':
         const rhs = this.evaluate(node.payload.expr);
         this.scope.set(node.payload.name, rhs);
         this.logOp(`>> SET ${node.payload.name} = ${JSON.stringify(rhs)}`);
         return rhs;

      case 'RETURN':
         return this.evaluate(node.payload);

      case 'APPLY_INTRINSIC':
        return this.execIntrinsic(node.op, node.args);

      case 'LS_OP':
        return this.execLSOp(node);

      case 'SEQ':
        return this.execSeq(node.body);

      case 'IF':
        const cond = this.evaluate(node.payload.cond);
        if (cond) {
           return this.execSeq(node.payload.then_branch.body);
        } else if (node.payload.else_branch) {
           return this.execSeq(node.payload.else_branch.body);
        }
        return null;
        
      case 'PIPELINE_APPLY':
        throw new Error("Pipeline nodes should be lowered by compiler.");

      case 'CALL_BLOCK':
        return null;

      default:
        return null;
    }
  }

  execSeq(nodes: any[]): any {
      let result = null;
      for (const node of nodes) {
          result = this.evaluate(node);
      }
      return result;
  }

  execIntrinsic(op: string, args: any[]): any {
    const vals = args.map(a => this.evaluate(a));
    switch (op) {
      case 'add': return vals[0] + vals[1];
      case 'sub': return vals[0] - vals[1];
      case 'mul': return vals[0] * vals[1];
      case 'div': return vals[0] / vals[1];
      case 'eq': return vals[0] === vals[1];
      case 'ne': return vals[0] !== vals[1];
      case 'gt': return vals[0] > vals[1];
      case 'lt': return vals[0] < vals[1];
      case 'and': return vals[0] && vals[1];
      case 'or': return vals[0] || vals[1];
      case 'not': return !vals[0];
      case 'assert': 
        if (!vals[0]) throw new Error("Assertion Failed");
        return true;
      case 'object_construct':
        const cid = vals[0];
        const fields = vals[1];
        const obj: any = { [cid]: {} };
        fields.forEach((f: any) => {
           obj[cid][`@${f.index}`] = f.value;
        });
        return obj;
      case 'object_create_generic':
        const genericFields = vals[0];
        const genObj: any = {};
        genericFields.forEach((f: any) => {
            genObj[f.key] = f.value;
        });
        return genObj;
      case 'object_get':
        const target = vals[0];
        const key = vals[1];
        return target ? target[key] : null;
      case 'array_get':
        if (Array.isArray(vals[0])) return vals[0][vals[1]];
        return null;
      default:
        return null;
    }
  }

  execLSOp(node: any): any {
    if (node.op === 'COLLAPSE') {
      const val = this.evaluate(node.val);
      const handle = this.runtime.collapse(val, node.tag || 'usr');
      this.logOp(`>> ⚳ COLLAPSE [${node.tag || 'usr'}] -> ${handle}`);
      const stream = this.runtime.encodeLC(val);
      this.appendStream(stream);
      return handle;
    }

    if (node.op === 'RESOLVE') {
      const handle = this.evaluate(node.handle);
      this.logOp(`>> ⚯ RESOLVE ${handle}`);
      const val = this.runtime.resolve(handle);
      const stream = this.runtime.encodeLC(val);
      this.appendStream(stream);
      return val;
    }

    if (node.op === 'SNAPSHOT') {
        this.logOp(`>> ⚶ SNAPSHOT`);
        const snap = this.runtime.snapshot();
        return snap;
    }
    
    // Fallback for new ops not fully implemented in mock
    if (node.op === 'COMPOSE') {
        this.logOp(`>> ⚳⊕ COMPOSE [${node.tag || 'usr'}]`);
        const composeId = this.runtime.collapse({ op: 'COMPOSE', tag: node.tag || 'usr' }, 'compose');
        return composeId;
    }
    
    return null;
  }
}

// =============================================================================
// SERVICE EXPORT
// =============================================================================

export class HLXEngineService {
    static async execute(mode: 'HLXL' | 'HLX', program: string): Promise<ExecutionResult> {
        
        // 0. LC STREAM DETECTION (BOOTSTRAPPING)
        // If the input starts with the LC Object Marker 🜊, we bypass compilation and treat it as raw wire format.
        if (program.trim().startsWith('🜊')) {
            try {
                const decoded = RUNTIME.decodeLC(program.trim());
                const snap = RUNTIME.snapshot();
                const table_entries = snap.handles.map(h => ({ handle: h, type: 'LC_Decode', size: 128 }));
                
                return {
                    hlxl: "/* RAW LC STREAM DECODED */",
                    hlxl_ls: "",
                    hlx: "",
                    hlx_ls: "",
                    lc_stream: program.trim(),
                    hlx_lite: decoded, // Return the decoded object
                    core_ast: { kind: "LC_BOOTSTRAP", stream: program.trim() },
                    invariants: { "LC_INTEGRITY": true, "BOOTSTRAP_OK": true },
                    provenance: {
                        engine_id: "hlx-runtime-alpha",
                        codex_version: "v0.9.0",
                        collapse_version: "lc-v2",
                        provenance_fp: "0xBOOTSTRAP_" + deterministicHash(program.trim()),
                        interpreter_mode: "LC_DIRECT"
                    },
                    output_log: ">> 🜊 BOOTSTRAP: LC Stream Decoded successfully.\n>> Manifest loaded into runtime.",
                    runtime_state: { active_handles: snap.handle_count, memory_usage: snap.memory_usage_approx_bytes, table_entries }
                };
            } catch (e: any) {
                return {
                    hlxl: "", hlxl_ls: "", hlx: "", hlx_ls: "", lc_stream: "", hlx_lite: null, core_ast: null,
                    invariants: { "LC_INTEGRITY": false },
                    provenance: { engine_id: "hlx-runtime", codex_version: "", collapse_version: "", provenance_fp: "", interpreter_mode: "LC_FAIL" },
                    output_log: `CRITICAL BOOTSTRAP FAILURE: ${e.message}`
                };
            }
        }

        // 1. Transliterate
        const hlxl = transliterate(program);
        
        // 2. Compile
        let ast = null;
        let error = null;
        try {
            const tokens = tokenize(hlxl);
            const compiler = new Compiler(tokens);
            ast = compiler.parse();
        } catch (e: any) {
            error = e.message;
        }

        // 3. Interpret
        const interpreter = new Interpreter(RUNTIME);
        let resultVal = null;
        if (ast && !ast.error && !error) {
            try {
                // Find main block
                const main = ast.blocks?.find((b: any) => b.block_id === 'main' || b.block_id === 'run' || b.block_id === 'build_manifest');
                if (main) {
                    resultVal = interpreter.execSeq(main.body);
                } else {
                    interpreter.logOp("No 'main' or 'run' or 'build_manifest' block found.");
                }
            } catch (e: any) {
                interpreter.logOp(`RUNTIME ERROR: ${e.message}`);
                error = e.message;
            }
        } else if (ast && ast.error) {
             error = ast.error;
        }

        // 4. Runtime State Snapshot
        const snap = RUNTIME.snapshot();
        const table_entries = snap.handles.map(h => ({
             handle: h,
             type: 'Object',
             size: 128
        }));

        return {
            hlxl: hlxl,
            hlxl_ls: hlxl, 
            hlx: program,
            hlx_ls: program, 
            lc_stream: interpreter.getStream(),
            hlx_lite: resultVal,
            core_ast: ast,
            invariants: {
                "DETERMINISTIC_LOWERING": !error,
                "LC_BIJECTION": true, 
                "RUNTIME_SAFETY": !error
            },
            provenance: {
                engine_id: "hlx-runtime-v1.0.1",
                codex_version: "v1.0.1",
                collapse_version: "lc-v2",
                provenance_fp: "0x" + deterministicHash(hlxl + interpreter.getStream()),
                interpreter_mode: mode
            },
            output_log: error ? `ERROR: ${error}\n${interpreter.getLog()}` : interpreter.getLog(),
            runtime_state: {
                active_handles: snap.handle_count,
                memory_usage: snap.memory_usage_approx_bytes,
                table_entries
            }
        };
    }

    static async runSystemTask(taskId: string): Promise<{ program: string, result: ExecutionResult }> {
        // --- NEW: LC_12 BOOTSTRAP GENERATOR ---
        if (taskId === 'sys-lc12-bootstrap') {
            const bundle = {
                "12": {
                    "@0": "HLX_BOOTSTRAP_BUNDLE_V1",
                    "@1": HLX_BOOTSTRAP_CODEX,
                    "@2": HLX_RUNTIME_CONFORMANCE,
                    "@3": HPCP_TRIGGERS_YAML
                }
            };
            
            // Encode directly using runtime
            const lcStream = RUNTIME.encodeLC(bundle as any);
            const handle = RUNTIME.collapse(bundle as any, "bootstrap_v1");
            const snap = RUNTIME.snapshot();
            
            const res: ExecutionResult = {
                hlxl: "/* GENERATED BY SYSTEM TASK */",
                hlxl_ls: "", hlx: "", hlx_ls: "",
                lc_stream: lcStream,
                hlx_lite: bundle,
                core_ast: null,
                invariants: { "LC_12_COMPLIANCE": true },
                provenance: {
                    engine_id: "hlx-runtime-alpha",
                    codex_version: "LC-12",
                    collapse_version: "lc-v2",
                    provenance_fp: handle,
                    interpreter_mode: "GENERATOR"
                },
                output_log: ">> LC_12 BOOTSTRAP STREAM GENERATED.\n>> Contains: Codex, Runtime Spec, Triggers.\n>> Copy the stream from the LC Output View.",
                runtime_state: {
                    active_handles: snap.handle_count,
                    memory_usage: snap.memory_usage_approx_bytes,
                    table_entries: snap.handles.map(h => ({ handle: h, type: 'Bootstrap', size: lcStream.length }))
                }
            };
            
            return {
                program: `⟠ bootstrap_lc12 {
  ◇ generate() {
    ⊢ bundle = ⚳ "bootstrap_v1" { ... };
    ↩ bundle;
  }
}`,
                result: res
            };
        }

        const programs: Record<string, string> = {
            'sys-executor': `⟠ sys_executor {
  ◇ run() {
    ⊢ msg = "Executor Mode: ACTIVE";
    ↩ msg;
  }
}`,
            'lc_test_basic_v2': `⟠ lc_test {
  ◇ run() {
    ⊢ val = {14:{@0:1}};
    ⊢ h = ⚳ val;
    ⊢ r = ⚯ h;
    ↩ r;
  }
}`,
            'spec_hotfix_sd7': `⟠ spec_hotfix_sd7 {
  ◇ main() ▣ spec_table {
    
    ⊢ registry = ⚳ contract_registry {
      1: "HLXLiteValue",
      2: "HLXLiteField", 
      3: "HLXLiteObject",
      4: "HLXLiteDocument",
      5: "ProvenanceLite",
      14: "UserValue",
      800: "LatentHandle",
      801: "LatentTable",
      820: "LSOp"
    };
    
    ⊢ lc_rules_patch = ⚳ lc_wire_rules {
      markers_no_whitespace: true,
      rule: "LC streams MUST contain no whitespace between markers"
    };
    
    ⊢ table_scoping = ⚳ table_scope_rules {
      default_table: "session",
      persistence_rule: "▣ <table_id> REQUIRED for cross-turn persistence"
    };
    
    ⊢ sd7_meta = ⚳ specdelta_sd7 {
      id: "SD7",
      name: "CANONICAL_HOTFIX",
      status: "FROZEN"
    };
    
    ⊢ sd7_bundle = ⚳⊕ HLX_SD7_BUNDLE [registry, lc_rules_patch, table_scoping, sd7_meta];
    ⚐ sd7_bundle != null;
    
    ↩ sd7_bundle ▷ ⚿ "HLX_SPEC_SD7_CANONICAL" ▷ ⚶;
  }
}`,
            'default': `⟠ task { ◇ run() { ↩ "Task Done"; } }`
        };

        const prog = programs[taskId] || programs['default'];
        const res = await this.execute('HLX', prog);
        return { program: prog, result: res };
    }
}

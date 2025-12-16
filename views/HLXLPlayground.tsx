
import React, { useState, useEffect } from 'react';
import { BookOpen, ArrowRight, Code, Database, Zap, Repeat, Layers, Terminal, Cpu, Network } from 'lucide-react';
import { HLX_UNIFIED_CODEX, STUDIO_LAYER_MAP } from '../data';
import { tokenize, Compiler } from '../utils/hlxl_compiler';

const HLXL_LAYER = STUDIO_LAYER_MAP._hlx_unified_codex.layers['1_track_a_lite'] || { status: 'UNKNOWN', description: 'HLXL Surface', contracts: {} };

type TaskKey = 'role' | 'compile_basic' | 'compile_ls' | 'pass_1_literals' | 'pass_2_operators' | 'pass_3_precedence' | 'pass_4_control_flow' | 'pass_5_expr_if' | 'pass_6_params' | 'pass_7_return' | 'pass_8_locals' | 'pass_9_while' | 'pass_10_foreach' | 'pass_11_calls' | 'pass_12_arrays' | 'pass_13_comments' | 'pass_14_objects' | 'pass_15_assert' | 'ls_pass_1_alias' | 'ls_pass_2_short' | 'ls_pass_3_bind' | 'ls_pass_4_resolve' | 'ls_pass_5_snapshot' | 'ls_pass_6_match' | 'ls_pass_7_guard' | 'ls_pass_8_batch_col' | 'ls_pass_9_batch_res' | 'ls_pass_10_pipeline' | 'ls_pass_11_scope' | 'ls_pass_12_compare' | 'ls_pass_13_resolve_or' | 'ls_pass_14_intro' | 'ls_pass_15_delete' | 'ls_pass_16_lazy' | 'ls_pass_17_alias' | 'ls_pass_18_scope' | 'ls_pass_19_watch' | 'ls_pass_20_compose' | 'ls_phase1_spec' | 'ls_phase2_spec' | 'ls_phase3_spec' | 'hlx_pass_0_spec' | 'hlxl_phase_omega_spec' | 'spec_invariant';

const TASKS: Record<TaskKey, {
    title: string;
    desc: string;
    code: string;
    expectedAST?: any;
    explanation?: React.ReactNode;
}> = {
    role: {
        title: "Foundation: Role Definition",
        desc: "Understand HLXL's place in the stack.",
        code: `program hlxl_role_demo {
  block definition {
    let role = "Surface Language";
    let target = "HLX-Core";
  }
}`,
        explanation: (
            <div className="space-y-2 text-sm text-hlx-muted">
                <p><strong>Goal:</strong> Zero ambiguity. "What you see is what executes".</p>
            </div>
        )
    },
    compile_basic: {
        title: "Foundation: Basic Compilation",
        desc: "Map 'let' and 'intrinsic' to CoreExprs.",
        code: `program demo {
  block main {
    let x = 1;
    let y = intrinsic add(x, 2);
  }
}`
    },
    compile_ls: {
        title: "Foundation: LS Integration",
        desc: "Map 'ls.collapse', 'ls.resolve', 'ls.snapshot'.",
        code: `program hello_world {
  block main {
    let ast_value = {14:{@0:123}};
    let ast_handle = ls.collapse bootstrap_table ast ast_value;
    let ast_round_trip = ls.resolve bootstrap_table ast_handle;
    let table_snapshot = ls.snapshot bootstrap_table;
  }
}`
    },
    pass_1_literals: {
        title: "Pass 1: Scalar Literals",
        desc: "Syntactic sugar for HLX-Lite values.",
        code: `program pass_1 {
  block literals {
    let a = 42;
    let b = 3.14;
    let msg = "hello";
    let flag = true;
    let nothing = null;
  }
}`,
        explanation: "Literals compile directly to CoreExpr LITERAL nodes with strongly typed HLX-Lite payloads."
    },
    pass_2_operators: {
        title: "Pass 2: Operators",
        desc: "Arithmetic & Logic sugar over intrinsics.",
        code: `program pass_2 {
  block math {
    let sum = 1 + 2 * 3;
    let is_equal = x == 10;
    let ok = flag && (count > 0);
    let neg = !flag;
  }
}`,
        explanation: "Operators like '+' are desugared into APPLY_INTRINSIC ops (e.g., 'add') during compilation."
    },
    pass_3_precedence: {
        title: "Pass 3: Precedence",
        desc: "Deterministic grouping rules.",
        code: `program pass_3 {
  block grouping {
    let a = 1 + 2 * 3;          // 1 + (2 * 3)
    let b = (1 + 2) * 3;        // (1 + 2) * 3
    let c = a > 0 && b < 10;    // (a > 0) && (b < 10)
  }
}`,
        explanation: "The compiler enforces standard precedence: unary (!) > multiplicative (*,/) > additive (+,-) > relational (==,<) > logical (&&,||)."
    },
    pass_4_control_flow: {
        title: "Pass 4: Control Flow",
        desc: "If/Else statements mapped to SEQ/IF.",
        code: `program pass_4 {
  block logic {
    if (flag) {
      let mode = "fast";
    } else {
      let mode = "safe";
    }
  }
}`,
        explanation: "Control flow blocks are compiled into nested SEQ expressions wrapped in an IF CoreExpr."
    },
    pass_5_expr_if: {
        title: "Pass 5: Expression If",
        desc: "Conditional expressions in bindings.",
        code: `program pass_5 {
  block conditional_bind {
    let mode = if (flag) {
      "fast";
    } else {
      "safe";
    };
  }
}`,
        explanation: "If/Else can be used as an expression (RHS). The result of the block (last expression) becomes the value."
    },
    pass_6_params: {
        title: "Pass 6: Block Params",
        desc: "Functions with arguments.",
        code: `program pass_6 {
  block compute(a, b) {
    let result = a + b;
  }
}`,
        explanation: "Blocks can now take parameters. These are compiled into the 'params' field of the CoreBlock definition."
    },
    pass_7_return: {
        title: "Pass 7: Return",
        desc: "Early exit from blocks.",
        code: `program pass_7 {
  block checker(val) {
    if (val < 0) {
      return 0;
    }
    return val;
  }
}`,
        explanation: "Return statements emit a specialized CoreExpr (or intrinsic) that triggers frame completion with a result."
    },
    pass_8_locals: {
        title: "Pass 8: Locals",
        desc: "Frame-scoped variables.",
        code: `program pass_8 {
  block scope_test() {
    local temp = 10;
    let global = 20;
    // 'temp' is discarded when frame pops
    // 'global' persists in CoreState
  }
}`,
        explanation: "The 'local' keyword emits SET_LOCAL instead of SET_VAR. These affect the ephemeral stack frame, not the persistent state."
    },
    pass_9_while: {
        title: "Pass 9: While Loops",
        desc: "Recursion lowering.",
        code: `program pass_9 {
  block loop_demo() {
    let x = 0;
    while (x < 5) {
      let x = x + 1;
    }
  }
}`,
        explanation: "While loops are lowered into a conditional (IF) containing the body followed by a recursive jump to the start."
    },
    pass_10_foreach: {
        title: "Pass 10: For-Each",
        desc: "Array iteration desugaring.",
        code: `program pass_10 {
  block iter_demo() {
    let values = [10, 20, 30];
    let total = 0;
    for (v in values) {
      let total = total + v;
    }
  }
}`,
        explanation: "For-loops are desugared into index-based while loops using array intrinsics (array_len, array_get)."
    },
    pass_11_calls: {
        title: "Pass 11: Block Calls",
        desc: "Invoking other blocks.",
        code: `program pass_11 {
  block add(a, b) {
    return a + b;
  }
  
  block main {
    let result = add(10, 20);
  }
}`,
        explanation: "Calling a block compiles to a CALL_BLOCK expression. This creates a new stack frame, executes the target block, and returns its result."
    },
    pass_12_arrays: {
        title: "Pass 12: Arrays",
        desc: "Literals and Indexing.",
        code: `program pass_12 {
  block main {
    let arr = [1, 2, 3];
    let first = arr[0];
    let last = arr[2];
  }
}`,
        explanation: "Array literals compile to LITERAL (if constant) or array construction intrinsics. Indexing 'arr[i]' maps to 'array_get(arr, i)'."
    },
    pass_13_comments: {
        title: "Pass 13: Comments",
        desc: "Line and Block comments.",
        code: `program pass_13 {
  block main {
    // This is a line comment
    let x = 1; 
    /* 
       This is a block comment.
       It spans multiple lines.
    */
    let y = 2;
  }
}`,
        explanation: "Comments are stripped during tokenization and do not appear in the compiled AST."
    },
    pass_14_objects: {
        title: "Pass 14: Objects",
        desc: "Structured object literals.",
        code: `program pass_14 {
  block main {
    let obj = object 14 {
      @0: 123,
      @1: "data"
    };
  }
}`,
        explanation: "The 'object' keyword allows constructing HLX-Lite objects with explicit Contract IDs and Field Indexes."
    },
    pass_15_assert: {
        title: "Pass 15: Assert",
        desc: "Runtime invariant checks.",
        code: `program pass_15 {
  block main {
    let x = 10;
    assert(x > 0);
    assert(x < 100);
  }
}`,
        explanation: "Assert statements compile to 'APPLY_INTRINSIC(assert, [cond])'. Failures halt execution."
    },
    ls_pass_1_alias: {
        title: "LS 1: Latent Tables",
        desc: "Defining table aliases.",
        code: `latent table bootstrap_table;

program ls_demo {
  block main {
    // 'bootstrap_table' is now a known alias
  }
}`,
        explanation: "Latent table declarations map aliases to IDs at compile time. No code is emitted, but the compiler tracks 'bootstrap_table' for future ops."
    },
    ls_pass_2_short: {
        title: "LS 2: Short Ops",
        desc: "Implicit table ops.",
        code: `latent table bootstrap_table;

program ls_demo {
  block main using bootstrap_table {
    // 'ls.collapse' now implies 'bootstrap_table'
    let h = ls.collapse tag {14:{@0:1}};
  }
}`,
        explanation: "When a block specifies 'using <table>', LS operations like 'ls.collapse' can omit the table argument."
    },
    ls_pass_3_bind: {
        title: "LS 3: Latent Bind",
        desc: "Collapse & bind sugar.",
        code: `latent table bootstrap_table;

program ls_demo {
  block main using bootstrap_table {
    let val = {14:{@0:1}};
    // Collapses 'val' into 'bootstrap_table' with tag 'my_data'
    // Binds handle to variable 'my_data'
    latent my_data = val;
  }
}`,
        explanation: "'latent NAME = EXPR' is sugar for: let NAME = ls.collapse(NAME, EXPR)."
    },
    ls_pass_4_resolve: {
        title: "LS 4: Resolve Bind",
        desc: "Resolve & bind sugar.",
        code: `latent table bootstrap_table;

program ls_demo {
  block main using bootstrap_table {
    let h = "&h_tag_123";
    // Resolves handle 'h' from 'bootstrap_table'
    // Binds value to variable 'res'
    latent value res = h;
  }
}`,
        explanation: "'latent value NAME = HANDLE' is sugar for: let NAME = ls.resolve(HANDLE)."
    },
    ls_pass_5_snapshot: {
        title: "LS 5: Snapshot",
        desc: "Snapshot binding.",
        code: `latent table bootstrap_table;

program ls_demo {
  block main using bootstrap_table {
    // Snapshots 'bootstrap_table' (with values)
    // Binds document to 'snap'
    latent snapshot snap;
  }
}`,
        explanation: "'latent snapshot NAME' is sugar for: let NAME = ls.snapshot()."
    },
    ls_pass_6_match: {
        title: "LS 6: Latent Match",
        desc: "Pattern matching resolve.",
        code: `latent table bootstrap_table;

program ls_demo {
  block main using bootstrap_table {
    let h = "&h_ast_1";
    // Resolves 'h', binds to 'node', executes block
    latent match node = h {
       let x = node.@0;
    }
  }
}`,
        explanation: "'latent match VAR = HANDLE { BODY }' resolves the handle to VAR and executes BODY. Lowers to SEQ(SET_LOCAL, BODY)."
    },
    ls_pass_7_guard: {
        title: "LS 7: Latent Guard",
        desc: "LS Context Assertions.",
        code: `latent table bootstrap_table;

program ls_demo {
  block main using bootstrap_table {
    latent match node = "&h_ast_1" {
       // Asserts condition or halts
       latent guard (node != null);
    }
  }
}`,
        explanation: "'latent guard EXPR' desugars to 'assert(EXPR)'. Semantic sugar for invariants within LS operations."
    },
    ls_pass_8_batch_col: {
        title: "LS 8: Batch Collapse",
        desc: "Array collapse sugar.",
        code: `latent table bootstrap_table;

program ls_demo {
  block main using bootstrap_table {
    let vals = [10, 20, 30];
    // Collapses all items in 'vals'
    // Binds array of handles to 'handles'
    latent batch handles = vals;
  }
}`,
        explanation: "'latent batch NAME = ARRAY' compiles to a loop/map operation that collapses every element and returns a list of handles."
    },
    ls_pass_9_batch_res: {
        title: "LS 9: Batch Resolve",
        desc: "Array resolve sugar.",
        code: `latent table bootstrap_table;

program ls_demo {
  block main using bootstrap_table {
    let handles = ["&h_1", "&h_2"];
    // Resolves all handles in 'handles'
    // Binds array of values to 'results'
    latent resolve batch results = handles;
  }
}`,
        explanation: "'latent resolve batch NAME = HANDLES' compiles to a loop/map operation that resolves every handle and returns a list of values."
    },
    ls_pass_10_pipeline: {
        title: "LS 10: Pipelines",
        desc: "Sequential LS Transforms.",
        code: `latent table bootstrap_table;

program ls_demo {
  block main using bootstrap_table {
    let val = {14:{@0:1}};
    
    // Pipe value -> collapse -> resolve
    let round_trip = val 
      |> ls.collapse tag 
      |> ls.resolve;
  }
}`,
        explanation: "The '|>' operator pipes the LHS as the *implicit* argument to the LS operation on the RHS. desugars to nested calls."
    },
    ls_pass_11_scope: {
        title: "LS 11: Latent Scope",
        desc: "Nested table contexts.",
        code: `latent table work_table;
        
program ls_demo {
  block main {
    latent scope work_table {
      // 'work_table' is active here
      latent ast = object 14 { @0: 123 };
    }
  }
}`,
        explanation: "Scopes push/pop active tables, allowing temporary context switching within a block."
    },
    ls_pass_12_compare: {
        title: "LS 12: Comparators",
        desc: "Value eq vs Handle identity.",
        code: `latent table t;

program ls_demo {
  block main using t {
    let h1 = "&h_1";
    let h2 = "&h_2";
    
    let is_same_content = h1 ls.eq h2;
    let is_same_handle = h1 ls.same h2;
    let fp = ls.fingerprint h1;
  }
}`,
        explanation: "ls.eq compares resolved values. ls.same compares handles. ls.fingerprint extracts content hash."
    },
    ls_pass_13_resolve_or: {
        title: "LS 13: Conditional Resolve",
        desc: "Resolution with fallback.",
        code: `latent table t;

program ls_demo {
  block main using t {
    let h = "&h_missing";
    // Returns null if handle not found instead of error
    let val = ls.resolve_or(h, null);
  }
}`,
        explanation: "ls.resolve_or(handle, default) checks existence before resolving, providing safe fallback."
    },
    ls_pass_14_intro: {
        title: "LS 14: Introspection",
        desc: "Table queries.",
        code: `latent table t;

program ls_demo {
  block main using t {
    if (ls.exists(h)) {
       let n = ls.count(t);
       let all = ls.handles(t);
    }
  }
}`,
        explanation: "Intrinsics for querying table state: ls.exists, ls.count, ls.handles."
    },
    ls_pass_15_delete: {
        title: "LS 15: Destructive Ops",
        desc: "Delete and Clear.",
        code: `latent table t;

program ls_demo {
  block main using t {
    ls.delete t h;
    ls.clear t;
  }
}`,
        explanation: "Explicit state mutation commands. These emit specific CoreDelta actions."
    },
    ls_pass_16_lazy: {
        title: "LS 16: Lazy Handles",
        desc: "Deferred evaluation.",
        code: `latent table t;

program ls_demo {
  block main using t {
    // Returns a handle, but 'expensive_op' is not run yet
    let h = ls.lazy "calc" expensive_op();
    
    // Forces evaluation now
    let val = ls.force h;
  }
}`,
        explanation: "Lazy handles delay collapse until explicitly forced. Useful for optimizing large dependency graphs."
    },
    ls_pass_17_alias: {
        title: "LS 17: Aliasing",
        desc: "Human-readable tags.",
        code: `latent table t;

program ls_demo {
  block main using t {
    let h = "&h_auto_generated_123";
    ls.alias "current_version" h;
    // Now accessible via "&h_current_version"
    ls.unalias "current_version";
  }
}`,
        explanation: "Aliases provide stable names for handles, useful for environment pointers (e.g., 'latest', 'prod')."
    },
    ls_pass_18_scope: {
        title: "LS 18: Scoped Tables",
        desc: "Ephemeral tables.",
        code: `program ls_demo {
  block main {
    ls.scope "temp_layer" {
       let h = ls.collapse "tmp" 123;
       // Promote to permanent storage
       let p = ls.promote "global" h;
    }
    // 'temp_layer' handles are dropped here
  }
}`,
        explanation: "ls.scope creates a temporary sub-table. 'promote' moves artifacts to parent/global storage before the scope ends."
    },
    ls_pass_19_watch: {
        title: "LS 19: Watchers",
        desc: "Reactivity triggers.",
        code: `latent table t;

program ls_demo {
  block main using t {
    ls.watch "w1" "&h_target";
    
    ls.on_change "w1" {
       let new_val = ls.resolve "&h_target";
       // reactive logic...
    }
    
    ls.unwatch "w1";
  }
}`,
        explanation: "Watchers register callbacks that trigger when a specific handle is updated (re-collapsed with new value)."
    },
    ls_pass_20_compose: {
        title: "LS 20: Composition",
        desc: "Structural handles.",
        code: `latent table t;

program ls_demo {
  block main using t {
    let h1 = "&h_part_1";
    let h2 = "&h_part_2";
    
    // Create composite handle without embedding values
    let c = ls.compose "group" [h1, h2];
    
    let parts = ls.decompose c;
    let sub = ls.project c [0];
  }
}`,
        explanation: "Composition allows building handles that reference other handles without resolving the underlying values."
    },
    ls_phase1_spec: {
        title: "Phase 1: Validation",
        desc: "Strict invariant checks for HLX-LS.",
        code: `latent table t1;

program spec_check {
  block main using t1 {
    // Valid: Explicit table context
    latent val = {14:{@0:1}};
    let h = ls.collapse tag val;
  }
  
  block bad {
    // Should fail (2006): No active table
    // let h = ls.collapse tag {14:{@0:1}};
    
    // Should fail (2002): Unknown table
    // ls.delete unknown_table "&h_1";
  }
}`,
        explanation: "This pass enforces error codes 2000-2011, ensuring all implicit LS operations occur within a valid 'using' scope or explicit table context."
    },
    ls_phase2_spec: {
        title: "Phase 2: Normalization",
        desc: "Sugar normalization and semantic invariants.",
        code: `latent table bootstrap_table;

program hlxl_ls_completion_phase2 {
  block main using bootstrap_table {
    // N1: Latent Bind
    // latent x = expr;
    // normalizes to:
    // let __v = expr;
    // let x = ls.collapse bootstrap_table __v;
    
    let v0 = {14:{@0:123}};
    latent ast = v0;
    
    // N3: Latent Snapshot
    // latent snapshot s;
    // normalizes to:
    // let s = ls.snapshot bootstrap_table;
    
    latent snapshot s1;
    
    // N9: Pipeline
    // expr |> f
    // normalizes to:
    // let __p0 = expr;
    // let __p1 = f(__p0);
    
    let rt = v0 |> ls.collapse t |> ls.resolve;
  }
}`,
        explanation: "Phase 2 defines how high-level sugar (latent bind, pipeline) normalizes to primitive LS_OPs and enforces semantic invariants (determinism, injectivity)."
    },
    ls_phase3_spec: {
        title: "Phase 3: Completion",
        desc: "Round-trip & Multi-table Invariants.",
        code: `latent table t1;
latent table t2;

program hlxl_ls_completion_phase3 {
  
  // RT-PASS-1: Round-Trip (Value)
  block rt_value using t1 {
    let v = {14:{@0:123}};
    latent ast = v;
    latent value rt = ast;
    assert(rt.@0 == 123);
  }

  // MT-1: Table Isolation
  block mt_isolation {
    ls.scope t1 {
       latent h1 = {14:{@0:1}};
       // Resolving h1 in t2 should generally be invalid or separate
    }
  }

  // PL-2: Pipeline Associativity
  block pl_assoc using t1 {
    let v = {14:{@0:5}};
    let r1 = v |> ls.collapse tag |> ls.resolve;
    // Equivalent to:
    let r2 = ls.resolve(ls.collapse tag v);
    assert(r1.@0 == r2.@0);
  }
}`,
        explanation: "Phase 3 locks the final round-trip, multi-table, and pipeline composition guarantees for the 1.0 specification."
    },
    hlx_pass_0_spec: {
        title: "Spec: HLX Pass 0",
        desc: "Core Glyph Surface & Transliteration.",
        code: `program hlx_pass_0_core_surface {
  block glyph_legend {
    // CORE STRUCTURAL GLYPHS (ASCII EQUIVALENTS)
    // ⟠  -> program
    // ◇  -> block
    // ⊢  -> let
    // ⊡  -> local (or set)
    // ↩  -> return
    // ❓  -> if
    // ❗  -> else
    // ⟳  -> while
    // ⟲  -> for
  }
  
  block rules {
    // TR-1: Program header
    // ⟠ name { ... } MUST transliterate to program name { ... }
    
    // TR-2: Block definition
    // ◇ name(params) { ... } MUST transliterate to block name(params) { ... }

    // TR-3: Variable binding
    // ⊢ x = expr; MUST transliterate to let x = expr;
    
    // TR-4: Assignment / mutation
    // ⊡ x = expr; MUST transliterate to local x = expr;

    // TR-5: Return
    // ↩ expr; MUST transliterate to return expr;

    // TR-6: If / else
    // ❓ (cond) { ... } ❗ { ... } MUST transliterate to if (cond) { ... } else { ... }

    // TR-7: While loop
    // ⟳ (cond) { ... } MUST transliterate to while (cond) { ... }
  }
}`,
        explanation: "HLX Pass 0 defines the pure syntactic sugar layer. Glyphs map 1:1 to ASCII keywords. No semantic changes are introduced in this pass."
    },
    hlxl_phase_omega_spec: {
        title: "Spec: Phase Ω (Final)",
        desc: "Canonical Grammar & Forbidden Constructs.",
        code: `program hlxl_completion_phase_omega {

  //-----------------------------------------------------------------
  // 1. CANONICAL BLOCK + FUNCTION GRAMMAR
  //-----------------------------------------------------------------
  block canonical_blocks {

    // BG-1: Canonical program.
    //
    //   program <identifier> { <body> }
    //
    // where:
    //   - <identifier> matches [A-Za-z_][A-Za-z0-9_]*
    //   - <body> is a sequence of top-level declarations (blocks, latents, etc.)
    //   - No extra tokens before "program".
    //   - No trailing tokens after closing "}" other than EOF/comments.

    // BG-2: Canonical block.
    //
    //   block <identifier>(<param_list>) { <body> }
    //
    // where:
    //   - Parentheses are MANDATORY, even if there are no params.
    //   - <param_list> is:
    //       • empty, or
    //       • one or more identifiers separated by commas: "x", "x,y", ...
    //   - No trailing comma is allowed: "x,y," is INVALID.
    //   - <body> is a sequence of statements.
    //
    // Valid:
    //   block main() { ... }
    //   block sum(a,b) { ... }
    //
    // Invalid:
    //   block main { ... }          // MISSING ()
    //   block sum(a,b,) { ... }     // TRAILING COMMA

    // BG-3: Parameter uniqueness.
    //
    //   Each parameter name within a block MUST be unique.
    //
    // Invalid:
    //   block f(x,x) { ... }  // duplicate parameter name

    // BG-4: Statement termination.
    //
    //   - All simple statements MUST be terminated by ";".
    //   - "block" definitions and control-flow blocks are terminated by "}".
  }

  //-----------------------------------------------------------------
  // 2. CANONICAL EXPRESSION GRAMMAR + PRECEDENCE
  //-----------------------------------------------------------------
  block canonical_expressions {

    // EG-1: Expression categories.
    //
    //   Primary:
    //     - literals (integer, float, string, boolean, null)
    //     - identifiers
    //     - parenthesized expressions: (expr)
    //     - array literals: [expr, ...]
    //     - object literals: object <id> { @0:expr, ... }
    //
    //   Postfix:
    //     - indexing: expr[expr]
    //     - call:     expr(expr_list)
    //
    //   Unary:
    //     - "-" expr
    //     - "!" expr
    //
    //   Binary (in order of increasing precedence):
    //
    //     1) "||"
    //     2) "&&"
    //     3) "==" "!="
    //     4) "<" "<=" ">" ">="
    //     5) "+" "-"
    //     6) "*" "/" "%"
    //
    //   All binary operators are left-associative.

    // EG-2: Parentheses canonicality.
    //
    //   - Parentheses MUST be used whenever operator precedence would
    //     otherwise be ambiguous to a human reader.
    //   - "((a))" and similar redundant nesting is discouraged but allowed
    //     as long as it does not change the AST.
    //
    //   Engines MUST interpret:
    //     a + b * c   as a + (b * c)
    //     a && b || c as (a && b) || c
    //
    //   If a model's parser cannot respect this table, it is non-conformant.

    // EG-3: Disallowed inline declarations in expressions.
    //
    //   The following are forbidden:
    //     - "let" inside an expression context.
    //     - "block" inside an expression context.
    //
    //   Examples (INVALID):
    //
    //     let x = (let y = 1; y);    // "let" inside expression
    //     let f = block g() { ... }; // block as expression
    //
    //   These MUST be rejected at parse or validation time.

    // EG-4: Boolean context.
    //
    //   - Conditions inside "if", "while", etc. MUST be expressions that
    //     evaluate to boolean values (true/false).
    //   - Engines MAY perform runtime checks for type correctness.
  }

  //-----------------------------------------------------------------
  // 3. FORBIDDEN CONSTRUCTS (FAIL-CLOSED)
  //-----------------------------------------------------------------
  block forbidden_constructs {

    // FC-1: Shadowing with "let" in same scope.
    //
    //   - Within a single block, it is ILLEGAL to use "let" twice with
    //     the same variable name.
    //
    //   Valid:
    //     block f() {
    //       let x = 1;
    //       x = 2;         // using assignment (if supported)
    //     }
    //
    //   Invalid:
    //     block f() {
    //       let x = 1;
    //       let x = 2;     // shadowing in same lexical scope
    //     }

    // FC-2: Mixed tabs and spaces in indentation (if indentation is used).
    //
    //   - A file MUST choose either all spaces or all tabs for leading
    //     indentation (or none at all).
    //   - Mixed indentation styles MUST be rejected or normalized before
    //     parse.
    //
    //   (If the engine ignores indentation, this rule can be treated as
    //    a style/linters-only requirement.)

    // FC-3: Trailing comma in arrays.
    //
    //   - Arrays MUST follow strict HLX-Lite rules: no trailing commas.
    //
    //   Valid:
    //     [1,2,3]
    //
    //   Invalid:
    //     [1,2,3,]

    // FC-4: Trailing comma in object literal field list.
    //
    //   - HLX-Lite objects MUST NOT have trailing commas:
    //
    //   Valid:
    //     object 14 { @0:1,@1:2 }
    //
    //   Invalid:
    //     object 14 { @0:1,@1:2, }

    // FC-5: Implicit returns.
    //
    //   - All return values MUST be explicit via "return expr;".
    //   - Falling off the end of a block without "return" is only allowed
    //     for blocks that conceptually return void.
    //
    //   Invalid:
    //     block f() {
    //       1 + 2;   // last expression does NOT act as return
    //     }

    // FC-6: Stray semicolons as statements (strong mode).
    //
    //   - A bare ";" is discouraged; engines MAY treat it as an empty
    //     statement, but strong conformance SHOULD reject multiple stray
    //     semicolons in sequence as suspicious.
  }

  //-----------------------------------------------------------------
  // 4. DETERMINISTIC LOWERING TO COREEXPR
  //-----------------------------------------------------------------
  block deterministic_lowering {

    // DL-1: Let vs Set.
    //
    //   HLXL distinguishes:
    //
    //     let x = expr;   // declaration + initialization
    //     x = expr;       // assignment to existing binding
    //
    //   Lowering:
    //     - "let x = expr;"  -> CoreExpr.SET_VAR with is_new_binding = true
    //     - "x = expr;"      -> CoreExpr.SET_VAR with is_new_binding = false
    //
    //   Engines MUST fail-closed if "x = expr;" is used without prior
    //   declaration of "x" in reachable scope.

    // DL-2: If / else lowering.
    //
    //   HLXL:
    //     if (cond) { then_body }
    //     else { else_body }
    //
    //   MUST lower to a single CoreExpr.IF node:
    //
    //     IF {
    //       @0: cond_expr,
    //       @1: then_seq,
    //       @2: else_seq
    //     }
    //
    //   Where:
    //     then_seq, else_seq are SEQ CoreExpr lists.
    //
    //   If there is no "else" in the source, else_seq MUST be an empty SEQ.

    // DL-3: While lowering.
    //
    //   HLXL:
    //     while (cond) { body }
    //
    //   MUST lower to a canonical loop form, e.g.:
    //
    //     LOOP {
    //       @0: cond_expr,
    //       @1: body_seq
    //     }
    //
    //   The exact contract ID is defined at Core layer, but the mapping
    //   MUST be 1:1 for all while loops.

    // DL-4: For-each lowering.
    //
    //   HLXL:
    //     for (x in xs) { body }
    //
    //   MUST lower to a SEQ equivalent of:
    //
    //     let __arr = xs;
    //     let __len = array_len(__arr);
    //     let __i   = 0;
    //     while (__i < __len) {
    //       let x = __arr[__i];
    //       body
    //       __i = __i + 1;
    //     }
    //
    //   with compiler-reserved temp names (__arr, __len, __i) that
    //   CANNOT collide with user code.

    // DL-5: Block as function.
    //
    //   A HLXL block with parameters MUST lower to a Core "function" or
    //   "block" expression where:
    //
    //     - parameters are captured in a fixed parameter list
    //     - body is a SEQ of CoreExpr
    //     - return is explicit
    //
    //   Lowering MUST be deterministic and independent of formatting.

    // DL-6: Expression lowering.
    //
    //   - Expressions MUST lower directly following the precedence and
    //     associativity rules from section canonical_expressions.
    //   - There MUST be no alternative lowering paths for a given expression
    //     AST. The AST itself is canonical.
  }

  //-----------------------------------------------------------------
  // 5. TESTS: MUST-PASS
  //-----------------------------------------------------------------
  block tests_must_pass {

    block t1_simple_block {
      // HLXL:
      //
      // program demo {
      //   block main() {
      //     let x = 1;
      //     let y = 2;
      //     let z = x + y * 3;
      //     return z;
      //   }
      // }
      //
      // MUST:
      //   - parse
      //   - obey precedence: y * 3, then x + (y * 3)
      //   - lower deterministically to CoreExpr tree
    }

    block t2_if_else {
      // HLXL:
      //
      // program demo {
      //   block main(flag) {
      //     if (flag) {
      //       return 1;
      //     } else {
      //       return 2;
      //     }
      //   }
      // }
      //
      // MUST:
      //   - produce a single IF CoreExpr with then_seq and else_seq.
    }

    block t3_while_loop {
      // HLXL:
      //
      // program demo {
      //   block main() {
      //     let i = 0;
      //     while (i < 3) {
      //       i = i + 1;
      //     }
      //     return i;
      //   }
      // }
      //
      // MUST:
      //   - lower to canonical LOOP CoreExpr.
      //   - result == 3.
    }

    block t4_for_each {
      // HLXL:
      //
      // program demo {
      //   block sum(xs) {
      //     let acc = 0;
      //     for (x in xs) {
      //       acc = acc + x;
      //     }
      //     return acc;
      //   }
      // }
      //
      // MUST:
      //   - lower to the SEQ+while canonical form defined in DL-4.
    }

    block t5_no_shadowing {
      // Valid:
      //
      // block f() {
      //   let x = 1;
      //   x = 2;
      //   return x;
      // }
      //
      // MUST:
      //   - parse and run.
    }
  }

  //-----------------------------------------------------------------
  // 6. TESTS: MUST-FAIL
  //-----------------------------------------------------------------
  block tests_must_fail {

    block f1_block_missing_parens {
      // INVALID:
      //
      // program demo {
      //   block main {
      //     return 0;
      //   }
      // }
      //
      // MUST be rejected: "block main" missing "()".
    }

    block f2_duplicate_param {
      // INVALID:
      //
      // block f(x,x) { return x; }
      //
      // MUST be rejected: duplicate parameter "x".
    }

    block f3_shadowing_let {
      // INVALID:
      //
      // block f() {
      //   let x = 1;
      //   let x = 2;   // same scope
      //   return x;
      // }
      //
      // MUST be rejected as shadowing in same scope.
    }

    block f4_trailing_array_comma {
      // INVALID:
      //
      // let xs = [1,2,3,];
      //
      // MUST be rejected: trailing comma.
    }

    block f5_trailing_object_comma {
      // INVALID:
      //
      // let o = object 14 { @0:1,@1:2, };
      //
      // MUST be rejected: trailing comma.
    }

    block f6_let_in_expression {
      // INVALID:
      //
      // let x = (let y = 1; y);
      //
      // MUST be rejected: "let" inside expression context.
    }

    block f7_block_expression {
      // INVALID:
      //
      // let f = block g() { return 1; };
      //
      // MUST be rejected: block used as expression.
    }
  }

  //-----------------------------------------------------------------
  // 7. MAIN (ANCHOR)
  //-----------------------------------------------------------------
  block main {
    let status = "HLXL completion phase Ω spec loaded (grammar + forbidden + deterministic lowering).";

    let report = object 999 {
      @0: "HLXL Completion Phase Ω",
      @1: "v1.0.0-final",
      @2: [
        object 998 { @0: "Grammar",   @1: "Canonical" },
        object 998 { @0: "Drift",     @1: "Eliminated" },
        object 998 { @0: "Lowering",  @1: "Deterministic" }
      ]
    };

    return report;
  }
}`,
        explanation: "Phase Ω freezes the HLXL grammar, explicitly forbids ambiguous constructs (shadowing, trailing commas, implicit returns), and mandates deterministic lowering to CoreExpr."
    },
    spec_invariant: {
        title: "Spec: ASCII Invariant",
        desc: "LITE-UNICODE-01 Definition",
        code: `program add_ascii_invariant_v1 {
  block main {
    let invariant = object 910 {
      @0: "LITE-UNICODE-01",
      @1: "No codepoint > 0x7F permitted in HLXL or HLXL/LS",
      @2: "Violation → E_LITE_NON_ASCII",
      @3: [
        "All identifiers must match ASCII [a-zA-Z0-9_]+",
        "All operators must be ASCII",
        "All string literals MUST contain only bytes in [0x20–0x7E]",
        "Reject Unicode whitespace, subscripts, glyphs, emojis, symbols"
      ]
    };

    return invariant;
  }
}`,
        explanation: "This program formally defines the ASCII-only constraint object (Contract 910) which engines must load during bootstrap."
    }
}


const HLXLPlayground: React.FC = () => {
  const [activeTask, setActiveTask] = useState<TaskKey>('role');
  const [sourceCode, setSourceCode] = useState(TASKS['role'].code);
  const [compiledAST, setCompiledAST] = useState<any>(null);

  const compile = (code: string) => {
      try {
          const tokens = tokenize(code);
          const compiler = new Compiler(tokens);
          const result = compiler.parse();
          setCompiledAST(result);
      } catch (e: any) {
          setCompiledAST({ error: e.message });
      }
  };

  useEffect(() => {
      setSourceCode(TASKS[activeTask].code);
      compile(TASKS[activeTask].code);
  }, [activeTask]);

  useEffect(() => {
      const timer = setTimeout(() => compile(sourceCode), 300);
      return () => clearTimeout(timer);
  }, [sourceCode]);


  return (
    <div className="space-y-8 animate-fade-in pb-12">
      <header>
        <h2 className="text-3xl font-bold text-white flex items-center gap-3">
          <BookOpen className="text-hlx-accent" />
          HLXL Compiler
        </h2>
        <div className="flex gap-4 mt-2 items-center">
             <p className="text-hlx-muted text-sm max-w-2xl">
                {HLXL_LAYER.description}
            </p>
            <span className="px-3 py-1 rounded-full border border-blue-500/20 bg-blue-500/10 text-blue-400 text-xs font-mono font-bold uppercase">
                {HLXL_LAYER.status}
            </span>
        </div>
      </header>

      {/* Task Tabs */}
      <div className="flex gap-2 bg-hlx-surface p-1 rounded-lg border border-hlx-border overflow-x-auto pb-2">
          {(Object.entries(TASKS) as [TaskKey, any][]).map(([key, task]) => (
              <button
                key={key}
                onClick={() => setActiveTask(key)}
                className={`flex items-center gap-2 px-3 py-2 rounded-md text-xs font-bold uppercase transition-colors whitespace-nowrap
                    ${activeTask === key ? 'bg-hlx-accent text-black shadow-lg shadow-hlx-accent/20' : 'text-hlx-muted hover:bg-hlx-bg hover:text-white border border-transparent hover:border-hlx-border'}
                `}
              >
                  {task.title.replace('Foundation:', '').replace('Pass ', 'P').replace('LS ', 'LS-').replace('Spec: ', '')}
              </button>
          ))}
      </div>

      <div className="bg-hlx-surface/50 border border-hlx-border rounded-xl p-4 flex items-center gap-4">
           <div className="p-2 bg-hlx-bg rounded-lg border border-hlx-border">
                {activeTask.includes('ls_') ? <Network size={24} className="text-pink-400" /> : activeTask.includes('pass') ? <Cpu size={24} className="text-green-400" /> : activeTask.includes('hlx_') ? <Zap size={24} className="text-yellow-400" /> : <Layers size={24} className="text-purple-400" />}
           </div>
           <div>
               <h3 className="text-white font-bold text-lg">{TASKS[activeTask].title}</h3>
               <p className="text-sm text-hlx-muted">{TASKS[activeTask].desc}</p>
           </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 h-[600px]">
          
          {/* Source Editor */}
          <div className="flex flex-col gap-2 h-full min-w-0">
               <div className="flex justify-between items-center px-1">
                   <span className="text-xs font-bold text-hlx-muted uppercase tracking-wider flex items-center gap-2">
                       <Code size={14} /> HLXL Source (ASCII)
                   </span>
               </div>
               <textarea 
                   className="flex-1 bg-[#09090b] border border-hlx-border rounded-xl p-4 font-mono text-sm leading-relaxed text-hlx-text focus:outline-none focus:border-hlx-accent/50 resize-none selection:bg-hlx-accent/30"
                   value={sourceCode}
                   onChange={(e) => setSourceCode(e.target.value)}
                   spellCheck={false}
               />
          </div>

          {/* Compiler Output */}
          <div className="flex flex-col gap-2 h-full min-w-0">
               <div className="flex justify-between items-center px-1">
                   <span className="text-xs font-bold text-hlx-muted uppercase tracking-wider flex items-center gap-2">
                       <Zap size={14} className="text-yellow-400" /> Compiled CoreExpr (AST)
                   </span>
                   <span className="text-[10px] text-yellow-400 bg-yellow-500/10 px-2 py-0.5 rounded border border-yellow-500/20">
                       Live Output
                   </span>
               </div>
               <div className="flex-1 bg-[#09090b] border border-hlx-border rounded-xl p-4 font-mono text-xs overflow-auto relative shadow-inner">
                   <pre className={`${compiledAST?.error ? 'text-red-400' : 'text-green-300'} whitespace-pre-wrap`}>
                       {JSON.stringify(compiledAST, null, 2)}
                   </pre>
               </div>
               {TASKS[activeTask].explanation && (
                   <div className="mt-2 p-3 bg-hlx-surface border border-hlx-border rounded-lg flex gap-3 items-start">
                       <Terminal size={16} className="text-hlx-accent mt-1 shrink-0" />
                       <div>
                            <h4 className="text-xs font-bold text-white mb-1 uppercase">Compiler Note</h4>
                            <div className="text-xs text-hlx-muted leading-relaxed">
                                {TASKS[activeTask].explanation}
                            </div>
                       </div>
                   </div>
               )}
          </div>
      </div>
      
      {/* Legend / Key */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 border-t border-hlx-border pt-6">
           <div className="p-3 bg-hlx-bg rounded border border-hlx-border">
               <div className="text-[10px] font-bold text-hlx-muted uppercase mb-1">Source Layer</div>
               <div className="text-sm font-bold text-white">HLXL (2.5)</div>
               <div className="text-xs text-hlx-muted">Human readable, ASCII only.</div>
           </div>
           <div className="flex items-center justify-center">
               <ArrowRight className="text-hlx-muted" />
           </div>
           <div className="p-3 bg-hlx-bg rounded border border-hlx-border">
               <div className="text-[10px] font-bold text-hlx-muted uppercase mb-1">Target Layer</div>
               <div className="text-sm font-bold text-white">HLX-Core (2.0)</div>
               <div className="text-xs text-hlx-muted">Machine executable, JSON AST.</div>
           </div>
      </div>
    </div>
  );
};

export default HLXLPlayground;

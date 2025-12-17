
// =============================================================================
// HLX GLYPH DEFINITIONS - PURE ASCII / UNICODE ESCAPE SEQUENCE VERSION
// =============================================================================
// This file guarantees that glyphs are loaded into memory correctly regardless
// of file encoding (UTF-8, Latin-1, etc) because it uses only ASCII characters.

export const GLYPH_MAP = {
  structure: {
    '\u27E0': 'program',      // ⟠
    '\u25C7': 'block',        // ◇
    '\u22A2': 'let',          // ⊢
    '\u22A1': 'local',        // ⊡
    '\u21A9': 'return'        // ↩
  },
  control: {
    '\u2753': 'if',           // ❓
    '\u2757': 'else',         // ❗
    '\u27F3': 'while',        // ⟳
    '\u27F2': 'foreach'       // ⟲
  },
  ls_core: {
    '\uA66E': 'latent',       // ꙮ
    '\u2338': 'table',        // ⌸
    '\u25A3': 'using',        // ▣
    '\u26B3': 'ls.collapse',  // ⚳
    '\u26AF': 'ls.resolve',   // ⚯
    '\u26B6': 'ls.snapshot',  // ⚶
    '\u25B7': '|>'            // ▷
  },
  ls_sugar: {
    '\u26B7': 'latent (bind)',       // ⚷
    '\u26B5': 'latent value',        // ⚵
    '\u26BB': 'latent snapshot (bind)', // ⚻
    '\u2691': 'latent match',        // ⚑
    '\u2690': 'latent guard',        // ⚐
    '\u26B3\u20F0': 'ls.batch_collapse',  // ⚳⃰
    '\u26AF\u20F0': 'ls.batch_resolve'    // ⚯⃰
  },
  ls_advanced: {
    '\u26B3?': 'ls.collapse_if',     // ⚳?
    '\u26AF\u2016': 'ls.resolve_or', // ⚯‖
    '\u26BF': 'ls.transaction',      // ⚿
    '\u2689': 'ls.fingerprint',      // ⚉
    '\u2687': 'ls.validate',         // ⚇
    '\u2338\u2442': 'ls.table_fork', // ⌸⑂
    '\u2338\u0394': 'ls.table_diff', // ⌸Δ
    '\u2338\u2295': 'ls.table_merge' // ⌸⊕
  },
  ls_passes_16_20: {
    '\u26B3~': 'ls.lazy',            // ⚳~
    '\u26AF!': 'ls.force',           // ⚯!
    '\u26B3\u2261': 'ls.alias',      // ⚳≡
    '\u26B3\u2262': 'ls.unalias',    // ⚳≢
    '\u2338{': 'ls.scope_begin',     // ⌸{
    '\u2338}': 'ls.scope_end',       // ⌸}
    '\u26B3\u2191': 'ls.promote',    // ⚳↑
    '\u26AD': 'ls.watch',            // ⚭
    '\u26AE': 'ls.unwatch',          // ⚮
    '\u26AD\u2192': 'ls.on_change',  // ⚭→
    '\u26B3\u2295': 'ls.compose',    // ⚳⊕
    '\u26AF\u2296': 'ls.decompose',  // ⚯⊖
    '\u26AF\u03C0': 'ls.project'     // ⚯π
  },
  latent_collapse: {
    '\uD83D\uDF0A': 'lc.obj_begin',     // 🜊 (surrogate pair)
    '\uD83D\uDF02': 'lc.obj_end',       // 🜂
    '\uD83D\uDF01': 'lc.field',         // 🜁
    '\uD83D\uDF03': 'lc.arr_begin',     // 🜃
    '\uD83D\uDF04': 'lc.arr_end',       // 🜄
    '\uD83D\uDF07': 'lc.handle_ref',    // 🜇
    '\u27C1': 'lc.handle_literal',      // ⟁
    '\uD83D\uDF0B': 'lc.doc_end'        // 🜋
  }
};

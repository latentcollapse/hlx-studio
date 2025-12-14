
export type TokenType = 
  | 'KEYWORD' | 'IDENT' | 'LITERAL_INT' | 'LITERAL_FLOAT' | 'LITERAL_STRING' 
  | 'SYMBOL' | 'OPERATOR' | 'HLX_LITE_BLOB' | 'EOF'
  | 'LAZY' | 'FORCE' | 'ALIAS' | 'UNALIAS' | 'SCOPE' | 'PROMOTE'
  | 'WATCH' | 'UNWATCH' | 'ON_CHANGE' | 'COMPOSE' | 'DECOMPOSE' | 'PROJECT';

export interface Token {
  type: TokenType;
  value: string;
  line: number;
}

export const KEYWORDS = new Set([
  'program', 'block', 'let', 'if', 'else', 'intrinsic', 
  'ls', 'collapse', 'resolve', 'snapshot', 'null', 'true', 'false',
  'return', 'local', 'while', 'for', 'in',
  'object', 'assert', 'latent', 'table', 'using', 'value',
  'match', 'guard', 'batch', 'scope', 'delete', 'clear',
  'lazy', 'force', 'alias', 'unalias', 'promote',
  'watch', 'unwatch', 'on_change', 'compose', 'decompose', 'project'
]);

export const tokenize = (input: string): Token[] => {
  let pos = 0;
  let line = 1;
  const tokens: Token[] = [];

  while (pos < input.length) {
    const char = input[pos];

    if (/\s/.test(char)) {
      if (char === '\n') line++;
      pos++;
      continue;
    }

    if (char === '/' && input[pos + 1] === '/') {
      while (pos < input.length && input[pos] !== '\n') pos++;
      continue;
    }

    if (char === '/' && input[pos + 1] === '*') {
      pos += 2;
      while (pos < input.length && !(input[pos] === '*' && input[pos + 1] === '/')) {
        if (input[pos] === '\n') line++;
        pos++;
      }
      pos += 2; 
      continue;
    }

    if (/[0-9]/.test(char)) {
      let value = '';
      while (pos < input.length && /[0-9.]/.test(input[pos])) {
        value += input[pos++];
      }
      tokens.push({ 
        type: value.includes('.') ? 'LITERAL_FLOAT' : 'LITERAL_INT', 
        value, 
        line 
      });
      continue;
    }

    if (/[a-zA-Z_]/.test(char)) {
      let value = '';
      while (pos < input.length && /[a-zA-Z0-9_.]/.test(input[pos])) {
        value += input[pos++];
      }
      
      if (KEYWORDS.has(value) || value.startsWith('ls.')) {
        tokens.push({ type: 'KEYWORD', value, line });
      } else {
        tokens.push({ type: 'IDENT', value, line });
      }
      continue;
    }

    if (char === '"') {
      let value = '';
      pos++; 
      while (pos < input.length) {
        if (input[pos] === '\\' && input[pos+1] === '"') {
            value += '\\"'; // Keep escape sequence
            pos += 2;
            continue;
        }
        if (input[pos] === '"') break;
        value += input[pos++];
      }
      pos++; 
      tokens.push({ type: 'LITERAL_STRING', value, line });
      continue;
    }

    // HLX_LITE_BLOB heuristic: starts with {number:
    if (char === '{' && /\d/.test(input[pos+1])) {
       let value = '';
       let braceCount = 0;
       let tempPos = pos + 1;
       let isBlob = false;
       while (tempPos < input.length && /\d/.test(input[tempPos])) tempPos++;
       if (input[tempPos] === ':') isBlob = true;

       if (isBlob) {
           while (pos < input.length) {
               const c = input[pos];
               value += c;
               if (c === '{') braceCount++;
               if (c === '}') braceCount--;
               pos++;
               if (braceCount === 0) break;
           }
           tokens.push({ type: 'HLX_LITE_BLOB', value, line });
           continue;
       }
    }

    const twoChar = input.substr(pos, 2);
    if (['==', '!=', '<=', '>=', '&&', '||', '|>'].includes(twoChar)) {
       tokens.push({ type: 'OPERATOR', value: twoChar, line });
       pos += 2;
       continue;
    }

    if (['+', '-', '*', '/', '<', '>', '!', '='].includes(char)) {
       tokens.push({ type: 'OPERATOR', value: char, line });
       pos++;
       continue;
    }
    
    if (['{', '}', '(', ')', '[', ']', ';', ',', '.', ':', '@'].includes(char)) {
       tokens.push({ type: 'SYMBOL', value: char, line });
       pos++;
       continue;
    }

    pos++; 
  }
  
  tokens.push({ type: 'EOF', value: '', line });
  return tokens;
};

export class Compiler {
    tokens: Token[];
    pos: number;
    latentTables: Set<string> = new Set();
    activeTable: string | null = null;

    constructor(tokens: Token[]) {
        this.tokens = tokens;
        this.pos = 0;
    }

    peek(): Token {
        return this.tokens[this.pos];
    }

    consume(expectedValue?: string): Token {
        const token = this.tokens[this.pos];
        if (expectedValue && token.value !== expectedValue) {
            throw new Error(`Syntax Error line ${token.line}: Expected '${expectedValue}', got '${token.value}'`);
        }
        this.pos++;
        return token;
    }

    check(type: TokenType, value?: string): boolean {
        const token = this.peek();
        if (token.type !== type) return false;
        if (value && token.value !== value) return false;
        return true;
    }

    parse() {
        while (this.check('KEYWORD', 'latent')) {
            this.consume('latent');
            this.consume('table');
            const name = this.consume().value;
            this.consume(';');
            if (this.latentTables.has(name)) {
                throw new Error(`E_LS_DUPLICATE_TABLE_ALIAS (2000): Table alias '${name}' already declared.`);
            }
            this.latentTables.add(name);
        }

        if (this.check('KEYWORD', 'program')) {
            const prog = this.parseProgram();
            if (this.check('KEYWORD', 'latent') && this.check('KEYWORD', 'table')) {
                throw new Error(`E_LS_ALIAS_AFTER_PROGRAM (2011): Latent table declarations must be top-level.`);
            }
            return prog;
        }
        return { error: "Code must start with 'program' (or 'latent table' declarations)" };
    }

    parseProgram() {
        this.consume('program');
        const id = this.consume().value; 
        this.consume('{');
        const blocks = [];
        while (!this.check('SYMBOL', '}')) {
            blocks.push(this.parseBlock());
        }
        this.consume('}');
        return { program_id: id, blocks };
    }

    parseBlock() {
        this.consume('block');
        const id = this.consume().value;
        
        let params: string[] = [];
        if (this.check('SYMBOL', '(')) {
            this.consume('(');
            if (!this.check('SYMBOL', ')')) {
                params.push(this.consume().value);
                while (this.check('SYMBOL', ',')) {
                    this.consume(',');
                    params.push(this.consume().value);
                }
            }
            this.consume(')');
        }

        let localActiveTable = this.activeTable;
        if (this.check('KEYWORD', 'using')) {
            this.consume('using');
            const tableName = this.consume().value;
            if (!this.latentTables.has(tableName)) {
                throw new Error(`E_LS_USING_UNDECLARED_TABLE (2002): Table alias '${tableName}' not declared.`);
            }
            localActiveTable = tableName;
        }

        const prevActiveTable = this.activeTable;
        this.activeTable = localActiveTable;

        this.consume('{');
        const body = this.parseBlockBody();
        this.consume('}');

        this.activeTable = prevActiveTable; 
        
        return { block_id: id, params, body };
    }

    parseBlockBody() {
        const body = [];
        while (!this.check('SYMBOL', '}')) {
            if (this.check('KEYWORD', 'if')) {
                body.push(this.parseIfStatement());
            } else {
                const stmt = this.parseStatement();
                if (stmt) body.push(this.lower(stmt));
            }
        }
        return body;
    }

    parseIfStatement(): any {
        this.consume('if');
        this.consume('(');
        const cond = this.parseExpression();
        this.consume(')');
        
        this.consume('{');
        const thenBody = this.parseBlockBody();
        this.consume('}');
        const thenBranch = { kind: 'SEQ', body: thenBody };

        let elseBranch = null;
        if (this.check('KEYWORD', 'else')) {
            this.consume('else');
            this.consume('{');
            const elseBody = this.parseBlockBody();
            this.consume('}');
            elseBranch = { kind: 'SEQ', body: elseBody };
        }

        return { 
            kind: 'IF', 
            payload: { cond: this.lower(cond), then_branch: thenBranch, else_branch: elseBranch } 
        };
    }

    parseStatement() {
        if (this.check('KEYWORD', 'let')) {
            this.consume('let');
            const name = this.consume().value;
            this.consume('=');
            let expr;
            if (this.check('KEYWORD', 'if')) {
                expr = this.parseIfExpression();
            } else {
                expr = this.parseExpression();
            }
            this.consume(';');
            return { kind: 'SET_VAR', payload: { name, expr } };
        }

        if (this.check('KEYWORD', 'local')) {
            this.consume('local');
            const name = this.consume().value;
            this.consume('=');
            const expr = this.parseExpression();
            this.consume(';');
            return { kind: 'SET_LOCAL', payload: { name, expr } };
        }
        
        if (this.check('KEYWORD', 'ls.delete')) {
            this.consume('ls.delete');
            const table = this.consume().value;
            const handleExpr = this.parseExpression();
            this.consume(';');
            return { kind: 'LS_OP', op: 'DELETE', table, handle: handleExpr };
        }
        if (this.check('KEYWORD', 'ls.clear')) {
            this.consume('ls.clear');
            const table = this.consume().value;
            this.consume(';');
            return { kind: 'LS_OP', op: 'CLEAR', table };
        }

        if (this.check('KEYWORD', 'ls.scope')) {
            this.consume('ls.scope');
            const scopeName = this.consume().value;
            this.consume('{');
            const body = this.parseBlockBody();
            this.consume('}');
            return { kind: 'LS_SCOPE', scope_name: scopeName, body };
        }
        
        if (this.check('KEYWORD', 'ls.on_change')) {
            this.consume('ls.on_change');
            const id = this.consume().value;
            this.consume('{');
            const body = this.parseBlockBody();
            this.consume('}');
            return { kind: 'LS_ON_CHANGE', watcher_id: id, handler_body: body };
        }
        
        if (this.check('KEYWORD', 'ls.watch')) {
            this.consume('ls.watch');
            const id = this.consume().value;
            const handle = this.parseExpression();
            this.consume(';');
            return { kind: 'LS_WATCH', watcher_id: id, handle_expr: handle };
        }
        if (this.check('KEYWORD', 'ls.unwatch')) {
            this.consume('ls.unwatch');
            const id = this.consume().value;
            this.consume(';');
            return { kind: 'LS_UNWATCH', watcher_id: id };
        }
        if (this.check('KEYWORD', 'ls.alias')) {
            this.consume('ls.alias');
            const tag = this.consume().value;
            const handle = this.parseExpression();
            this.consume(';');
            return { kind: 'LS_ALIAS', new_tag: tag, handle_expr: handle };
        }
        if (this.check('KEYWORD', 'ls.unalias')) {
            this.consume('ls.unalias');
            const tag = this.consume().value;
            this.consume(';');
            return { kind: 'LS_UNALIAS', tag: tag };
        }
        if (this.check('KEYWORD', 'ls.table_fork')) {
            this.consume('ls.table_fork');
            const newTable = this.consume().value;
            this.consume('from');
            const sourceTable = this.consume().value;
            this.consume(';');
            return { kind: 'LS_TABLE_FORK', new_table: newTable, source_table: sourceTable };
        }
        if (this.check('KEYWORD', 'ls.table_merge')) {
            this.consume('ls.table_merge');
            const src = this.consume().value;
            this.consume('into');
            const tgt = this.consume().value;
            this.consume(';');
            return { kind: 'LS_TABLE_MERGE', source: src, target: tgt };
        }

        if (this.check('KEYWORD', 'latent')) {
            this.consume('latent');
            
            if (this.check('KEYWORD', 'scope')) {
                this.consume('scope');
                const tableName = this.consume().value;
                const prevActiveTable = this.activeTable;
                this.activeTable = tableName;
                this.consume('{');
                const body = this.parseBlockBody();
                this.consume('}');
                this.activeTable = prevActiveTable;
                return { kind: 'SEQ', body: body, meta: `Latent Scope: ${tableName}` };
            }

            const requiresTable = 
                this.check('KEYWORD', 'value') || 
                this.check('KEYWORD', 'snapshot') || 
                this.check('KEYWORD', 'match') || 
                this.check('KEYWORD', 'batch') ||
                this.check('KEYWORD', 'resolve') ||
                !this.check('KEYWORD', 'guard'); 
            
            if (requiresTable && !this.activeTable) {
                 throw new Error("E_LS_LATENT_STMT_OUT_OF_SCOPE (2003): Implicit table operation requires 'using' block.");
            }

            if (this.check('KEYWORD', 'value')) {
                this.consume('value');
                const name = this.consume().value;
                this.consume('=');
                const handleExpr = this.parseExpression();
                this.consume(';');
                return { kind: 'SET_VAR', payload: { name, expr: { kind: 'LS_OP', op: 'RESOLVE', table: this.activeTable, handle: handleExpr } } };
            } else if (this.check('KEYWORD', 'snapshot')) {
                this.consume('snapshot');
                const name = this.consume().value;
                this.consume(';');
                return { kind: 'SET_VAR', payload: { name, expr: { kind: 'LS_OP', op: 'SNAPSHOT', table: this.activeTable, include_values: true } } };
            } else if (this.check('KEYWORD', 'match')) {
                 this.consume('match');
                 const name = this.consume().value;
                 this.consume('=');
                 const handleExpr = this.parseExpression();
                 this.consume('{');
                 const body = this.parseBlockBody();
                 this.consume('}');
                 return {
                     kind: 'SEQ',
                     body: [{ kind: 'SET_LOCAL', payload: { name, expr: { kind: 'LS_OP', op: 'RESOLVE', table: this.activeTable, handle: handleExpr } }}, ...body],
                     meta: 'Lowered from LATENT MATCH'
                 };
            } else if (this.check('KEYWORD', 'guard')) {
                this.consume('guard');
                const expr = this.parseExpression();
                this.consume(';');
                return { kind: 'APPLY_INTRINSIC', op: 'assert', args: [expr], meta: 'Latent Guard' };
            } else if (this.check('KEYWORD', 'batch')) {
                this.consume('batch');
                const name = this.consume().value;
                this.consume('=');
                const arrExpr = this.parseExpression();
                this.consume(';');
                return { kind: 'SET_VAR', payload: { name, expr: { kind: 'LS_BATCH_OP', op: 'COLLAPSE', table: this.activeTable, input: arrExpr } } };
            } else if (this.check('KEYWORD', 'resolve')) {
                 this.consume('resolve');
                 this.consume('batch');
                 const name = this.consume().value;
                 this.consume('=');
                 const arrExpr = this.parseExpression();
                 this.consume(';');
                 return { kind: 'SET_VAR', payload: { name, expr: { kind: 'LS_BATCH_OP', op: 'RESOLVE', table: this.activeTable, input: arrExpr } } };
            } else {
                const name = this.consume().value; 
                this.consume('=');
                const valExpr = this.parseExpression();
                this.consume(';');
                return { kind: 'SET_VAR', payload: { name, expr: { kind: 'LS_OP', op: 'COLLAPSE', table: this.activeTable, tag: name, val: valExpr } } };
            }
        }

        if (this.check('KEYWORD', 'return')) {
            this.consume('return');
            const expr = this.parseExpression();
            this.consume(';');
            return { kind: 'RETURN', payload: expr };
        }

        if (this.check('KEYWORD', 'assert')) {
            this.consume('assert');
            this.consume('(');
            const expr = this.parseExpression();
            this.consume(')');
            this.consume(';');
            return { kind: 'APPLY_INTRINSIC', op: 'assert', args: [expr] };
        }

        if (this.check('KEYWORD', 'while')) {
            return this.parseWhile();
        }

        if (this.check('KEYWORD', 'for')) {
            return this.parseFor();
        }
        
        const expr = this.parseExpression();
        if (this.check('SYMBOL', ';')) this.consume(';');
        return expr;
    }

    parseWhile() {
        this.consume('while');
        this.consume('(');
        const cond = this.parseExpression();
        this.consume(')');
        this.consume('{');
        const body = this.parseBlockBody();
        this.consume('}');
        
        const seqBody = [...body, { kind: 'RECURSIVE_JUMP', desc: 'Auto-inserted by compiler' }];
        
        return {
            kind: 'IF',
            payload: { cond: this.lower(cond), then_branch: { kind: 'SEQ', body: seqBody }, else_branch: null },
            meta: 'Lowered from WHILE'
        };
    }

    parseFor() {
        this.consume('for');
        this.consume('(');
        const iteratorName = this.consume().value; 
        this.consume('in');
        const collectionExpr = this.parseExpression();
        this.consume(')');
        this.consume('{');
        const body = this.parseBlockBody();
        this.consume('}');

        return {
             kind: 'SEQ',
             body: [
                 { kind: 'SET_LOCAL', payload: { name: '__arr', expr: this.lower(collectionExpr) } },
                 { kind: 'SET_LOCAL', payload: { name: '__idx', expr: { kind: 'LITERAL', value: 0 } } },
                 {
                     kind: 'IF',
                     payload: {
                         cond: { kind: 'APPLY_INTRINSIC', op: 'lt', args: [ 
                             { kind: 'VAR_REF', name: '__idx', source: 'LOCAL' },
                             { kind: 'APPLY_INTRINSIC', op: 'array_len', args: [{ kind: 'VAR_REF', name: '__arr', source: 'LOCAL' }] }
                         ]},
                         then_branch: {
                             kind: 'SEQ',
                             body: [
                                 { kind: 'SET_LOCAL', payload: { 
                                     name: iteratorName, 
                                     expr: { kind: 'APPLY_INTRINSIC', op: 'array_get', args: [
                                         { kind: 'VAR_REF', name: '__arr', source: 'LOCAL' }, 
                                         { kind: 'VAR_REF', name: '__idx', source: 'LOCAL' }
                                     ]} 
                                 }},
                                 ...body,
                                 { kind: 'SET_LOCAL', payload: {
                                     name: '__idx',
                                     expr: { kind: 'APPLY_INTRINSIC', op: 'add', args: [
                                         { kind: 'VAR_REF', name: '__idx', source: 'LOCAL' },
                                         { kind: 'LITERAL', value: 1 }
                                     ]}
                                 }},
                                 { kind: 'RECURSIVE_JUMP' }
                             ]
                         },
                         else_branch: null
                     }
                 }
             ],
             meta: "Lowered from FOR"
        };
    }

    parseIfExpression(): any {
        return this.parseIfStatement();
    }

    parseExpression(): any {
        return this.parsePipeline();
    }

    parsePipeline(): any {
        let left = this.parseLogicalOr();
        while (this.check('OPERATOR', '|>')) {
            this.consume('|>');
            if (this.peek().value.startsWith('ls.')) {
                 const opFull = this.consume().value;
                 const op = opFull.split('.')[1];
                 let table = this.activeTable || "UNKNOWN";
                 
                 if (op === 'collapse') {
                     const tag = this.consume().value; 
                     if (!this.activeTable) throw new Error("E_LS_PIPELINE_NO_ACTIVE_TABLE (2006): Pipeline stage requires active table.");
                     left = { kind: 'LS_OP', op: 'COLLAPSE', table, tag, val: left };
                 } else if (op === 'resolve') {
                     if (!this.activeTable) throw new Error("E_LS_PIPELINE_NO_ACTIVE_TABLE (2006): Pipeline stage requires active table.");
                     left = { kind: 'LS_OP', op: 'RESOLVE', table, handle: left };
                 } else if (op === 'lazy') {
                     const tag = this.consume().value;
                     left = { kind: 'LS_LAZY', tag, thunk_expr: left };
                 } else if (op === 'force') {
                     left = { kind: 'LS_FORCE', handle_expr: left };
                 } else if (op === 'decompose') {
                     left = { kind: 'LS_DECOMPOSE', handle_expr: left };
                 }
            } else {
                 const func = this.parsePostfix(); 
                 if (func.kind === 'CALL_BLOCK') {
                     func.args.unshift(left);
                     left = func;
                 } else if (func.kind === 'VAR_REF') {
                     left = { kind: 'CALL_BLOCK', target: func.name, args: [left] };
                 } else {
                     left = { kind: 'PIPELINE_APPLY', input: left, fn: func };
                 }
            }
        }
        return left;
    }

    parseLogicalOr(): any {
        let left = this.parseLogicalAnd();
        while (this.check('OPERATOR', '||')) {
            const op = this.consume().value;
            const right = this.parseLogicalAnd();
            left = { kind: 'APPLY_INTRINSIC', op: 'or', args: [left, right] };
        }
        return left;
    }

    parseLogicalAnd(): any {
        let left = this.parseEquality();
        while (this.check('OPERATOR', '&&')) {
            const op = this.consume().value;
            const right = this.parseEquality();
            left = { kind: 'APPLY_INTRINSIC', op: 'and', args: [left, right] };
        }
        return left;
    }

    parseEquality(): any {
        let left = this.parseRelational();
        while (this.check('OPERATOR', '==') || this.check('OPERATOR', '!=') || 
               (this.peek().type === 'KEYWORD' && (this.peek().value === 'ls.eq' || this.peek().value === 'ls.same'))) {
            let op = '';
            if (this.check('KEYWORD')) {
                 op = this.consume().value; 
            } else {
                 op = this.consume().value; 
            }
            const right = this.parseRelational();
            if (op === 'ls.eq') {
                left = { kind: 'APPLY_INTRINSIC', op: 'ls_eq', args: [left, right] };
            } else if (op === 'ls.same') {
                left = { kind: 'APPLY_INTRINSIC', op: 'ls_same', args: [left, right] };
            } else {
                left = { kind: 'APPLY_INTRINSIC', op: op === '==' ? 'eq' : 'ne', args: [left, right] };
            }
        }
        return left;
    }

    parseRelational(): any {
        let left = this.parseAdditive();
        while (['<', '<=', '>', '>='].includes(this.peek().value)) {
            const op = this.consume().value;
            const right = this.parseAdditive();
            const opMap: Record<string, string> = { '<': 'lt', '<=': 'le', '>': 'gt', '>=': 'ge' };
            left = { kind: 'APPLY_INTRINSIC', op: opMap[op], args: [left, right] };
        }
        return left;
    }

    parseAdditive(): any {
        let left = this.parseMultiplicative();
        while (['+', '-'].includes(this.peek().value)) {
            const op = this.consume().value;
            const right = this.parseMultiplicative();
            left = { kind: 'APPLY_INTRINSIC', op: op === '+' ? 'add' : 'sub', args: [left, right] };
        }
        return left;
    }

    parseMultiplicative(): any {
        let left = this.parseUnary();
        while (['*', '/'].includes(this.peek().value)) {
            const op = this.consume().value;
            const right = this.parseUnary();
            left = { kind: 'APPLY_INTRINSIC', op: op === '*' ? 'mul' : 'div', args: [left, right] };
        }
        return left;
    }

    parseUnary(): any {
        if (this.check('OPERATOR', '!')) {
            this.consume();
            const expr = this.parseUnary();
            return { kind: 'APPLY_INTRINSIC', op: 'not', args: [expr] };
        }
        return this.parsePostfix();
    }

    parsePostfix(): any {
        let left = this.parseAtom();
        while (true) {
            if (this.check('SYMBOL', '[')) {
                this.consume('[');
                const index = this.parseExpression();
                this.consume(']');
                left = { kind: 'APPLY_INTRINSIC', op: 'array_get', args: [left, index] };
            } else if (this.check('SYMBOL', '.')) {
                this.consume('.');
                if (this.check('SYMBOL', '@')) {
                    this.consume('@');
                    const idx = this.consume().value; 
                    left = { kind: 'APPLY_INTRINSIC', op: 'array_get', args: [left, { kind: 'LITERAL', value: parseInt(idx) }] };
                } else {
                     const field = this.consume().value;
                     left = { kind: 'APPLY_INTRINSIC', op: 'object_get', args: [left, { kind: 'LITERAL', value: field }] };
                }
            } else if (this.check('SYMBOL', '(')) {
                if (left.kind !== 'VAR_REF') throw new Error("Cannot call non-identifier expression");
                const targetName = left.payload ? left.payload.name : left.name; 
                this.consume('(');
                const args = [];
                if (!this.check('SYMBOL', ')')) {
                    args.push(this.parseExpression());
                    while (this.check('SYMBOL', ',')) {
                        this.consume(',');
                        args.push(this.parseExpression());
                    }
                }
                this.consume(')');
                left = { kind: 'CALL_BLOCK', target: targetName, args };
            } else {
                break;
            }
        }
        return left;
    }

    parseAtom(): any {
        const token = this.peek();

        if (this.check('LITERAL_INT')) return { kind: 'LITERAL', value: parseInt(this.consume().value) };
        if (this.check('LITERAL_FLOAT')) return { kind: 'LITERAL', value: parseFloat(this.consume().value) };
        if (this.check('LITERAL_STRING')) return { kind: 'LITERAL', value: this.consume().value };
        if (this.check('KEYWORD', 'true')) { this.consume(); return { kind: 'LITERAL', value: true }; }
        if (this.check('KEYWORD', 'false')) { this.consume(); return { kind: 'LITERAL', value: false }; }
        if (this.check('KEYWORD', 'null')) { this.consume(); return { kind: 'LITERAL', value: null }; }
        if (this.check('HLX_LITE_BLOB')) return { kind: 'LITERAL', value: this.consume().value };
        
        if (this.check('SYMBOL', '[')) {
            this.consume('[');
            const items = [];
            if (!this.check('SYMBOL', ']')) {
                items.push(this.parseExpression());
                while (this.check('SYMBOL', ',')) {
                    this.consume(',');
                    items.push(this.parseExpression());
                }
            }
            this.consume(']');
            return { kind: 'LITERAL', value: items }; 
        }

        if (this.check('SYMBOL', '{')) {
            this.consume('{');
            const fields: any[] = [];
            while (!this.check('SYMBOL', '}')) {
                let key;
                if (this.check('LITERAL_STRING')) key = this.consume().value;
                else key = this.consume().value;
                
                this.consume(':');
                const val = this.parseExpression();
                fields.push({ key, value: val });
                if (this.check('SYMBOL', ',')) this.consume(',');
            }
            this.consume('}');
            return { kind: 'APPLY_INTRINSIC', op: 'object_create_generic', args: [ { kind: 'LITERAL', value: fields } ] };
        }

        if (this.check('KEYWORD', 'object')) {
            this.consume('object');
            const contractId = parseInt(this.consume().value);
            this.consume('{');
            const fields: any[] = [];
            while (!this.check('SYMBOL', '}')) {
                this.consume('@');
                const index = parseInt(this.consume().value);
                this.consume(':');
                const val = this.parseExpression();
                fields.push({ index, value: val });
                if (this.check('SYMBOL', ',')) this.consume(',');
            }
            this.consume('}');
            return { kind: 'APPLY_INTRINSIC', op: 'object_construct', args: [ { kind: 'LITERAL', value: contractId }, { kind: 'LITERAL', value: fields } ] };
        }

        if (this.check('SYMBOL', '(')) {
            this.consume('(');
            const expr = this.parseExpression();
            this.consume(')');
            return expr;
        }

        if (this.check('KEYWORD', 'intrinsic')) {
            this.consume('intrinsic');
            const op = this.consume().value;
            this.consume('(');
            const args = [];
            if (!this.check('SYMBOL', ')')) {
                args.push(this.parseExpression());
                while (this.check('SYMBOL', ',')) {
                    this.consume(',');
                    args.push(this.parseExpression());
                }
            }
            this.consume(')');
            return { kind: 'APPLY_INTRINSIC', op, args };
        }

        if (token.value.startsWith('ls.')) {
            const opFull = this.consume().value;
            const op = opFull.split('.')[1];
            
            if (op === 'fingerprint') {
                 const expr = this.parseExpression();
                 return { kind: 'APPLY_INTRINSIC', op: 'ls_fingerprint', args: [expr] };
            }
            
            if (op === 'exists') {
                 this.consume('(');
                 const expr = this.parseExpression();
                 this.consume(')');
                 return { kind: 'APPLY_INTRINSIC', op: 'ls_exists', args: [expr] };
            }
            
            if (op === 'resolve_or') {
                 this.consume('(');
                 const handleExpr = this.parseExpression();
                 this.consume(',');
                 const defaultExpr = this.parseExpression();
                 this.consume(')');
                 return { kind: 'LS_RESOLVE_OR', handle_expr: handleExpr, default_expr: defaultExpr };
            }

            if (op === 'collapse_if') {
                 this.consume('(');
                 const cond = this.parseExpression();
                 this.consume(')');
                 const tag = this.consume().value;
                 const val = this.parseExpression();
                 return { kind: 'LS_COLLAPSE_IF', cond, tag, value_expr: val };
            }

            if (op === 'lazy') {
                const tag = this.consume().value;
                const expr = this.parseExpression();
                return { kind: 'LS_LAZY', tag, thunk_expr: expr };
            }
            if (op === 'force') {
                const handle = this.parseExpression();
                return { kind: 'LS_FORCE', handle_expr: handle };
            }
            if (op === 'alias') {
                const tag = this.consume().value;
                const handle = this.parseExpression();
                return { kind: 'LS_ALIAS', new_tag: tag, handle_expr: handle };
            }
            if (op === 'unalias') {
                const tag = this.consume().value;
                return { kind: 'LS_UNALIAS', tag };
            }
            if (op === 'promote') {
                const tag = this.consume().value;
                const handle = this.parseExpression();
                return { kind: 'LS_PROMOTE', tag, handle_expr: handle };
            }
            if (op === 'watch') {
                const id = this.consume().value;
                const handle = this.parseExpression();
                return { kind: 'LS_WATCH', watcher_id: id, handle_expr: handle };
            }
            if (op === 'unwatch') {
                const id = this.consume().value;
                return { kind: 'LS_UNWATCH', watcher_id: id };
            }
            if (op === 'compose') {
                const tag = this.consume().value;
                this.consume('[');
                const handles = [];
                if (!this.check('SYMBOL', ']')) {
                    handles.push(this.parseExpression());
                    while (this.check('SYMBOL', ',')) {
                        this.consume(',');
                        handles.push(this.parseExpression());
                    }
                }
                this.consume(']');
                return { kind: 'LS_COMPOSE', tag, handle_array: { kind: 'LITERAL', value: handles } };
            }
            if (op === 'decompose') {
                const handle = this.parseExpression();
                return { kind: 'LS_DECOMPOSE', handle_expr: handle };
            }
            if (op === 'project') {
                const handle = this.parseExpression();
                this.consume('[');
                const indices = [];
                if (!this.check('SYMBOL', ']')) {
                    indices.push(parseInt(this.consume().value));
                    while (this.check('SYMBOL', ',')) {
                        this.consume(',');
                        indices.push(parseInt(this.consume().value));
                    }
                }
                this.consume(']');
                return { kind: 'LS_PROJECT', handle_expr: handle, indices };
            }
            if (op === 'table_diff') {
                const t1 = this.consume().value;
                const t2 = this.consume().value;
                return { kind: 'LS_TABLE_DIFF', table_a: t1, table_b: t2 };
            }
            
            let table = this.activeTable || "";
            const nextVal = this.peek().value;
            
            if (this.latentTables.has(nextVal)) {
                 table = this.consume().value; 
            } else if (!this.activeTable) {
                 throw new Error(`E_LS_PIPELINE_NO_ACTIVE_TABLE (2006): Operation '${op}' requires active table or explicit alias.`);
            }
            
            if (op === 'collapse') {
                const tag = this.consume().value;
                const valExpr = this.parseExpression(); 
                return { kind: 'LS_OP', op: 'COLLAPSE', table, tag, val: valExpr };
            } else if (op === 'resolve') {
                const handleExpr = this.parseExpression();
                return { kind: 'LS_OP', op: 'RESOLVE', table, handle: handleExpr };
            } else if (op === 'snapshot') {
                return { kind: 'LS_OP', op: 'SNAPSHOT', table };
            } else if (op === 'batch_collapse') {
                const tag = this.consume().value;
                const valExpr = this.parseExpression();
                return { kind: 'LS_BATCH_OP', op: 'COLLAPSE', table, tag, input: valExpr };
            } else if (op === 'batch_resolve') {
                const handleExpr = this.parseExpression();
                return { kind: 'LS_BATCH_OP', op: 'RESOLVE', table, input: handleExpr };
            }
        }

        if (this.check('IDENT')) {
            return { kind: 'VAR_REF', name: this.consume().value };
        }
        
        if (this.check('KEYWORD', 'if')) {
             return this.parseIfExpression();
        }

        throw new Error(`Unexpected token: ${token.value} (line ${token.line})`);
    }
    
    lower(expr: any): any {
        if (!expr || typeof expr !== 'object') return expr;
        
        if (expr.kind === 'LS_COLLAPSE_IF') {
            return {
                kind: 'IF',
                payload: {
                    cond: this.lower(expr.cond),
                    then_branch: { kind: 'SEQ', body: [{ kind: 'LS_OP', op: 'COLLAPSE', tag: expr.tag, args: [this.lower(expr.value_expr)] }] },
                    else_branch: { kind: 'SEQ', body: [{ kind: 'LITERAL', value: null }] }
                }
            };
        }
        if (expr.kind === 'LS_RESOLVE_OR') {
            return {
                kind: 'IF',
                payload: {
                    cond: { kind: 'APPLY_INTRINSIC', op: 'ls_exists', args: [this.lower(expr.handle_expr)] },
                    then_branch: { kind: 'SEQ', body: [{ kind: 'LS_OP', op: 'RESOLVE', args: [this.lower(expr.handle_expr)] }] },
                    else_branch: { kind: 'SEQ', body: [this.lower(expr.default_expr)] }
                }
            };
        }
        
        if (expr.kind === 'LS_LAZY') {
            return { kind: 'LS_OP', op: 'LAZY_COLLAPSE', tag: expr.tag, args: [this.lower(expr.thunk_expr)] };
        }
        if (expr.kind === 'LS_FORCE') {
            return { kind: 'LS_OP', op: 'FORCE_RESOLVE', args: [this.lower(expr.handle_expr)] };
        }
        if (expr.kind === 'LS_ALIAS') {
            return { kind: 'LS_OP', op: 'ALIAS', args: [{ kind: 'LITERAL', value: expr.new_tag }, this.lower(expr.handle_expr)] };
        }
        if (expr.kind === 'LS_UNALIAS') {
            return { kind: 'LS_OP', op: 'UNALIAS', args: [{ kind: 'LITERAL', value: expr.tag }] };
        }
        if (expr.kind === 'LS_SCOPE') {
            return {
                kind: 'SEQ',
                body: [
                    { kind: 'LS_OP', op: 'SCOPE_BEGIN', args: [{ kind: 'LITERAL', value: expr.scope_name }] },
                    ...expr.body.map((e: any) => this.lower(e)),
                    { kind: 'LS_OP', op: 'SCOPE_END', args: [] }
                ]
            };
        }
        if (expr.kind === 'LS_PROMOTE') {
            return { kind: 'LS_OP', op: 'PROMOTE', args: [{ kind: 'LITERAL', value: expr.tag }, this.lower(expr.handle_expr)] };
        }
        if (expr.kind === 'LS_WATCH') {
            return { kind: 'LS_OP', op: 'WATCH', args: [{ kind: 'LITERAL', value: expr.watcher_id }, this.lower(expr.handle_expr)] };
        }
        if (expr.kind === 'LS_UNWATCH') {
            return { kind: 'LS_OP', op: 'UNWATCH', args: [{ kind: 'LITERAL', value: expr.watcher_id }] };
        }
        if (expr.kind === 'LS_ON_CHANGE') {
            return { kind: 'LS_OP', op: 'ON_CHANGE', args: [{ kind: 'LITERAL', value: expr.watcher_id }, { kind: 'SEQ', body: expr.handler_body.map((e: any) => this.lower(e)) }] };
        }
        if (expr.kind === 'LS_COMPOSE') {
            return { kind: 'LS_OP', op: 'COMPOSE', args: [{ kind: 'LITERAL', value: expr.tag }, this.lower(expr.handle_array)] };
        }
        if (expr.kind === 'LS_DECOMPOSE') {
            return { kind: 'LS_OP', op: 'DECOMPOSE', args: [this.lower(expr.handle_expr)] };
        }
        if (expr.kind === 'LS_PROJECT') {
            return { kind: 'LS_OP', op: 'PROJECT', args: [this.lower(expr.handle_expr), { kind: 'LITERAL', value: expr.indices }] };
        }
        if (expr.kind === 'LS_BATCH_OP') {
             const iterator = '__batch_item';
             const result_acc = '__batch_result';
             const opKind = expr.op === 'COLLAPSE' ? 'COLLAPSE' : 'RESOLVE';
             const args = expr.op === 'COLLAPSE' ? 
                 [{ kind: 'LITERAL', value: expr.tag }, { kind: 'VAR_REF', name: iterator }] : 
                 [{ kind: 'VAR_REF', name: iterator }];
             
             return {
                 kind: 'SEQ',
                 body: [
                     { kind: 'SET_VAR', payload: { name: result_acc, expr: { kind: 'LITERAL', value: [] } } },
                     {
                         kind: 'FOR_EACH', 
                         binding: iterator,
                         iterable: this.lower(expr.input),
                         body: {
                             kind: 'APPLY_INTRINSIC',
                             op: 'array_push',
                             args: [
                                 { kind: 'VAR_REF', name: result_acc },
                                 { kind: 'LS_OP', op: opKind, args }
                             ]
                         }
                     },
                     { kind: 'VAR_REF', name: result_acc }
                 ]
             };
        }

        const newExpr: any = Array.isArray(expr) ? [] : {};
        for (const k in expr) {
            newExpr[k] = this.lower(expr[k]);
        }
        return newExpr;
    }
}

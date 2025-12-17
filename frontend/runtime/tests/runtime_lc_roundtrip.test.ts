
import { HLXRuntime } from '../HLXRuntime';

// Test globals declarations
declare var describe: any;
declare var test: any;
declare var expect: any;
declare var beforeEach: any;

describe('HLXRuntime LC Roundtrip & Invariants', () => {
  let runtime: HLXRuntime;

  beforeEach(() => {
    runtime = new HLXRuntime();
  });

  test('Primitives Roundtrip (Encode -> Decode)', () => {
    const primitives = [
      null,
      true,
      false,
      12345,
      3.14159,
      "Hello World",
      "String with \"quotes\""
    ];

    primitives.forEach(val => {
      const encoded = runtime.encodeLC(val);
      const decoded = runtime.decodeLC(encoded);
      expect(decoded).toEqual(val);
    });
  });

  test('Complex Object Roundtrip', () => {
    // Structure: { 14: { @0: 100, @1: "test" } }
    const obj = { "14": { "@0": 100, "@1": "test" } };
    
    const encoded = runtime.encodeLC(obj);
    const decoded = runtime.decodeLC(encoded);
    
    expect(decoded).toEqual(obj);
  });

  test('Array Roundtrip', () => {
    const arr = [1, 2, "three", true];
    const encoded = runtime.encodeLC(arr);
    const decoded = runtime.decodeLC(encoded);
    
    expect(decoded).toEqual(arr);
  });

  test('Invariant: collapse(resolve(h)) == h', () => {
    const val = { "14": { "@0": "invariant" } };
    const h1 = runtime.collapse(val, 'inv');
    const resolved = runtime.resolve(h1);
    const h2 = runtime.collapse(resolved, 'inv');
    
    expect(h1).toBe(h2);
  });

  test('Invariant: Idempotence', () => {
    const val = { "test": "idempotence" };
    const h1 = runtime.collapse(val, 'idem');
    const h2 = runtime.collapse(val, 'idem');
    
    expect(h1).toBe(h2);
    expect(runtime.snapshot().handle_count).toBe(1);
  });
  
  test('LC Stream Structure', () => {
    const val = 123;
    const stream = runtime.encodeLC(val);
    // Integer 123 is CID 2. format: 🜊2🜁0123🜂
    expect(stream).toContain('🜊2');
    expect(stream).toContain('123');
    expect(stream).toContain('🜂');
  });
});

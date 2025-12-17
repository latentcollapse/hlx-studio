
import { HLXRuntime } from '../HLXRuntime';

// Test globals declarations
declare var describe: any;
declare var test: any;
declare var expect: any;
declare var beforeEach: any;

describe('HLXRuntime v1.0', () => {
  let runtime: HLXRuntime;

  beforeEach(() => {
    runtime = new HLXRuntime();
  });

  test('Determinism: collapse() should return same handle for same value', () => {
    const val1 = { "14": { "@0": 123 } };
    const val2 = { "14": { "@0": 123 } };

    const h1 = runtime.collapse(val1, 'test');
    const h2 = runtime.collapse(val2, 'test');

    expect(h1).toBe(h2);
  });

  test('Reversibility: resolve(collapse(v)) == v', () => {
    const val = { "hello": "world" };
    const h = runtime.collapse(val, 'rev');
    const resolved = runtime.resolve(h);

    expect(resolved).toEqual(val);
  });

  test('LC Encoding: encodeLC() should produce stream string', () => {
    const val = { "14": { "@0": 123 } };
    const stream = runtime.encodeLC(val);
    expect(stream).toContain('🜊');
    expect(stream).toContain('123');
  });

  test('Snapshot: should report accurate counts', () => {
    runtime.collapse({ a: 1 }, 's1');
    runtime.collapse({ b: 2 }, 's2');
    
    const snap = runtime.snapshot();
    expect(snap.handle_count).toBe(2);
    expect(snap.handles.length).toBe(2);
  });
});

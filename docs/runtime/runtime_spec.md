# HLX Runtime Specification: Reference Implementation
**Version:** 1.0 (Optional / External)
**Status:** REFERENCE_IMPLEMENTATION

## 1. Introduction
This document defines the execution semantics for the HLX language family. While the HLX Bootstrap Capsule defines *syntax* and *structure*, this specification defines *behavior*.

## 2. The HLX Reference Runtime Model
The Reference Runtime is a standardized architecture. Implementations may vary, but observable behavior must match this state machine.

**DISCLAIMER:** The Reference Runtime is NOT part of the HLX language definition. It is one possible implementation of a runtime environment capable of executing HLX-Lite bytecode.

### States
* **IDLE**: Engine is ready. No active context.
* **EXECUTING**: Processing a program block. Handles are mutable in local scope.
* **VALIDATING**: Checking constraints (Contract schemas, Invariants).
* **COMMITTED**: Transaction successful. State persisted to CAS.
* **ROLLED_BACK**: Transaction failed. State reverted.
* **FAULT**: Unrecoverable runtime error.

## 3. Operator Semantics

### `ls.collapse` (⚳)
* **Signature**: `collapse(table_id: String, tag: String, value: HLXLite) -> Handle`
* **Behavior**:
  1. Canonicalize `value`.
  2. Compute Hash `H = BLAKE3(value)`.
  3. Store `(H, value)` in Content-Addressable Storage (CAS).
  4. Register `Handle(tag, H)` in `table_id`.
* **Side Effects**: CAS Write, Table Update.
* **Errors**: `E_RUNTIME_CAS_WRITE_FAIL`.

### `ls.resolve` (⚯)
* **Signature**: `resolve(table_id: String, handle: Handle) -> HLXLite`
* **Behavior**:
  1. Lookup `handle` in `table_id` to get Hash `H`.
  2. Retrieve `value` from CAS using `H`.
* **Side Effects**: CAS Read.
* **Errors**: `E_RUNTIME_HANDLE_NOT_FOUND`, `E_RUNTIME_CAS_MISSING_BLOB`.

### `ls.snapshot` (⚶)
* **Signature**: `snapshot(table_id: String) -> Handle`
* **Behavior**:
  1. Serialize current state of `table_id`.
  2. `ls.collapse` the serialized state.
* **Output**: A handle pointing to the table state.

### `ls.transaction` (⚿)
* **Signature**: `transaction(block: Closure) -> Result`
* **Behavior**:
  1. Fork current table state.
  2. Execute `block`.
  3. If successful, MERGE changes to parent.
  4. If failure/panic, DISCARD changes.

### Pipe Operator (▷ / |>)
* **Behavior**: Syntactic sugar. `A |> B` lowers to `B(A)`.
* **Runtime**: Handled at compilation/lowering time. No runtime opcode.

## 4. Contract Semantic Binding
HLX-Lite Contracts 1-5 are structural. Contracts > 5 have external semantics.

* **Registry**: The runtime maintains a map `Map<ContractID, SchemaValidator>`.
* **Validation**: Occurs implicitly on `ls.collapse` or explicitly via `ls.validate`.
* **Unknown Contracts**: By default, treated as valid structural objects. Runtimes MAY configure "Strict Mode" to reject unknown IDs.

## 5. Runtime Error Taxonomy
These errors occur during execution, distinct from parse/syntax errors.

* `0xE001`: **E_RUNTIME_SCHEMA_VIOLATION** - Data does not match User Contract definition.
* `0xE002`: **E_RUNTIME_SIDE_EFFECT_FORBIDDEN** - Operation attempted side effect in pure context.
* `0xE003`: **E_RUNTIME_TRANSACTION_ABORT** - Explicit abort or constraint failure.
* `0xE004`: **E_RUNTIME_CAS_FAILURE** - Storage subsystem error.
* `0xE005`: **E_RUNTIME_CYCLE_DETECTED** - Recursive resolution loop.

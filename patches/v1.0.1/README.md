# HLX Patch v1.0.1: Patch Delivery Scaffolding

**Status:** TRANSPORT ONLY
**Requires:** External Tooling (No Runtime Execution)

## Purpose
This patch establishes the canonical method for delivering incremental updates via HLX-LS handles. It defines the `PatchManifest` (Contract 200) and `PatchOperation` (Contract 201) structures.

## Contents
* `hlx_v101_patch.hlx`: Runic source code defining the patch logic.
* `hlx_v101_patch.hlxl`: ASCII source code (bijective equivalent).
* `lc12_manifest.json`: Transport envelope.
* `handles/`: Folder containing the LC payloads for the specific files modified/added in this patch.

## Usage
1. Load `hlx_v101_patch.hlx` into context.
2. Verify structural validity.
3. External tooling parses the `PatchManifest` at `&h_patch_manifest_0`.
4. Tooling executes the operations defined in the manifest.

## Structural Contracts (External Semantics)
This patch uses contracts 200 and 201. These are structurally valid in HLX v1.0.0 but have no defined runtime behavior inside the HLX Engine. Their semantics are defined solely for external patch-applicator tools.

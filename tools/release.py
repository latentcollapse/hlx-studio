#!/usr/bin/env python3
"""
HLX RELEASE BUNDLER v1.1.0
==========================
Creates untruncated .zip bundles for release.

Bundles:
1. HLX_v1.1.0_COMPLETE.zip
2. HLX_v1.1.0_CHAPTERS_ONLY.zip
3. HLX_v1.1.0_TOOLS_ONLY.zip

Author: Matt (latentcollapse)
"""

import zipfile
import sys
import os
from pathlib import Path

def create_release_bundles():
    print("=" * 60)
    print("HLX RELEASE BUNDLER v1.1.0")
    print("=" * 60)

    # Define file lists
    common_files = [
        'corpus/README_GITHUB.md',
        'corpus/USAGE.md'
    ]
    
    chapter_files = [
        'corpus/HLX_CHAPTER_CORE_v1.0.0.json',
        'corpus/HLX_CHAPTER_RUNTIME_v1.0.0.json',
        'corpus/HLX_CHAPTER_EXTENSIONS_v1.0.0.json',
        'corpus/HLX_MANIFEST_v1.0.0.json',
        'corpus/HLX_WATERMARK_v1.0.0.json'
    ]
    
    tool_files = [
        'tools/verify_full.py',
        'tools/ingest.py',
        'tools/chapter_verify.py',
        'tools/verify_watermark.py'
    ]

    # create output directory if it doesn't exist (e.g. 'release')
    # For now, we output to root as per plan implied
    
    # 1. COMPLETE BUNDLE
    bundle_name = 'HLX_v1.1.0_COMPLETE.zip'
    print(f"[*] Creating {bundle_name}...")
    with zipfile.ZipFile(bundle_name, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        for f in common_files + chapter_files + tool_files:
            if os.path.exists(f):
                z.write(f)
            else:
                print(f"  [!] Warning: Missing file {f}")

    # 2. CHAPTERS ONLY
    bundle_name = 'HLX_v1.1.0_CHAPTERS_ONLY.zip'
    print(f"[*] Creating {bundle_name}...")
    with zipfile.ZipFile(bundle_name, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        for f in chapter_files + ['corpus/README_GITHUB.md']:
            if os.path.exists(f):
                z.write(f)

    # 3. TOOLS ONLY
    bundle_name = 'HLX_v1.1.0_TOOLS_ONLY.zip'
    print(f"[*] Creating {bundle_name}...")
    with zipfile.ZipFile(bundle_name, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        for f in tool_files + ['corpus/USAGE.md']:
            if os.path.exists(f):
                z.write(f)

    print("\n[✓] Release bundles created successfully.")

if __name__ == "__main__":
    create_release_bundles()

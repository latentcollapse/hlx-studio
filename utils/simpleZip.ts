
// Minimal ZIP implementation (Store only, no compression)
// Conforms to PKWARE APPNOTE.TXT

const CRC_TABLE = new Int32Array(256);
for (let i = 0; i < 256; i++) {
  let c = i;
  for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
  CRC_TABLE[i] = c;
}

function crc32(data: Uint8Array): number {
  let crc = -1;
  for (let i = 0; i < data.length; i++) {
    crc = (crc >>> 8) ^ CRC_TABLE[(crc ^ data[i]) & 0xff];
  }
  return (crc ^ -1) >>> 0;
}

export class SimpleZip {
  private files: { name: string; data: Uint8Array; crc: number; }[] = [];

  addFile(name: string, content: string) {
    const data = new TextEncoder().encode(content);
    this.files.push({
      name,
      data,
      crc: crc32(data)
    });
  }

  generate(): Blob {
    const parts: Uint8Array[] = [];
    let offset = 0;
    const centralDir: Uint8Array[] = [];

    for (const file of this.files) {
      const nameBytes = new TextEncoder().encode(file.name);
      const header = new Uint8Array(30 + nameBytes.length);
      const view = new DataView(header.buffer);

      // Local File Header
      view.setUint32(0, 0x04034b50, true); // Signature
      view.setUint16(4, 0x000a, true);     // Version needed
      view.setUint16(6, 0x0800, true);     // Flags (UTF-8)
      view.setUint16(8, 0x0000, true);     // Compression (Store)
      view.setUint16(10, 0x0000, true);    // Time (Zeroed for determinism)
      view.setUint16(12, 0x0000, true);    // Date
      view.setUint32(14, file.crc, true);  // CRC-32
      view.setUint32(18, file.data.length, true); // Compressed Size
      view.setUint32(22, file.data.length, true); // Uncompressed Size
      view.setUint16(26, nameBytes.length, true); // Filename Length
      view.setUint16(28, 0x0000, true);    // Extra Field Length

      header.set(nameBytes, 30);
      
      parts.push(header);
      parts.push(file.data);

      // Central Directory Record for this file
      const cDir = new Uint8Array(46 + nameBytes.length);
      const cView = new DataView(cDir.buffer);

      cView.setUint32(0, 0x02014b50, true); // Signature
      cView.setUint16(4, 0x000a, true);     // Version made by
      cView.setUint16(6, 0x000a, true);     // Version needed
      cView.setUint16(8, 0x0800, true);     // Flags (UTF-8)
      cView.setUint16(10, 0x0000, true);    // Compression
      cView.setUint16(12, 0x0000, true);    // Time
      cView.setUint16(14, 0x0000, true);    // Date
      cView.setUint32(16, file.crc, true);  // CRC
      cView.setUint32(20, file.data.length, true); // Comp Size
      cView.setUint32(24, file.data.length, true); // Uncomp Size
      cView.setUint16(28, nameBytes.length, true); // Filename Len
      cView.setUint16(30, 0, true);         // Extra Field Len
      cView.setUint16(32, 0, true);         // Comment Len
      cView.setUint16(34, 0, true);         // Disk Start
      cView.setUint16(36, 0, true);         // Internal Attrs
      cView.setUint32(38, 0, true);         // External Attrs
      cView.setUint32(42, offset, true);    // Local Header Offset

      cDir.set(nameBytes, 46);
      centralDir.push(cDir);

      offset += header.length + file.data.length;
    }

    const cDirStart = offset;
    let cDirSize = 0;
    for (const cd of centralDir) {
      parts.push(cd);
      cDirSize += cd.length;
    }

    // End of Central Directory Record
    const eocd = new Uint8Array(22);
    const eView = new DataView(eocd.buffer);
    eView.setUint32(0, 0x06054b50, true);   // Signature
    eView.setUint16(4, 0, true);            // Disk Number
    eView.setUint16(6, 0, true);            // Disk w/ CD
    eView.setUint16(8, this.files.length, true); // Entries on Disk
    eView.setUint16(10, this.files.length, true); // Total Entries
    eView.setUint32(12, cDirSize, true);    // CD Size
    eView.setUint32(16, cDirStart, true);   // CD Offset
    eView.setUint16(20, 0, true);           // Comment Len

    parts.push(eocd);

    return new Blob(parts as BlobPart[], { type: 'application/zip' });
  }
}

# LC-T and LC-B Format Specification

**Version**: 1.0.0
**Date**: 2025-12-18
**Author**: HLXL Brain Training System

---

## Overview

This document specifies two additional formats in the HLX family for representing Latent Collapse data:

| Format | Full Name | Description | Use Case |
|--------|-----------|-------------|----------|
| HLXL | HLX Language | Human-readable syntax | Source code, configuration |
| LC-R | Latent Collapse Runic | Unicode glyph notation | Visual representation, compact storage |
| LC-T | Latent Collapse Text | ASCII-safe text format | Cross-platform compatibility, logging |
| LC-B | Latent Collapse Binary | Hex/binary encoding | Wire protocols, binary storage |

---

## LC-R Reference (Existing)

LC-R uses Unicode glyphs for maximum visual density:

| Glyph | Meaning | Unicode |
|-------|---------|---------|
| `null` | null | U+2205 |
| `true` | true | U+22A4 |
| `false` | false | U+22A5 |
| `bytes prefix` | bytes prefix | U+22A0 |
| `handle` | handle reference | U+27C1 |
| `contract start` | contract start | U+1F70A |
| `contract end` | contract end | U+1F702 |
| `field separator` | field index marker | U+1F701 |
| `array start` | array start | U+1F703 |
| `array end` | array end | U+1F704 |
| `object start` | object start | U+25C7 |
| `object end` | object end | U+25C6 |

---

## LC-T (Latent Collapse Text) Specification

### Design Principles

1. **ASCII-only**: No Unicode characters required
2. **Human-readable**: Clear delimiters with semantic meaning
3. **Parseable**: Unambiguous grammar for machine parsing
4. **Reversible**: Lossless conversion to/from LC-R

### Glyph-to-Text Mapping

| LC-R | LC-T | Description |
|------|------|-------------|
| `null` | `NULL` | Null value |
| `true` | `TRUE` | Boolean true |
| `false` | `FALSE` | Boolean false |
| `bytes` | `#` | Bytes prefix (followed by hex) |
| `handle` | `@` | Handle reference |
| `contract start` | `{C:` | Contract start with ID |
| `contract end` | `}` | Contract end |
| `field sep` | `,` | Field separator with index |
| `array start` | `[` | Array start |
| `array end` | `]` | Array end |
| `object start` | `{` | Object start |
| `object end` | `}` | Object end |

### LC-T Grammar

```
lct_value     := primitive | contract | array | object
primitive     := null | bool | number | string | bytes | handle

null          := "NULL"
bool          := "TRUE" | "FALSE"
number        := integer | float
integer       := ["-"] digit+
float         := ["-"] digit+ "." digit+ ["e" ["-"] digit+]
string        := '"' char* '"'
bytes         := "#" hex_char*
handle        := "@" identifier

contract      := "{C:" contract_id fields "}"
contract_id   := integer
fields        := field ("," field)*
field         := field_index "=" lct_value
field_index   := integer

array         := "[" [lct_value ("," lct_value)*] "]"
object        := "{" [pair ("," pair)*] "}"
pair          := identifier ":" lct_value
identifier    := alpha (alpha | digit | "_")*
```

### LC-T Examples

#### Primitives

| HLXL | LC-R | LC-T |
|------|------|------|
| `null` | `null` | `NULL` |
| `true` | `true` | `TRUE` |
| `false` | `false` | `FALSE` |
| `42` | `42` | `42` |
| `3.14` | `3.14` | `3.14` |
| `"hello"` | `"hello"` | `"hello"` |
| `b"data"` | `bytes64617461` | `#64617461` |
| `&h_ast` | `handle_ast` | `@ast` |

#### Contracts

| HLXL | LC-R | LC-T |
|------|------|------|
| `{14: {@0: 42}}` | `contract_start14field_sep0 42contract_end` | `{C:14,0=42}` |
| `{16: {@0: "hello"}}` | `contract_start16field_sep0 "hello"contract_end` | `{C:16,0="hello"}` |
| `{1000: {@0: "search", @1: @query}}` | `contract_start1000field_sep0 "search"field_sep1 handle_querycontract_end` | `{C:1000,0="search",1=@query}` |

#### Arrays

| HLXL | LC-R | LC-T |
|------|------|------|
| `[]` | `array_startarray_end` | `[]` |
| `[1, 2, 3]` | `array_start1, 2, 3array_end` | `[1,2,3]` |
| `["a", "b"]` | `array_start"a", "b"array_end` | `["a","b"]` |
| `[&h_a, &h_b]` | `array_starthandle_a, handle_barray_end` | `[@a,@b]` |

#### Objects

| HLXL | LC-R | LC-T |
|------|------|------|
| `{x: 10}` | `object_start x: 10 object_end` | `{x:10}` |
| `{name: "Alice", age: 30}` | `object_start name: "Alice", age: 30 object_end` | `{name:"Alice",age:30}` |

#### Complex Examples

```
English: Search for documents
HLXL: {1000: {@0: "search", @1: &h_documents}}
LC-R: contract_start1000field_sep0 "search"field_sep1 handle_documentscontract_end
LC-T: {C:1000,0="search",1=@documents}
```

```
English: Filter active users
HLXL: {1000: {@0: "filter", @1: &h_users, @2: &h_active}}
LC-R: contract_start1000field_sep0 "filter"field_sep1 handle_usersfield_sep2 handle_activecontract_end
LC-T: {C:1000,0="filter",1=@users,2=@active}
```

---

## LC-B (Latent Collapse Binary) Specification

### Design Principles

1. **Compact**: Minimize byte count
2. **Efficient**: Fast parsing and serialization
3. **Type-tagged**: Self-describing format
4. **Aligned**: Word-aligned for performance (optional)

### Type Tags (1 byte)

| Tag | Hex | Type | Description |
|-----|-----|------|-------------|
| 0x00 | `00` | NULL | Null value |
| 0x01 | `01` | TRUE | Boolean true |
| 0x02 | `02` | FALSE | Boolean false |
| 0x10 | `10` | INT8 | 8-bit signed integer |
| 0x11 | `11` | INT16 | 16-bit signed integer |
| 0x12 | `12` | INT32 | 32-bit signed integer |
| 0x13 | `13` | INT64 | 64-bit signed integer |
| 0x14 | `14` | UINT8 | 8-bit unsigned integer |
| 0x15 | `15` | UINT16 | 16-bit unsigned integer |
| 0x16 | `16` | UINT32 | 32-bit unsigned integer |
| 0x17 | `17` | UINT64 | 64-bit unsigned integer |
| 0x20 | `20` | F32 | 32-bit float |
| 0x21 | `21` | F64 | 64-bit float |
| 0x30 | `30` | STR | String (length-prefixed) |
| 0x31 | `31` | BYTES | Bytes (length-prefixed) |
| 0x40 | `40` | HANDLE | Handle reference |
| 0x50 | `50` | CONTRACT | Contract structure |
| 0x60 | `60` | ARRAY | Array (count-prefixed) |
| 0x70 | `70` | OBJECT | Object (count-prefixed) |

### Encoding Rules

#### Primitives

```
NULL:    00
TRUE:    01
FALSE:   02
INT8:    10 <byte>
INT16:   11 <2 bytes little-endian>
INT32:   12 <4 bytes little-endian>
INT64:   13 <8 bytes little-endian>
F32:     20 <4 bytes IEEE 754>
F64:     21 <8 bytes IEEE 754>
STRING:  30 <length:u16> <utf8 bytes>
BYTES:   31 <length:u16> <raw bytes>
HANDLE:  40 <length:u8> <ascii tag>
```

#### Structures

```
CONTRACT: 50 <contract_id:u16> <field_count:u8> <fields...>
  field:  <field_index:u8> <value>

ARRAY:    60 <count:u16> <elements...>
  element: <value>

OBJECT:   70 <count:u8> <pairs...>
  pair:   <key_length:u8> <key> <value>
```

### LC-B Text Representation

For human readability in documentation and logs, LC-B uses hex notation with type prefixes:

```
<TYPE>:<hex_data>
```

Examples:
- `NULL:00`
- `TRUE:01`
- `FALSE:02`
- `INT:12:2a000000` (42 as INT32)
- `STR:30:0005:68656c6c6f` ("hello")
- `HDL:40:03:617374` (@ast)
- `CON:50:03e8:02:00:STR:30:0006:736561726368:01:HDL:40:05:7175657279` (contract 1000, "search", @query)

### LC-B Simplified Notation

For training data, we use a simplified hex representation:

```
[<contract_id>|<field_idx>:<value>|<field_idx>:<value>|...]
```

Where values are encoded as:
- Integers: decimal or hex with `0x` prefix
- Strings: quoted
- Handles: `&` prefix
- Arrays: `[]` with comma separation
- Null: `_`
- True: `T`
- False: `F`

### LC-B Examples

#### Primitives

| HLXL | LC-R | LC-T | LC-B |
|------|------|------|------|
| `null` | `null` | `NULL` | `[_]` |
| `true` | `true` | `TRUE` | `[T]` |
| `false` | `false` | `FALSE` | `[F]` |
| `42` | `42` | `42` | `[0x2a]` |
| `"hello"` | `"hello"` | `"hello"` | `["hello"]` |
| `&h_ast` | `handle_ast` | `@ast` | `[&ast]` |

#### Contracts

| HLXL | LC-R | LC-T | LC-B |
|------|------|------|------|
| `{14: {@0: 42}}` | `contract_start14field_sep0 42contract_end` | `{C:14,0=42}` | `[14\|0:0x2a]` |
| `{16: {@0: "hello"}}` | `contract_start16field_sep0 "hello"contract_end` | `{C:16,0="hello"}` | `[16\|0:"hello"]` |
| `{1000: {@0: "search", @1: @query}}` | `contract_start1000field_sep0 "search"field_sep1 handle_querycontract_end` | `{C:1000,0="search",1=@query}` | `[1000\|0:"search"\|1:&query]` |

#### Arrays

| HLXL | LC-R | LC-T | LC-B |
|------|------|------|------|
| `[]` | `array_startarray_end` | `[]` | `[[]]` |
| `[1, 2, 3]` | `array_start1, 2, 3array_end` | `[1,2,3]` | `[[0x01,0x02,0x03]]` |
| `[&h_a, &h_b]` | `array_starthandle_a, handle_barray_end` | `[@a,@b]` | `[[&a,&b]]` |

#### Objects

| HLXL | LC-R | LC-T | LC-B |
|------|------|------|------|
| `{x: 10}` | `object_start x: 10 object_end` | `{x:10}` | `[{x:0x0a}]` |
| `{name: "Alice"}` | `object_start name: "Alice" object_end` | `{name:"Alice"}` | `[{name:"Alice"}]` |

---

## Conversion Rules

### LC-R to LC-T

```
null -> NULL
true -> TRUE
false -> FALSE
bytesXXXX -> #XXXX
handle_X -> @X
contract_startN -> {C:N
field_sepN -> ,N=
contract_end -> }
array_start -> [
array_end -> ]
object_start -> {
object_end -> }
```

### LC-T to LC-B

```
NULL -> [_]
TRUE -> [T]
FALSE -> [F]
number -> [0xHEX] or [decimal]
"string" -> ["string"]
@handle -> [&handle]
{C:N,...} -> [N|fields...]
[items] -> [[items]]
{k:v,...} -> [{k:v,...}]
```

### LC-B to Wire Format (Full Binary)

For actual binary transmission, use the byte-level encoding defined in the Type Tags section.

---

## Format Selection Guidelines

| Use Case | Recommended Format |
|----------|-------------------|
| Source files, config | HLXL |
| Visual debugging, compact display | LC-R |
| Logs, cross-platform text | LC-T |
| Network protocols, storage | LC-B |
| Human editing | HLXL or LC-T |
| Machine processing | LC-B or LC-R |

---

## Implementation Notes

### Tokenizer Requirements

The tokenizer must support:
1. All LC-R glyphs as single tokens
2. LC-T delimiters: `{C:`, `}`, `[`, `]`, `@`, `#`, `NULL`, `TRUE`, `FALSE`
3. LC-B markers: `[`, `]`, `|`, `:`, `&`, `_`, `T`, `F`, `0x`

### Corpus Format

Training examples should include all four formats:

```
English: <natural language description>
HLXL: <hlxl syntax>
LC-R: <runic glyph notation>
LC-T: <text-safe notation>
LC-B: <binary/hex notation>
```

### Validation

Valid LC-T must:
- Parse without errors
- Convert losslessly to LC-R
- Contain only ASCII characters

Valid LC-B must:
- Parse without errors
- Convert losslessly to LC-T and LC-R
- Use correct type tags
- Have matching bracket/brace counts

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-18 | Initial specification |

---

**End of Specification**

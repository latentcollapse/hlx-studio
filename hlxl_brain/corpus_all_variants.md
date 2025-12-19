# HLX Family Comprehensive Corpus
# All Four Formats: HLXL, LC-R, LC-T, LC-B

**Version**: 1.0.0
**Date**: 2025-12-18
**Total Examples**: 150+
**Formats**: HLXL (human-readable), LC-R (runic glyphs), LC-T (text-safe), LC-B (binary/hex)

---

## SECTION 1: PRIMITIVES (20 examples)

### Null Values

English: Represent nothing
HLXL: null
LC-R: ∅
LC-T: NULL
LC-B: [_]

English: Empty value
HLXL: null
LC-R: ∅
LC-T: NULL
LC-B: [_]

### Boolean Values

English: Represent true
HLXL: true
LC-R: ⊤
LC-T: TRUE
LC-B: [T]

English: Represent false
HLXL: false
LC-R: ⊥
LC-T: FALSE
LC-B: [F]

English: Enable flag
HLXL: true
LC-R: ⊤
LC-T: TRUE
LC-B: [T]

English: Disable flag
HLXL: false
LC-R: ⊥
LC-T: FALSE
LC-B: [F]

### Integer Values

English: Number zero
HLXL: 0
LC-R: 0
LC-T: 0
LC-B: [0x00]

English: Number one
HLXL: 1
LC-R: 1
LC-T: 1
LC-B: [0x01]

English: Number forty-two
HLXL: 42
LC-R: 42
LC-T: 42
LC-B: [0x2a]

English: Negative number
HLXL: -100
LC-R: -100
LC-T: -100
LC-B: [0xff9c]

English: Large number
HLXL: 1000
LC-R: 1000
LC-T: 1000
LC-B: [0x03e8]

### Float Values

English: Pi constant
HLXL: 3.14159
LC-R: 3.14159
LC-T: 3.14159
LC-B: [3.14159]

English: Decimal half
HLXL: 0.5
LC-R: 0.5
LC-T: 0.5
LC-B: [0.5]

### String Values

English: Greeting message
HLXL: "hello"
LC-R: "hello"
LC-T: "hello"
LC-B: ["hello"]

English: User name Alice
HLXL: "Alice"
LC-R: "Alice"
LC-T: "Alice"
LC-B: ["Alice"]

English: File path
HLXL: "/home/user/data.txt"
LC-R: "/home/user/data.txt"
LC-T: "/home/user/data.txt"
LC-B: ["/home/user/data.txt"]

### Handle References

English: Reference to AST
HLXL: &h_ast
LC-R: ⟁ast
LC-T: @ast
LC-B: [&ast]

English: Reference to documents
HLXL: &h_documents
LC-R: ⟁documents
LC-T: @documents
LC-B: [&documents]

English: Reference to model
HLXL: &h_model
LC-R: ⟁model
LC-T: @model
LC-B: [&model]

English: Reference to query
HLXL: &h_query
LC-R: ⟁query
LC-T: @query
LC-B: [&query]

---

## SECTION 2: BASIC OPERATIONS (30 examples)

### Search Operations

English: Search for documents
HLXL: {1000: {@0: "search", @1: &h_documents}}
LC-R: 🜊1000🜁0 "search"🜁1 ⟁documents🜂
LC-T: {C:1000,0="search",1=@documents}
LC-B: [1000|0:"search"|1:&documents]

English: Search files for pattern
HLXL: {1000: {@0: "search", @1: &h_files, @2: "pattern"}}
LC-R: 🜊1000🜁0 "search"🜁1 ⟁files🜁2 "pattern"🜂
LC-T: {C:1000,0="search",1=@files,2="pattern"}
LC-B: [1000|0:"search"|1:&files|2:"pattern"]

English: Search database for users
HLXL: {1000: {@0: "search", @1: &h_database, @2: "users"}}
LC-R: 🜊1000🜁0 "search"🜁1 ⟁database🜁2 "users"🜂
LC-T: {C:1000,0="search",1=@database,2="users"}
LC-B: [1000|0:"search"|1:&database|2:"users"]

English: Find error in logs
HLXL: {1000: {@0: "search", @1: &h_logs, @2: "error"}}
LC-R: 🜊1000🜁0 "search"🜁1 ⟁logs🜁2 "error"🜂
LC-T: {C:1000,0="search",1=@logs,2="error"}
LC-B: [1000|0:"search"|1:&logs|2:"error"]

English: Query the cache
HLXL: {1000: {@0: "search", @1: &h_cache}}
LC-R: 🜊1000🜁0 "search"🜁1 ⟁cache🜂
LC-T: {C:1000,0="search",1=@cache}
LC-B: [1000|0:"search"|1:&cache]

### Filter Operations

English: Filter active users
HLXL: {1000: {@0: "filter", @1: &h_users, @2: &h_active}}
LC-R: 🜊1000🜁0 "filter"🜁1 ⟁users🜁2 ⟁active🜂
LC-T: {C:1000,0="filter",1=@users,2=@active}
LC-B: [1000|0:"filter"|1:&users|2:&active]

English: Filter items where valid
HLXL: {1000: {@0: "filter", @1: &h_items, @2: &h_valid}}
LC-R: 🜊1000🜁0 "filter"🜁1 ⟁items🜁2 ⟁valid🜂
LC-T: {C:1000,0="filter",1=@items,2=@valid}
LC-B: [1000|0:"filter"|1:&items|2:&valid]

English: Filter records by status
HLXL: {1000: {@0: "filter", @1: &h_records, @2: &h_status}}
LC-R: 🜊1000🜁0 "filter"🜁1 ⟁records🜁2 ⟁status🜂
LC-T: {C:1000,0="filter",1=@records,2=@status}
LC-B: [1000|0:"filter"|1:&records|2:&status]

English: Keep only recent documents
HLXL: {1000: {@0: "filter", @1: &h_documents, @2: &h_recent}}
LC-R: 🜊1000🜁0 "filter"🜁1 ⟁documents🜁2 ⟁recent🜂
LC-T: {C:1000,0="filter",1=@documents,2=@recent}
LC-B: [1000|0:"filter"|1:&documents|2:&recent]

English: Select enabled features
HLXL: {1000: {@0: "filter", @1: &h_features, @2: &h_enabled}}
LC-R: 🜊1000🜁0 "filter"🜁1 ⟁features🜁2 ⟁enabled🜂
LC-T: {C:1000,0="filter",1=@features,2=@enabled}
LC-B: [1000|0:"filter"|1:&features|2:&enabled]

### Transform Operations

English: Transform text to uppercase
HLXL: {1000: {@0: "transform", @1: &h_text, @2: &h_uppercase}}
LC-R: 🜊1000🜁0 "transform"🜁1 ⟁text🜁2 ⟁uppercase🜂
LC-T: {C:1000,0="transform",1=@text,2=@uppercase}
LC-B: [1000|0:"transform"|1:&text|2:&uppercase]

English: Convert data to JSON
HLXL: {1000: {@0: "transform", @1: &h_data, @2: &h_json}}
LC-R: 🜊1000🜁0 "transform"🜁1 ⟁data🜁2 ⟁json🜂
LC-T: {C:1000,0="transform",1=@data,2=@json}
LC-B: [1000|0:"transform"|1:&data|2:&json]

English: Normalize the input
HLXL: {1000: {@0: "transform", @1: &h_input, @2: &h_normalize}}
LC-R: 🜊1000🜁0 "transform"🜁1 ⟁input🜁2 ⟁normalize🜂
LC-T: {C:1000,0="transform",1=@input,2=@normalize}
LC-B: [1000|0:"transform"|1:&input|2:&normalize]

English: Encode value as base64
HLXL: {1000: {@0: "transform", @1: &h_value, @2: &h_base64}}
LC-R: 🜊1000🜁0 "transform"🜁1 ⟁value🜁2 ⟁base64🜂
LC-T: {C:1000,0="transform",1=@value,2=@base64}
LC-B: [1000|0:"transform"|1:&value|2:&base64]

English: Parse string as integer
HLXL: {1000: {@0: "transform", @1: &h_string, @2: &h_parseInt}}
LC-R: 🜊1000🜁0 "transform"🜁1 ⟁string🜁2 ⟁parseInt🜂
LC-T: {C:1000,0="transform",1=@string,2=@parseInt}
LC-B: [1000|0:"transform"|1:&string|2:&parseInt]

### Aggregate Operations

English: Calculate sum of values
HLXL: {1000: {@0: "aggregate", @1: &h_sum, @2: &h_values}}
LC-R: 🜊1000🜁0 "aggregate"🜁1 ⟁sum🜁2 ⟁values🜂
LC-T: {C:1000,0="aggregate",1=@sum,2=@values}
LC-B: [1000|0:"aggregate"|1:&sum|2:&values]

English: Get average of scores
HLXL: {1000: {@0: "aggregate", @1: &h_average, @2: &h_scores}}
LC-R: 🜊1000🜁0 "aggregate"🜁1 ⟁average🜁2 ⟁scores🜂
LC-T: {C:1000,0="aggregate",1=@average,2=@scores}
LC-B: [1000|0:"aggregate"|1:&average|2:&scores]

English: Find maximum value
HLXL: {1000: {@0: "aggregate", @1: &h_max, @2: &h_value}}
LC-R: 🜊1000🜁0 "aggregate"🜁1 ⟁max🜁2 ⟁value🜂
LC-T: {C:1000,0="aggregate",1=@max,2=@value}
LC-B: [1000|0:"aggregate"|1:&max|2:&value]

English: Find minimum value
HLXL: {1000: {@0: "aggregate", @1: &h_min, @2: &h_value}}
LC-R: 🜊1000🜁0 "aggregate"🜁1 ⟁min🜁2 ⟁value🜂
LC-T: {C:1000,0="aggregate",1=@min,2=@value}
LC-B: [1000|0:"aggregate"|1:&min|2:&value]

English: Count all items
HLXL: {1000: {@0: "aggregate", @1: &h_count, @2: &h_items}}
LC-R: 🜊1000🜁0 "aggregate"🜁1 ⟁count🜁2 ⟁items🜂
LC-T: {C:1000,0="aggregate",1=@count,2=@items}
LC-B: [1000|0:"aggregate"|1:&count|2:&items]

### Read/Write Operations

English: Read from database
HLXL: {1000: {@0: "read", @1: "database"}}
LC-R: 🜊1000🜁0 "read"🜁1 "database"🜂
LC-T: {C:1000,0="read",1="database"}
LC-B: [1000|0:"read"|1:"database"]

English: Load config file
HLXL: {1000: {@0: "read", @1: "config.json"}}
LC-R: 🜊1000🜁0 "read"🜁1 "config.json"🜂
LC-T: {C:1000,0="read",1="config.json"}
LC-B: [1000|0:"read"|1:"config.json"]

English: Write results to file
HLXL: {1000: {@0: "write", @1: "output.txt", @2: &h_results}}
LC-R: 🜊1000🜁0 "write"🜁1 "output.txt"🜁2 ⟁results🜂
LC-T: {C:1000,0="write",1="output.txt",2=@results}
LC-B: [1000|0:"write"|1:"output.txt"|2:&results]

English: Save data to log
HLXL: {1000: {@0: "write", @1: "log.txt", @2: &h_data}}
LC-R: 🜊1000🜁0 "write"🜁1 "log.txt"🜁2 ⟁data🜂
LC-T: {C:1000,0="write",1="log.txt",2=@data}
LC-B: [1000|0:"write"|1:"log.txt"|2:&data]

English: Store in cache
HLXL: {1000: {@0: "write", @1: "cache", @2: &h_value}}
LC-R: 🜊1000🜁0 "write"🜁1 "cache"🜁2 ⟁value🜂
LC-T: {C:1000,0="write",1="cache",2=@value}
LC-B: [1000|0:"write"|1:"cache"|2:&value]

### Execute Operations

English: Execute command
HLXL: {1000: {@0: "execute", @1: &h_command}}
LC-R: 🜊1000🜁0 "execute"🜁1 ⟁command🜂
LC-T: {C:1000,0="execute",1=@command}
LC-B: [1000|0:"execute"|1:&command]

English: Run the operation
HLXL: {1000: {@0: "execute", @1: &h_operation}}
LC-R: 🜊1000🜁0 "execute"🜁1 ⟁operation🜂
LC-T: {C:1000,0="execute",1=@operation}
LC-B: [1000|0:"execute"|1:&operation]

English: Compute result
HLXL: {1000: {@0: "compute", @1: &h_result}}
LC-R: 🜊1000🜁0 "compute"🜁1 ⟁result🜂
LC-T: {C:1000,0="compute",1=@result}
LC-B: [1000|0:"compute"|1:&result]

English: Validate input against schema
HLXL: {1000: {@0: "validate", @1: &h_input, @2: &h_schema}}
LC-R: 🜊1000🜁0 "validate"🜁1 ⟁input🜁2 ⟁schema🜂
LC-T: {C:1000,0="validate",1=@input,2=@schema}
LC-B: [1000|0:"validate"|1:&input|2:&schema]

English: Process the request
HLXL: {1000: {@0: "process", @1: &h_request}}
LC-R: 🜊1000🜁0 "process"🜁1 ⟁request🜂
LC-T: {C:1000,0="process",1=@request}
LC-B: [1000|0:"process"|1:&request]

---

## SECTION 3: NAVIGATION COMMANDS (20 examples)

English: Navigate to home
HLXL: {1000: {@0: "navigate", @1: &h_home}}
LC-R: 🜊1000🜁0 "navigate"🜁1 ⟁home🜂
LC-T: {C:1000,0="navigate",1=@home}
LC-B: [1000|0:"navigate"|1:&home]

English: Go to settings page
HLXL: {1000: {@0: "navigate", @1: &h_settings}}
LC-R: 🜊1000🜁0 "navigate"🜁1 ⟁settings🜂
LC-T: {C:1000,0="navigate",1=@settings}
LC-B: [1000|0:"navigate"|1:&settings]

English: Open dashboard
HLXL: {1000: {@0: "navigate", @1: &h_dashboard}}
LC-R: 🜊1000🜁0 "navigate"🜁1 ⟁dashboard🜂
LC-T: {C:1000,0="navigate",1=@dashboard}
LC-B: [1000|0:"navigate"|1:&dashboard]

English: Go back to previous page
HLXL: {1000: {@0: "navigate", @1: &h_back}}
LC-R: 🜊1000🜁0 "navigate"🜁1 ⟁back🜂
LC-T: {C:1000,0="navigate",1=@back}
LC-B: [1000|0:"navigate"|1:&back]

English: Navigate forward
HLXL: {1000: {@0: "navigate", @1: &h_forward}}
LC-R: 🜊1000🜁0 "navigate"🜁1 ⟁forward🜂
LC-T: {C:1000,0="navigate",1=@forward}
LC-B: [1000|0:"navigate"|1:&forward]

English: Open file browser
HLXL: {1000: {@0: "open", @1: &h_fileBrowser}}
LC-R: 🜊1000🜁0 "open"🜁1 ⟁fileBrowser🜂
LC-T: {C:1000,0="open",1=@fileBrowser}
LC-B: [1000|0:"open"|1:&fileBrowser]

English: Open terminal
HLXL: {1000: {@0: "open", @1: &h_terminal}}
LC-R: 🜊1000🜁0 "open"🜁1 ⟁terminal🜂
LC-T: {C:1000,0="open",1=@terminal}
LC-B: [1000|0:"open"|1:&terminal]

English: Close current window
HLXL: {1000: {@0: "close", @1: &h_window}}
LC-R: 🜊1000🜁0 "close"🜁1 ⟁window🜂
LC-T: {C:1000,0="close",1=@window}
LC-B: [1000|0:"close"|1:&window]

English: Refresh the page
HLXL: {1000: {@0: "refresh", @1: &h_page}}
LC-R: 🜊1000🜁0 "refresh"🜁1 ⟁page🜂
LC-T: {C:1000,0="refresh",1=@page}
LC-B: [1000|0:"refresh"|1:&page]

English: Scroll to top
HLXL: {1000: {@0: "scroll", @1: &h_top}}
LC-R: 🜊1000🜁0 "scroll"🜁1 ⟁top🜂
LC-T: {C:1000,0="scroll",1=@top}
LC-B: [1000|0:"scroll"|1:&top]

English: Scroll down
HLXL: {1000: {@0: "scroll", @1: &h_down}}
LC-R: 🜊1000🜁0 "scroll"🜁1 ⟁down🜂
LC-T: {C:1000,0="scroll",1=@down}
LC-B: [1000|0:"scroll"|1:&down]

English: Zoom in
HLXL: {1000: {@0: "zoom", @1: &h_in}}
LC-R: 🜊1000🜁0 "zoom"🜁1 ⟁in🜂
LC-T: {C:1000,0="zoom",1=@in}
LC-B: [1000|0:"zoom"|1:&in]

English: Zoom out
HLXL: {1000: {@0: "zoom", @1: &h_out}}
LC-R: 🜊1000🜁0 "zoom"🜁1 ⟁out🜂
LC-T: {C:1000,0="zoom",1=@out}
LC-B: [1000|0:"zoom"|1:&out]

English: Focus on input field
HLXL: {1000: {@0: "focus", @1: &h_input}}
LC-R: 🜊1000🜁0 "focus"🜁1 ⟁input🜂
LC-T: {C:1000,0="focus",1=@input}
LC-B: [1000|0:"focus"|1:&input]

English: Select all text
HLXL: {1000: {@0: "select", @1: &h_all}}
LC-R: 🜊1000🜁0 "select"🜁1 ⟁all🜂
LC-T: {C:1000,0="select",1=@all}
LC-B: [1000|0:"select"|1:&all]

English: Copy selection
HLXL: {1000: {@0: "copy", @1: &h_selection}}
LC-R: 🜊1000🜁0 "copy"🜁1 ⟁selection🜂
LC-T: {C:1000,0="copy",1=@selection}
LC-B: [1000|0:"copy"|1:&selection]

English: Paste from clipboard
HLXL: {1000: {@0: "paste", @1: &h_clipboard}}
LC-R: 🜊1000🜁0 "paste"🜁1 ⟁clipboard🜂
LC-T: {C:1000,0="paste",1=@clipboard}
LC-B: [1000|0:"paste"|1:&clipboard]

English: Undo last action
HLXL: {1000: {@0: "undo", @1: &h_last}}
LC-R: 🜊1000🜁0 "undo"🜁1 ⟁last🜂
LC-T: {C:1000,0="undo",1=@last}
LC-B: [1000|0:"undo"|1:&last]

English: Redo action
HLXL: {1000: {@0: "redo", @1: &h_action}}
LC-R: 🜊1000🜁0 "redo"🜁1 ⟁action🜂
LC-T: {C:1000,0="redo",1=@action}
LC-B: [1000|0:"redo"|1:&action]

English: Show help menu
HLXL: {1000: {@0: "show", @1: &h_help}}
LC-R: 🜊1000🜁0 "show"🜁1 ⟁help🜂
LC-T: {C:1000,0="show",1=@help}
LC-B: [1000|0:"show"|1:&help]

---

## SECTION 4: DATA STRUCTURES (25 examples)

### Arrays

English: Empty list
HLXL: []
LC-R: 🜃🜄
LC-T: []
LC-B: [[]]

English: List of numbers one two three
HLXL: [1, 2, 3]
LC-R: 🜃1, 2, 3🜄
LC-T: [1,2,3]
LC-B: [[0x01,0x02,0x03]]

English: List of names Alice Bob Carol
HLXL: ["Alice", "Bob", "Carol"]
LC-R: 🜃"Alice", "Bob", "Carol"🜄
LC-T: ["Alice","Bob","Carol"]
LC-B: [["Alice","Bob","Carol"]]

English: List of handles a b c
HLXL: [&h_a, &h_b, &h_c]
LC-R: 🜃⟁a, ⟁b, ⟁c🜄
LC-T: [@a,@b,@c]
LC-B: [[&a,&b,&c]]

English: Mixed list with number string boolean
HLXL: [42, "test", true]
LC-R: 🜃42, "test", ⊤🜄
LC-T: [42,"test",TRUE]
LC-B: [[0x2a,"test",T]]

English: Coordinate list x y z
HLXL: [100, 200, 300]
LC-R: 🜃100, 200, 300🜄
LC-T: [100,200,300]
LC-B: [[0x64,0xc8,0x12c]]

English: Float values for weights
HLXL: [0.1, 0.5, 0.9]
LC-R: 🜃0.1, 0.5, 0.9🜄
LC-T: [0.1,0.5,0.9]
LC-B: [[0.1,0.5,0.9]]

English: Single element list
HLXL: [42]
LC-R: 🜃42🜄
LC-T: [42]
LC-B: [[0x2a]]

### Objects

English: User object with name
HLXL: {name: "Alice"}
LC-R: ◇name: "Alice"◆
LC-T: {name:"Alice"}
LC-B: [{name:"Alice"}]

English: Point with x and y coordinates
HLXL: {x: 10, y: 20}
LC-R: ◇x: 10, y: 20◆
LC-T: {x:10,y:20}
LC-B: [{x:0x0a,y:0x14}]

English: User profile with name and age
HLXL: {name: "Alice", age: 30}
LC-R: ◇name: "Alice", age: 30◆
LC-T: {name:"Alice",age:30}
LC-B: [{name:"Alice",age:0x1e}]

English: Config with debug flag
HLXL: {debug: true, verbose: false}
LC-R: ◇debug: ⊤, verbose: ⊥◆
LC-T: {debug:TRUE,verbose:FALSE}
LC-B: [{debug:T,verbose:F}]

English: Color with RGB values
HLXL: {r: 255, g: 128, b: 64}
LC-R: ◇r: 255, g: 128, b: 64◆
LC-T: {r:255,g:128,b:64}
LC-B: [{r:0xff,g:0x80,b:0x40}]

English: Size with width and height
HLXL: {width: 800, height: 600}
LC-R: ◇width: 800, height: 600◆
LC-T: {width:800,height:600}
LC-B: [{width:0x320,height:0x258}]

English: Score record with player and points
HLXL: {player: "Bob", score: 1500}
LC-R: ◇player: "Bob", score: 1500◆
LC-T: {player:"Bob",score:1500}
LC-B: [{player:"Bob",score:0x5dc}]

English: Status with enabled flag
HLXL: {enabled: true, count: 5}
LC-R: ◇enabled: ⊤, count: 5◆
LC-T: {enabled:TRUE,count:5}
LC-B: [{enabled:T,count:0x05}]

English: Empty object
HLXL: {}
LC-R: ◇◆
LC-T: {}
LC-B: [{}]

### Contracts

English: Integer literal forty-two
HLXL: {14: {@0: 42}}
LC-R: 🜊14🜁0 42🜂
LC-T: {C:14,0=42}
LC-B: [14|0:0x2a]

English: Float literal pi
HLXL: {15: {@0: 3.14159}}
LC-R: 🜊15🜁0 3.14159🜂
LC-T: {C:15,0=3.14159}
LC-B: [15|0:3.14159]

English: Text literal hello
HLXL: {16: {@0: "hello"}}
LC-R: 🜊16🜁0 "hello"🜂
LC-T: {C:16,0="hello"}
LC-B: [16|0:"hello"]

English: Handle reference to model
HLXL: {20: {@0: &h_model}}
LC-R: 🜊20🜁0 ⟁model🜂
LC-T: {C:20,0=@model}
LC-B: [20|0:&model]

English: Null literal
HLXL: {21: {@0: null}}
LC-R: 🜊21🜁0 ∅🜂
LC-T: {C:21,0=NULL}
LC-B: [21|0:_]

English: Boolean true literal
HLXL: {22: {@0: true}}
LC-R: 🜊22🜁0 ⊤🜂
LC-T: {C:22,0=TRUE}
LC-B: [22|0:T]

English: Boolean false literal
HLXL: {22: {@0: false}}
LC-R: 🜊22🜁0 ⊥🜂
LC-T: {C:22,0=FALSE}
LC-B: [22|0:F]

---

## SECTION 5: COMPLEX QUERIES (25 examples)

English: Copy source to destination
HLXL: {1000: {@0: "copy", @1: &h_source, @2: &h_dest}}
LC-R: 🜊1000🜁0 "copy"🜁1 ⟁source🜁2 ⟁dest🜂
LC-T: {C:1000,0="copy",1=@source,2=@dest}
LC-B: [1000|0:"copy"|1:&source|2:&dest]

English: Merge dataset A with dataset B
HLXL: {1000: {@0: "merge", @1: &h_datasetA, @2: &h_datasetB}}
LC-R: 🜊1000🜁0 "merge"🜁1 ⟁datasetA🜁2 ⟁datasetB🜂
LC-T: {C:1000,0="merge",1=@datasetA,2=@datasetB}
LC-B: [1000|0:"merge"|1:&datasetA|2:&datasetB]

English: Join tables users and orders
HLXL: {1000: {@0: "join", @1: &h_users, @2: &h_orders}}
LC-R: 🜊1000🜁0 "join"🜁1 ⟁users🜁2 ⟁orders🜂
LC-T: {C:1000,0="join",1=@users,2=@orders}
LC-B: [1000|0:"join"|1:&users|2:&orders]

English: Sort items by score descending
HLXL: {1000: {@0: "sort", @1: &h_items, @2: &h_score, @3: &h_desc}}
LC-R: 🜊1000🜁0 "sort"🜁1 ⟁items🜁2 ⟁score🜁3 ⟁desc🜂
LC-T: {C:1000,0="sort",1=@items,2=@score,3=@desc}
LC-B: [1000|0:"sort"|1:&items|2:&score|3:&desc]

English: Group records by category
HLXL: {1000: {@0: "group", @1: &h_records, @2: &h_category}}
LC-R: 🜊1000🜁0 "group"🜁1 ⟁records🜁2 ⟁category🜂
LC-T: {C:1000,0="group",1=@records,2=@category}
LC-B: [1000|0:"group"|1:&records|2:&category]

English: Limit results to ten
HLXL: {1000: {@0: "limit", @1: &h_results, @2: 10}}
LC-R: 🜊1000🜁0 "limit"🜁1 ⟁results🜁2 10🜂
LC-T: {C:1000,0="limit",1=@results,2=10}
LC-B: [1000|0:"limit"|1:&results|2:0x0a]

English: Skip first five items
HLXL: {1000: {@0: "skip", @1: &h_items, @2: 5}}
LC-R: 🜊1000🜁0 "skip"🜁1 ⟁items🜁2 5🜂
LC-T: {C:1000,0="skip",1=@items,2=5}
LC-B: [1000|0:"skip"|1:&items|2:0x05]

English: Map function over array
HLXL: {1000: {@0: "map", @1: &h_function, @2: &h_array}}
LC-R: 🜊1000🜁0 "map"🜁1 ⟁function🜁2 ⟁array🜂
LC-T: {C:1000,0="map",1=@function,2=@array}
LC-B: [1000|0:"map"|1:&function|2:&array]

English: Reduce array with accumulator
HLXL: {1000: {@0: "reduce", @1: &h_array, @2: &h_accumulator}}
LC-R: 🜊1000🜁0 "reduce"🜁1 ⟁array🜁2 ⟁accumulator🜂
LC-T: {C:1000,0="reduce",1=@array,2=@accumulator}
LC-B: [1000|0:"reduce"|1:&array|2:&accumulator]

English: Flatten nested structure
HLXL: {1000: {@0: "flatten", @1: &h_nested}}
LC-R: 🜊1000🜁0 "flatten"🜁1 ⟁nested🜂
LC-T: {C:1000,0="flatten",1=@nested}
LC-B: [1000|0:"flatten"|1:&nested]

English: Reverse the list
HLXL: {1000: {@0: "reverse", @1: &h_list}}
LC-R: 🜊1000🜁0 "reverse"🜁1 ⟁list🜂
LC-T: {C:1000,0="reverse",1=@list}
LC-B: [1000|0:"reverse"|1:&list]

English: Unique values from collection
HLXL: {1000: {@0: "unique", @1: &h_collection}}
LC-R: 🜊1000🜁0 "unique"🜁1 ⟁collection🜂
LC-T: {C:1000,0="unique",1=@collection}
LC-B: [1000|0:"unique"|1:&collection]

English: Split string by delimiter
HLXL: {1000: {@0: "split", @1: &h_string, @2: ","}}
LC-R: 🜊1000🜁0 "split"🜁1 ⟁string🜁2 ","🜂
LC-T: {C:1000,0="split",1=@string,2=","}
LC-B: [1000|0:"split"|1:&string|2:","]

English: Concatenate strings together
HLXL: {1000: {@0: "concat", @1: &h_strings}}
LC-R: 🜊1000🜁0 "concat"🜁1 ⟁strings🜂
LC-T: {C:1000,0="concat",1=@strings}
LC-B: [1000|0:"concat"|1:&strings]

English: Replace old with new in text
HLXL: {1000: {@0: "replace", @1: &h_text, @2: &h_old, @3: &h_new}}
LC-R: 🜊1000🜁0 "replace"🜁1 ⟁text🜁2 ⟁old🜁3 ⟁new🜂
LC-T: {C:1000,0="replace",1=@text,2=@old,3=@new}
LC-B: [1000|0:"replace"|1:&text|2:&old|3:&new]

English: Trim whitespace from string
HLXL: {1000: {@0: "trim", @1: &h_string}}
LC-R: 🜊1000🜁0 "trim"🜁1 ⟁string🜂
LC-T: {C:1000,0="trim",1=@string}
LC-B: [1000|0:"trim"|1:&string]

English: Check if value exists in collection
HLXL: {1000: {@0: "contains", @1: &h_collection, @2: &h_value}}
LC-R: 🜊1000🜁0 "contains"🜁1 ⟁collection🜁2 ⟁value🜂
LC-T: {C:1000,0="contains",1=@collection,2=@value}
LC-B: [1000|0:"contains"|1:&collection|2:&value]

English: Get length of array
HLXL: {1000: {@0: "length", @1: &h_array}}
LC-R: 🜊1000🜁0 "length"🜁1 ⟁array🜂
LC-T: {C:1000,0="length",1=@array}
LC-B: [1000|0:"length"|1:&array]

English: Get element at index five
HLXL: {1000: {@0: "get", @1: &h_array, @2: 5}}
LC-R: 🜊1000🜁0 "get"🜁1 ⟁array🜁2 5🜂
LC-T: {C:1000,0="get",1=@array,2=5}
LC-B: [1000|0:"get"|1:&array|2:0x05]

English: Set value at index three
HLXL: {1000: {@0: "set", @1: &h_array, @2: 3, @3: &h_value}}
LC-R: 🜊1000🜁0 "set"🜁1 ⟁array🜁2 3🜁3 ⟁value🜂
LC-T: {C:1000,0="set",1=@array,2=3,3=@value}
LC-B: [1000|0:"set"|1:&array|2:0x03|3:&value]

English: Append value to list
HLXL: {1000: {@0: "append", @1: &h_list, @2: &h_value}}
LC-R: 🜊1000🜁0 "append"🜁1 ⟁list🜁2 ⟁value🜂
LC-T: {C:1000,0="append",1=@list,2=@value}
LC-B: [1000|0:"append"|1:&list|2:&value]

English: Remove element from collection
HLXL: {1000: {@0: "remove", @1: &h_collection, @2: &h_element}}
LC-R: 🜊1000🜁0 "remove"🜁1 ⟁collection🜁2 ⟁element🜂
LC-T: {C:1000,0="remove",1=@collection,2=@element}
LC-B: [1000|0:"remove"|1:&collection|2:&element]

English: Clear all items
HLXL: {1000: {@0: "clear", @1: &h_items}}
LC-R: 🜊1000🜁0 "clear"🜁1 ⟁items🜂
LC-T: {C:1000,0="clear",1=@items}
LC-B: [1000|0:"clear"|1:&items]

English: Delete record by id
HLXL: {1000: {@0: "delete", @1: &h_record, @2: &h_id}}
LC-R: 🜊1000🜁0 "delete"🜁1 ⟁record🜁2 ⟁id🜂
LC-T: {C:1000,0="delete",1=@record,2=@id}
LC-B: [1000|0:"delete"|1:&record|2:&id]

English: Update field in object
HLXL: {1000: {@0: "update", @1: &h_object, @2: &h_field, @3: &h_value}}
LC-R: 🜊1000🜁0 "update"🜁1 ⟁object🜁2 ⟁field🜁3 ⟁value🜂
LC-T: {C:1000,0="update",1=@object,2=@field,3=@value}
LC-B: [1000|0:"update"|1:&object|2:&field|3:&value]

---

## SECTION 6: GPU AND COMPUTE OPERATIONS (15 examples)

English: Load shader module
HLXL: {900: {@0: &h_spirv, @1: "main", @2: "compute"}}
LC-R: 🜊900🜁0 ⟁spirv🜁1 "main"🜁2 "compute"🜂
LC-T: {C:900,0=@spirv,1="main",2="compute"}
LC-B: [900|0:&spirv|1:"main"|2:"compute"]

English: Create vertex shader
HLXL: {900: {@0: &h_vertex, @1: "vs_main", @2: "vertex"}}
LC-R: 🜊900🜁0 ⟁vertex🜁1 "vs_main"🜁2 "vertex"🜂
LC-T: {C:900,0=@vertex,1="vs_main",2="vertex"}
LC-B: [900|0:&vertex|1:"vs_main"|2:"vertex"]

English: Create fragment shader
HLXL: {900: {@0: &h_fragment, @1: "fs_main", @2: "fragment"}}
LC-R: 🜊900🜁0 ⟁fragment🜁1 "fs_main"🜁2 "fragment"🜂
LC-T: {C:900,0=@fragment,1="fs_main",2="fragment"}
LC-B: [900|0:&fragment|1:"fs_main"|2:"fragment"]

English: Configure compute kernel map
HLXL: {901: {@0: "map", @1: &h_shader}}
LC-R: 🜊901🜁0 "map"🜁1 ⟁shader🜂
LC-T: {C:901,0="map",1=@shader}
LC-B: [901|0:"map"|1:&shader]

English: Configure compute kernel reduce
HLXL: {901: {@0: "reduce", @1: &h_kernel}}
LC-R: 🜊901🜁0 "reduce"🜁1 ⟁kernel🜂
LC-T: {C:901,0="reduce",1=@kernel}
LC-B: [901|0:"reduce"|1:&kernel]

English: Configure compute kernel scan
HLXL: {901: {@0: "scan", @1: &h_compute}}
LC-R: 🜊901🜁0 "scan"🜁1 ⟁compute🜂
LC-T: {C:901,0="scan",1=@compute}
LC-B: [901|0:"scan"|1:&compute]

English: Create render pipeline
HLXL: {902: {@0: "render_pipeline", @1: [&h_vs, &h_fs]}}
LC-R: 🜊902🜁0 "render_pipeline"🜁1 🜃⟁vs, ⟁fs🜄🜂
LC-T: {C:902,0="render_pipeline",1=[@vs,@fs]}
LC-B: [902|0:"render_pipeline"|1:[&vs,&fs]]

English: Create compute pipeline
HLXL: {902: {@0: "compute_pipeline", @1: [&h_kernel]}}
LC-R: 🜊902🜁0 "compute_pipeline"🜁1 🜃⟁kernel🜄🜂
LC-T: {C:902,0="compute_pipeline",1=[@kernel]}
LC-B: [902|0:"compute_pipeline"|1:[&kernel]]

English: Dispatch compute workgroup
HLXL: {1000: {@0: "dispatch", @1: &h_pipeline, @2: [64, 64, 1]}}
LC-R: 🜊1000🜁0 "dispatch"🜁1 ⟁pipeline🜁2 🜃64, 64, 1🜄🜂
LC-T: {C:1000,0="dispatch",1=@pipeline,2=[64,64,1]}
LC-B: [1000|0:"dispatch"|1:&pipeline|2:[0x40,0x40,0x01]]

English: Bind buffer to slot
HLXL: {1000: {@0: "bind", @1: &h_buffer, @2: 0}}
LC-R: 🜊1000🜁0 "bind"🜁1 ⟁buffer🜁2 0🜂
LC-T: {C:1000,0="bind",1=@buffer,2=0}
LC-B: [1000|0:"bind"|1:&buffer|2:0x00]

English: Upload data to GPU
HLXL: {1000: {@0: "upload", @1: &h_data, @2: &h_gpuBuffer}}
LC-R: 🜊1000🜁0 "upload"🜁1 ⟁data🜁2 ⟁gpuBuffer🜂
LC-T: {C:1000,0="upload",1=@data,2=@gpuBuffer}
LC-B: [1000|0:"upload"|1:&data|2:&gpuBuffer]

English: Download results from GPU
HLXL: {1000: {@0: "download", @1: &h_gpuBuffer, @2: &h_output}}
LC-R: 🜊1000🜁0 "download"🜁1 ⟁gpuBuffer🜁2 ⟁output🜂
LC-T: {C:1000,0="download",1=@gpuBuffer,2=@output}
LC-B: [1000|0:"download"|1:&gpuBuffer|2:&output]

English: Synchronize GPU operations
HLXL: {1000: {@0: "sync", @1: &h_device}}
LC-R: 🜊1000🜁0 "sync"🜁1 ⟁device🜂
LC-T: {C:1000,0="sync",1=@device}
LC-B: [1000|0:"sync"|1:&device]

English: Render frame to target
HLXL: {1000: {@0: "render", @1: &h_scene, @2: &h_target}}
LC-R: 🜊1000🜁0 "render"🜁1 ⟁scene🜁2 ⟁target🜂
LC-T: {C:1000,0="render",1=@scene,2=@target}
LC-B: [1000|0:"render"|1:&scene|2:&target]

English: Present swapchain image
HLXL: {1000: {@0: "present", @1: &h_swapchain}}
LC-R: 🜊1000🜁0 "present"🜁1 ⟁swapchain🜂
LC-T: {C:1000,0="present",1=@swapchain}
LC-B: [1000|0:"present"|1:&swapchain]

---

## SECTION 7: ML AND AI OPERATIONS (15 examples)

English: Train model on data
HLXL: {1000: {@0: "train", @1: &h_model, @2: &h_data}}
LC-R: 🜊1000🜁0 "train"🜁1 ⟁model🜁2 ⟁data🜂
LC-T: {C:1000,0="train",1=@model,2=@data}
LC-B: [1000|0:"train"|1:&model|2:&data]

English: Run inference on input
HLXL: {1000: {@0: "infer", @1: &h_model, @2: &h_input}}
LC-R: 🜊1000🜁0 "infer"🜁1 ⟁model🜁2 ⟁input🜂
LC-T: {C:1000,0="infer",1=@model,2=@input}
LC-B: [1000|0:"infer"|1:&model|2:&input]

English: Evaluate model accuracy
HLXL: {1000: {@0: "evaluate", @1: &h_model, @2: &h_testData}}
LC-R: 🜊1000🜁0 "evaluate"🜁1 ⟁model🜁2 ⟁testData🜂
LC-T: {C:1000,0="evaluate",1=@model,2=@testData}
LC-B: [1000|0:"evaluate"|1:&model|2:&testData]

English: Save model checkpoint
HLXL: {1000: {@0: "save", @1: &h_model, @2: "checkpoint.pt"}}
LC-R: 🜊1000🜁0 "save"🜁1 ⟁model🜁2 "checkpoint.pt"🜂
LC-T: {C:1000,0="save",1=@model,2="checkpoint.pt"}
LC-B: [1000|0:"save"|1:&model|2:"checkpoint.pt"]

English: Load pretrained weights
HLXL: {1000: {@0: "load", @1: &h_model, @2: "weights.pt"}}
LC-R: 🜊1000🜁0 "load"🜁1 ⟁model🜁2 "weights.pt"🜂
LC-T: {C:1000,0="load",1=@model,2="weights.pt"}
LC-B: [1000|0:"load"|1:&model|2:"weights.pt"]

English: Forward pass through network
HLXL: {1000: {@0: "forward", @1: &h_network, @2: &h_batch}}
LC-R: 🜊1000🜁0 "forward"🜁1 ⟁network🜁2 ⟁batch🜂
LC-T: {C:1000,0="forward",1=@network,2=@batch}
LC-B: [1000|0:"forward"|1:&network|2:&batch]

English: Backward pass compute gradients
HLXL: {1000: {@0: "backward", @1: &h_loss}}
LC-R: 🜊1000🜁0 "backward"🜁1 ⟁loss🜂
LC-T: {C:1000,0="backward",1=@loss}
LC-B: [1000|0:"backward"|1:&loss]

English: Optimize model parameters
HLXL: {1000: {@0: "optimize", @1: &h_optimizer, @2: &h_gradients}}
LC-R: 🜊1000🜁0 "optimize"🜁1 ⟁optimizer🜁2 ⟁gradients🜂
LC-T: {C:1000,0="optimize",1=@optimizer,2=@gradients}
LC-B: [1000|0:"optimize"|1:&optimizer|2:&gradients]

English: Embed text into vectors
HLXL: {1000: {@0: "embed", @1: &h_text, @2: &h_embedder}}
LC-R: 🜊1000🜁0 "embed"🜁1 ⟁text🜁2 ⟁embedder🜂
LC-T: {C:1000,0="embed",1=@text,2=@embedder}
LC-B: [1000|0:"embed"|1:&text|2:&embedder]

English: Tokenize input text
HLXL: {1000: {@0: "tokenize", @1: &h_text, @2: &h_tokenizer}}
LC-R: 🜊1000🜁0 "tokenize"🜁1 ⟁text🜁2 ⟁tokenizer🜂
LC-T: {C:1000,0="tokenize",1=@text,2=@tokenizer}
LC-B: [1000|0:"tokenize"|1:&text|2:&tokenizer]

English: Decode tokens to text
HLXL: {1000: {@0: "decode", @1: &h_tokens, @2: &h_tokenizer}}
LC-R: 🜊1000🜁0 "decode"🜁1 ⟁tokens🜁2 ⟁tokenizer🜂
LC-T: {C:1000,0="decode",1=@tokens,2=@tokenizer}
LC-B: [1000|0:"decode"|1:&tokens|2:&tokenizer]

English: Generate completion from prompt
HLXL: {1000: {@0: "generate", @1: &h_model, @2: &h_prompt}}
LC-R: 🜊1000🜁0 "generate"🜁1 ⟁model🜁2 ⟁prompt🜂
LC-T: {C:1000,0="generate",1=@model,2=@prompt}
LC-B: [1000|0:"generate"|1:&model|2:&prompt]

English: Sample from distribution
HLXL: {1000: {@0: "sample", @1: &h_distribution, @2: &h_temperature}}
LC-R: 🜊1000🜁0 "sample"🜁1 ⟁distribution🜁2 ⟁temperature🜂
LC-T: {C:1000,0="sample",1=@distribution,2=@temperature}
LC-B: [1000|0:"sample"|1:&distribution|2:&temperature]

English: Batch inputs together
HLXL: {1000: {@0: "batch", @1: &h_inputs, @2: 32}}
LC-R: 🜊1000🜁0 "batch"🜁1 ⟁inputs🜁2 32🜂
LC-T: {C:1000,0="batch",1=@inputs,2=32}
LC-B: [1000|0:"batch"|1:&inputs|2:0x20]

English: Collate batch samples
HLXL: {1000: {@0: "collate", @1: &h_samples}}
LC-R: 🜊1000🜁0 "collate"🜁1 ⟁samples🜂
LC-T: {C:1000,0="collate",1=@samples}
LC-B: [1000|0:"collate"|1:&samples]

---

## SECTION 8: EXPRESSIONS AND CONTROL FLOW (15 examples)

English: Create code block named main
HLXL: {100: {@0: "main", @1: []}}
LC-R: 🜊100🜁0 "main"🜁1 🜃🜄🜂
LC-T: {C:100,0="main",1=[]}
LC-B: [100|0:"main"|1:[]]

English: Add expression one plus two
HLXL: {101: {@0: "add", @1: 1, @2: 2}}
LC-R: 🜊101🜁0 "add"🜁1 1🜁2 2🜂
LC-T: {C:101,0="add",1=1,2=2}
LC-B: [101|0:"add"|1:0x01|2:0x02]

English: Multiply five times ten
HLXL: {101: {@0: "multiply", @1: 5, @2: 10}}
LC-R: 🜊101🜁0 "multiply"🜁1 5🜁2 10🜂
LC-T: {C:101,0="multiply",1=5,2=10}
LC-B: [101|0:"multiply"|1:0x05|2:0x0a]

English: Reference variable x
HLXL: {102: {@0: "x"}}
LC-R: 🜊102🜁0 "x"🜂
LC-T: {C:102,0="x"}
LC-B: [102|0:"x"]

English: Reference variable result
HLXL: {102: {@0: "result"}}
LC-R: 🜊102🜁0 "result"🜂
LC-T: {C:102,0="result"}
LC-B: [102|0:"result"]

English: Assign forty-two to x
HLXL: {103: {@0: "x", @1: 42}}
LC-R: 🜊103🜁0 "x"🜁1 42🜂
LC-T: {C:103,0="x",1=42}
LC-B: [103|0:"x"|1:0x2a]

English: Assign Alice to name
HLXL: {103: {@0: "name", @1: "Alice"}}
LC-R: 🜊103🜁0 "name"🜁1 "Alice"🜂
LC-T: {C:103,0="name",1="Alice"}
LC-B: [103|0:"name"|1:"Alice"]

English: Set flag to true
HLXL: {103: {@0: "flag", @1: true}}
LC-R: 🜊103🜁0 "flag"🜁1 ⊤🜂
LC-T: {C:103,0="flag",1=TRUE}
LC-B: [103|0:"flag"|1:T]

English: Define function add with parameters a and b
HLXL: {104: {@0: "add", @1: ["a", "b"], @2: &h_body}}
LC-R: 🜊104🜁0 "add"🜁1 🜃"a", "b"🜄🜁2 ⟁body🜂
LC-T: {C:104,0="add",1=["a","b"],2=@body}
LC-B: [104|0:"add"|1:["a","b"]|2:&body]

English: Define function square with parameter x
HLXL: {104: {@0: "square", @1: ["x"], @2: &h_impl}}
LC-R: 🜊104🜁0 "square"🜁1 🜃"x"🜄🜁2 ⟁impl🜂
LC-T: {C:104,0="square",1=["x"],2=@impl}
LC-B: [104|0:"square"|1:["x"]|2:&impl]

English: Call function print with hello
HLXL: {105: {@0: "print", @1: ["hello"]}}
LC-R: 🜊105🜁0 "print"🜁1 🜃"hello"🜄🜂
LC-T: {C:105,0="print",1=["hello"]}
LC-B: [105|0:"print"|1:["hello"]]

English: Call function add with one and two
HLXL: {105: {@0: "add", @1: [1, 2]}}
LC-R: 🜊105🜁0 "add"🜁1 🜃1, 2🜄🜂
LC-T: {C:105,0="add",1=[1,2]}
LC-B: [105|0:"add"|1:[0x01,0x02]]

English: Call function max with ten twenty thirty
HLXL: {105: {@0: "max", @1: [10, 20, 30]}}
LC-R: 🜊105🜁0 "max"🜁1 🜃10, 20, 30🜄🜂
LC-T: {C:105,0="max",1=[10,20,30]}
LC-B: [105|0:"max"|1:[0x0a,0x14,0x1e]]

English: Conditional if true then a else b
HLXL: {106: {@0: true, @1: &h_a, @2: &h_b}}
LC-R: 🜊106🜁0 ⊤🜁1 ⟁a🜁2 ⟁b🜂
LC-T: {C:106,0=TRUE,1=@a,2=@b}
LC-B: [106|0:T|1:&a|2:&b]

English: Loop while condition do body
HLXL: {107: {@0: &h_condition, @1: &h_body}}
LC-R: 🜊107🜁0 ⟁condition🜁1 ⟁body🜂
LC-T: {C:107,0=@condition,1=@body}
LC-B: [107|0:&condition|1:&body]

---

## GLYPH REFERENCE

### LC-R Glyphs
| Glyph | Meaning | Unicode |
|-------|---------|---------|
| ∅ | null | U+2205 |
| ⊤ | true | U+22A4 |
| ⊥ | false | U+22A5 |
| ⊠ | bytes prefix | U+22A0 |
| ⟁ | handle reference | U+27C1 |
| 🜊 | contract start | U+1F70A |
| 🜂 | contract end | U+1F702 |
| 🜁 | field separator | U+1F701 |
| 🜃 | array start | U+1F703 |
| 🜄 | array end | U+1F704 |
| ◇ | object start | U+25C7 |
| ◆ | object end | U+25C6 |

### LC-T Mappings
| LC-R | LC-T |
|------|------|
| ∅ | NULL |
| ⊤ | TRUE |
| ⊥ | FALSE |
| ⊠ | # |
| ⟁ | @ |
| 🜊 | {C: |
| 🜂 | } |
| 🜁 | , |
| 🜃 | [ |
| 🜄 | ] |
| ◇ | { |
| ◆ | } |

### LC-B Mappings
| LC-R | LC-B |
|------|------|
| ∅ | _ |
| ⊤ | T |
| ⊥ | F |
| ⟁ | & |
| 🜊 | [ |
| field sep | \| |
| 🜂 | ] |
| array | [[...]] |
| object | [{...}] |

---

**Total Examples**: 150+
**Formats Covered**: HLXL, LC-R, LC-T, LC-B
**Version**: 1.0.0
**Date**: 2025-12-18

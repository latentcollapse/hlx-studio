# ASCII Specialist (LC-T) Specialized Corpus
# Version: 1.0.0
# Date: 2025-12-18
# Distribution: 70% lc_t, 20% English, 10% lc_r
# Total Examples: 164
#

## SECTION 1: ASCII SPECIALIST (LC-T) NATIVE (114 examples)

English: Represent nothing
HLXL: null
lc_t: NULL

English: Empty value
HLXL: null
lc_t: NULL

English: Represent true
HLXL: true
lc_t: TRUE

English: Represent false
HLXL: false
lc_t: FALSE

English: Enable flag
HLXL: true
lc_t: TRUE

English: Disable flag
HLXL: false
lc_t: FALSE

English: Number zero
HLXL: 0
lc_t: 0

English: Number one
HLXL: 1
lc_t: 1

English: Number forty-two
HLXL: 42
lc_t: 42

English: Negative number
HLXL: -100
lc_t: -100

English: Large number
HLXL: 1000
lc_t: 1000

English: Pi constant
HLXL: 3.14159
lc_t: 3.14159

English: Decimal half
HLXL: 0.5
lc_t: 0.5

English: Greeting message
HLXL: "hello"
lc_t: "hello"

English: User name Alice
HLXL: "Alice"
lc_t: "Alice"

English: File path
HLXL: "/home/user/data.txt"
lc_t: "/home/user/data.txt"

English: Reference to AST
HLXL: &h_ast
lc_t: @ast

English: Reference to documents
HLXL: &h_documents
lc_t: @documents

English: Reference to model
HLXL: &h_model
lc_t: @model

English: Reference to query
HLXL: &h_query
lc_t: @query

English: Search for documents
HLXL: {1000: {@0: "search", @1: &h_documents}}
lc_t: {C:1000,0="search",1=@documents}

English: Search files for pattern
HLXL: {1000: {@0: "search", @1: &h_files, @2: "pattern"}}
lc_t: {C:1000,0="search",1=@files,2="pattern"}

English: Search database for users
HLXL: {1000: {@0: "search", @1: &h_database, @2: "users"}}
lc_t: {C:1000,0="search",1=@database,2="users"}

English: Find error in logs
HLXL: {1000: {@0: "search", @1: &h_logs, @2: "error"}}
lc_t: {C:1000,0="search",1=@logs,2="error"}

English: Query the cache
HLXL: {1000: {@0: "search", @1: &h_cache}}
lc_t: {C:1000,0="search",1=@cache}

English: Filter active users
HLXL: {1000: {@0: "filter", @1: &h_users, @2: &h_active}}
lc_t: {C:1000,0="filter",1=@users,2=@active}

English: Filter items where valid
HLXL: {1000: {@0: "filter", @1: &h_items, @2: &h_valid}}
lc_t: {C:1000,0="filter",1=@items,2=@valid}

English: Filter records by status
HLXL: {1000: {@0: "filter", @1: &h_records, @2: &h_status}}
lc_t: {C:1000,0="filter",1=@records,2=@status}

English: Keep only recent documents
HLXL: {1000: {@0: "filter", @1: &h_documents, @2: &h_recent}}
lc_t: {C:1000,0="filter",1=@documents,2=@recent}

English: Select enabled features
HLXL: {1000: {@0: "filter", @1: &h_features, @2: &h_enabled}}
lc_t: {C:1000,0="filter",1=@features,2=@enabled}

English: Transform text to uppercase
HLXL: {1000: {@0: "transform", @1: &h_text, @2: &h_uppercase}}
lc_t: {C:1000,0="transform",1=@text,2=@uppercase}

English: Convert data to JSON
HLXL: {1000: {@0: "transform", @1: &h_data, @2: &h_json}}
lc_t: {C:1000,0="transform",1=@data,2=@json}

English: Normalize the input
HLXL: {1000: {@0: "transform", @1: &h_input, @2: &h_normalize}}
lc_t: {C:1000,0="transform",1=@input,2=@normalize}

English: Encode value as base64
HLXL: {1000: {@0: "transform", @1: &h_value, @2: &h_base64}}
lc_t: {C:1000,0="transform",1=@value,2=@base64}

English: Parse string as integer
HLXL: {1000: {@0: "transform", @1: &h_string, @2: &h_parseInt}}
lc_t: {C:1000,0="transform",1=@string,2=@parseInt}

English: Calculate sum of values
HLXL: {1000: {@0: "aggregate", @1: &h_sum, @2: &h_values}}
lc_t: {C:1000,0="aggregate",1=@sum,2=@values}

English: Get average of scores
HLXL: {1000: {@0: "aggregate", @1: &h_average, @2: &h_scores}}
lc_t: {C:1000,0="aggregate",1=@average,2=@scores}

English: Find maximum value
HLXL: {1000: {@0: "aggregate", @1: &h_max, @2: &h_value}}
lc_t: {C:1000,0="aggregate",1=@max,2=@value}

English: Find minimum value
HLXL: {1000: {@0: "aggregate", @1: &h_min, @2: &h_value}}
lc_t: {C:1000,0="aggregate",1=@min,2=@value}

English: Count all items
HLXL: {1000: {@0: "aggregate", @1: &h_count, @2: &h_items}}
lc_t: {C:1000,0="aggregate",1=@count,2=@items}

English: Read from database
HLXL: {1000: {@0: "read", @1: "database"}}
lc_t: {C:1000,0="read",1="database"}

English: Load config file
HLXL: {1000: {@0: "read", @1: "config.json"}}
lc_t: {C:1000,0="read",1="config.json"}

English: Write results to file
HLXL: {1000: {@0: "write", @1: "output.txt", @2: &h_results}}
lc_t: {C:1000,0="write",1="output.txt",2=@results}

English: Save data to log
HLXL: {1000: {@0: "write", @1: "log.txt", @2: &h_data}}
lc_t: {C:1000,0="write",1="log.txt",2=@data}

English: Store in cache
HLXL: {1000: {@0: "write", @1: "cache", @2: &h_value}}
lc_t: {C:1000,0="write",1="cache",2=@value}

English: Execute command
HLXL: {1000: {@0: "execute", @1: &h_command}}
lc_t: {C:1000,0="execute",1=@command}

English: Run the operation
HLXL: {1000: {@0: "execute", @1: &h_operation}}
lc_t: {C:1000,0="execute",1=@operation}

English: Compute result
HLXL: {1000: {@0: "compute", @1: &h_result}}
lc_t: {C:1000,0="compute",1=@result}

English: Validate input against schema
HLXL: {1000: {@0: "validate", @1: &h_input, @2: &h_schema}}
lc_t: {C:1000,0="validate",1=@input,2=@schema}

English: Process the request
HLXL: {1000: {@0: "process", @1: &h_request}}
lc_t: {C:1000,0="process",1=@request}

English: Navigate to home
HLXL: {1000: {@0: "navigate", @1: &h_home}}
lc_t: {C:1000,0="navigate",1=@home}

English: Go to settings page
HLXL: {1000: {@0: "navigate", @1: &h_settings}}
lc_t: {C:1000,0="navigate",1=@settings}

English: Open dashboard
HLXL: {1000: {@0: "navigate", @1: &h_dashboard}}
lc_t: {C:1000,0="navigate",1=@dashboard}

English: Go back to previous page
HLXL: {1000: {@0: "navigate", @1: &h_back}}
lc_t: {C:1000,0="navigate",1=@back}

English: Navigate forward
HLXL: {1000: {@0: "navigate", @1: &h_forward}}
lc_t: {C:1000,0="navigate",1=@forward}

English: Open file browser
HLXL: {1000: {@0: "open", @1: &h_fileBrowser}}
lc_t: {C:1000,0="open",1=@fileBrowser}

English: Open terminal
HLXL: {1000: {@0: "open", @1: &h_terminal}}
lc_t: {C:1000,0="open",1=@terminal}

English: Close current window
HLXL: {1000: {@0: "close", @1: &h_window}}
lc_t: {C:1000,0="close",1=@window}

English: Refresh the page
HLXL: {1000: {@0: "refresh", @1: &h_page}}
lc_t: {C:1000,0="refresh",1=@page}

English: Scroll to top
HLXL: {1000: {@0: "scroll", @1: &h_top}}
lc_t: {C:1000,0="scroll",1=@top}

English: Scroll down
HLXL: {1000: {@0: "scroll", @1: &h_down}}
lc_t: {C:1000,0="scroll",1=@down}

English: Zoom in
HLXL: {1000: {@0: "zoom", @1: &h_in}}
lc_t: {C:1000,0="zoom",1=@in}

English: Zoom out
HLXL: {1000: {@0: "zoom", @1: &h_out}}
lc_t: {C:1000,0="zoom",1=@out}

English: Focus on input field
HLXL: {1000: {@0: "focus", @1: &h_input}}
lc_t: {C:1000,0="focus",1=@input}

English: Select all text
HLXL: {1000: {@0: "select", @1: &h_all}}
lc_t: {C:1000,0="select",1=@all}

English: Copy selection
HLXL: {1000: {@0: "copy", @1: &h_selection}}
lc_t: {C:1000,0="copy",1=@selection}

English: Paste from clipboard
HLXL: {1000: {@0: "paste", @1: &h_clipboard}}
lc_t: {C:1000,0="paste",1=@clipboard}

English: Undo last action
HLXL: {1000: {@0: "undo", @1: &h_last}}
lc_t: {C:1000,0="undo",1=@last}

English: Redo action
HLXL: {1000: {@0: "redo", @1: &h_action}}
lc_t: {C:1000,0="redo",1=@action}

English: Show help menu
HLXL: {1000: {@0: "show", @1: &h_help}}
lc_t: {C:1000,0="show",1=@help}

English: Empty list
HLXL: []
lc_t: []

English: List of numbers one two three
HLXL: [1, 2, 3]
lc_t: [1,2,3]

English: List of names Alice Bob Carol
HLXL: ["Alice", "Bob", "Carol"]
lc_t: ["Alice","Bob","Carol"]

English: List of handles a b c
HLXL: [&h_a, &h_b, &h_c]
lc_t: [@a,@b,@c]

English: Mixed list with number string boolean
HLXL: [42, "test", true]
lc_t: [42,"test",TRUE]

English: Coordinate list x y z
HLXL: [100, 200, 300]
lc_t: [100,200,300]

English: Float values for weights
HLXL: [0.1, 0.5, 0.9]
lc_t: [0.1,0.5,0.9]

English: Single element list
HLXL: [42]
lc_t: [42]

English: User object with name
HLXL: {name: "Alice"}
lc_t: {name:"Alice"}

English: Point with x and y coordinates
HLXL: {x: 10, y: 20}
lc_t: {x:10,y:20}

English: User profile with name and age
HLXL: {name: "Alice", age: 30}
lc_t: {name:"Alice",age:30}

English: Config with debug flag
HLXL: {debug: true, verbose: false}
lc_t: {debug:TRUE,verbose:FALSE}

English: Color with RGB values
HLXL: {r: 255, g: 128, b: 64}
lc_t: {r:255,g:128,b:64}

English: Size with width and height
HLXL: {width: 800, height: 600}
lc_t: {width:800,height:600}

English: Score record with player and points
HLXL: {player: "Bob", score: 1500}
lc_t: {player:"Bob",score:1500}

English: Status with enabled flag
HLXL: {enabled: true, count: 5}
lc_t: {enabled:TRUE,count:5}

English: Empty object
HLXL: {}
lc_t: {}

English: Integer literal forty-two
HLXL: {14: {@0: 42}}
lc_t: {C:14,0=42}

English: Float literal pi
HLXL: {15: {@0: 3.14159}}
lc_t: {C:15,0=3.14159}

English: Text literal hello
HLXL: {16: {@0: "hello"}}
lc_t: {C:16,0="hello"}

English: Handle reference to model
HLXL: {20: {@0: &h_model}}
lc_t: {C:20,0=@model}

English: Null literal
HLXL: {21: {@0: null}}
lc_t: {C:21,0=NULL}

English: Boolean true literal
HLXL: {22: {@0: true}}
lc_t: {C:22,0=TRUE}

English: Boolean false literal
HLXL: {22: {@0: false}}
lc_t: {C:22,0=FALSE}

English: Copy source to destination
HLXL: {1000: {@0: "copy", @1: &h_source, @2: &h_dest}}
lc_t: {C:1000,0="copy",1=@source,2=@dest}

English: Merge dataset A with dataset B
HLXL: {1000: {@0: "merge", @1: &h_datasetA, @2: &h_datasetB}}
lc_t: {C:1000,0="merge",1=@datasetA,2=@datasetB}

English: Join tables users and orders
HLXL: {1000: {@0: "join", @1: &h_users, @2: &h_orders}}
lc_t: {C:1000,0="join",1=@users,2=@orders}

English: Sort items by score descending
HLXL: {1000: {@0: "sort", @1: &h_items, @2: &h_score, @3: &h_desc}}
lc_t: {C:1000,0="sort",1=@items,2=@score,3=@desc}

English: Group records by category
HLXL: {1000: {@0: "group", @1: &h_records, @2: &h_category}}
lc_t: {C:1000,0="group",1=@records,2=@category}

English: Limit results to ten
HLXL: {1000: {@0: "limit", @1: &h_results, @2: 10}}
lc_t: {C:1000,0="limit",1=@results,2=10}

English: Skip first five items
HLXL: {1000: {@0: "skip", @1: &h_items, @2: 5}}
lc_t: {C:1000,0="skip",1=@items,2=5}

English: Map function over array
HLXL: {1000: {@0: "map", @1: &h_function, @2: &h_array}}
lc_t: {C:1000,0="map",1=@function,2=@array}

English: Reduce array with accumulator
HLXL: {1000: {@0: "reduce", @1: &h_array, @2: &h_accumulator}}
lc_t: {C:1000,0="reduce",1=@array,2=@accumulator}

English: Flatten nested structure
HLXL: {1000: {@0: "flatten", @1: &h_nested}}
lc_t: {C:1000,0="flatten",1=@nested}

English: Reverse the list
HLXL: {1000: {@0: "reverse", @1: &h_list}}
lc_t: {C:1000,0="reverse",1=@list}

English: Unique values from collection
HLXL: {1000: {@0: "unique", @1: &h_collection}}
lc_t: {C:1000,0="unique",1=@collection}

English: Split string by delimiter
HLXL: {1000: {@0: "split", @1: &h_string, @2: ","}}
lc_t: {C:1000,0="split",1=@string,2=","}

English: Concatenate strings together
HLXL: {1000: {@0: "concat", @1: &h_strings}}
lc_t: {C:1000,0="concat",1=@strings}

English: Replace old with new in text
HLXL: {1000: {@0: "replace", @1: &h_text, @2: &h_old, @3: &h_new}}
lc_t: {C:1000,0="replace",1=@text,2=@old,3=@new}

English: Trim whitespace from string
HLXL: {1000: {@0: "trim", @1: &h_string}}
lc_t: {C:1000,0="trim",1=@string}

English: Check if value exists in collection
HLXL: {1000: {@0: "contains", @1: &h_collection, @2: &h_value}}
lc_t: {C:1000,0="contains",1=@collection,2=@value}

English: Get length of array
HLXL: {1000: {@0: "length", @1: &h_array}}
lc_t: {C:1000,0="length",1=@array}

English: Get element at index five
HLXL: {1000: {@0: "get", @1: &h_array, @2: 5}}
lc_t: {C:1000,0="get",1=@array,2=5}

English: Set value at index three
HLXL: {1000: {@0: "set", @1: &h_array, @2: 3, @3: &h_value}}
lc_t: {C:1000,0="set",1=@array,2=3,3=@value}


## SECTION 2: ENGLISH DESCRIPTIONS (32 examples)

English: Append value to list

English: Remove element from collection

English: Clear all items

English: Delete record by id

English: Update field in object

English: Load shader module

English: Create vertex shader

English: Create fragment shader

English: Configure compute kernel map

English: Configure compute kernel reduce

English: Configure compute kernel scan

English: Create render pipeline

English: Create compute pipeline

English: Dispatch compute workgroup

English: Bind buffer to slot

English: Upload data to GPU

English: Download results from GPU

English: Synchronize GPU operations

English: Render frame to target

English: Present swapchain image

English: Train model on data

English: Run inference on input

English: Evaluate model accuracy

English: Save model checkpoint

English: Load pretrained weights

English: Forward pass through network

English: Backward pass compute gradients

English: Optimize model parameters

English: Embed text into vectors

English: Tokenize input text

English: Decode tokens to text

English: Generate completion from prompt


## SECTION 3: CROSS-TRACK AWARENESS - lc_r (16 examples)

English: Represent nothing
lc_r: ∅

English: Empty value
lc_r: ∅

English: Represent true
lc_r: ⊤

English: Represent false
lc_r: ⊥

English: Enable flag
lc_r: ⊤

English: Disable flag
lc_r: ⊥

English: Reference to AST
lc_r: ⟁ast

English: Reference to documents
lc_r: ⟁documents

English: Reference to model
lc_r: ⟁model

English: Reference to query
lc_r: ⟁query

English: Search for documents
lc_r: 🜊1000🜁0 "search"🜁1 ⟁documents🜂

English: Search files for pattern
lc_r: 🜊1000🜁0 "search"🜁1 ⟁files🜁2 "pattern"🜂

English: Search database for users
lc_r: 🜊1000🜁0 "search"🜁1 ⟁database🜁2 "users"🜂

English: Find error in logs
lc_r: 🜊1000🜁0 "search"🜁1 ⟁logs🜁2 "error"🜂

English: Query the cache
lc_r: 🜊1000🜁0 "search"🜁1 ⟁cache🜂

English: Filter active users
lc_r: 🜊1000🜁0 "filter"🜁1 ⟁users🜁2 ⟁active🜂

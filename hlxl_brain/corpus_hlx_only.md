HLXL: null
LC-R: ∅
LC-T: NULL
LC-B: [_]
HLXL: null
LC-R: ∅
LC-T: NULL
LC-B: [_]
HLXL: true
LC-R: ⊤
LC-T: TRUE
LC-B: [T]
HLXL: false
LC-R: ⊥
LC-T: FALSE
LC-B: [F]
HLXL: true
LC-R: ⊤
LC-T: TRUE
LC-B: [T]
HLXL: false
LC-R: ⊥
LC-T: FALSE
LC-B: [F]
HLXL: 0
LC-R: 0
LC-T: 0
LC-B: [0x00]
HLXL: 1
LC-R: 1
LC-T: 1
LC-B: [0x01]
HLXL: 42
LC-R: 42
LC-T: 42
LC-B: [0x2a]
HLXL: -100
LC-R: -100
LC-T: -100
LC-B: [0xff9c]
HLXL: 1000
LC-R: 1000
LC-T: 1000
LC-B: [0x03e8]
HLXL: 3.14159
LC-R: 3.14159
LC-T: 3.14159
LC-B: [3.14159]
HLXL: 0.5
LC-R: 0.5
LC-T: 0.5
LC-B: [0.5]
HLXL: "hello"
LC-R: "hello"
LC-T: "hello"
LC-B: ["hello"]
HLXL: "Alice"
LC-R: "Alice"
LC-T: "Alice"
LC-B: ["Alice"]
HLXL: "/home/user/data.txt"
LC-R: "/home/user/data.txt"
LC-T: "/home/user/data.txt"
LC-B: ["/home/user/data.txt"]
HLXL: &h_ast
LC-R: ⟁ast
LC-T: @ast
LC-B: [&ast]
HLXL: &h_documents
LC-R: ⟁documents
LC-T: @documents
LC-B: [&documents]
HLXL: &h_model
LC-R: ⟁model
LC-T: @model
LC-B: [&model]
HLXL: &h_query
LC-R: ⟁query
LC-T: @query
LC-B: [&query]
HLXL: {1000: {@0: "search", @1: &h_documents}}
LC-R: 🜊1000🜁0 "search"🜁1 ⟁documents🜂
LC-T: {C:1000,0="search",1=@documents}
LC-B: [1000|0:"search"|1:&documents]
HLXL: {1000: {@0: "search", @1: &h_files, @2: "pattern"}}
LC-R: 🜊1000🜁0 "search"🜁1 ⟁files🜁2 "pattern"🜂
LC-T: {C:1000,0="search",1=@files,2="pattern"}
LC-B: [1000|0:"search"|1:&files|2:"pattern"]
HLXL: {1000: {@0: "search", @1: &h_database, @2: "users"}}
LC-R: 🜊1000🜁0 "search"🜁1 ⟁database🜁2 "users"🜂
LC-T: {C:1000,0="search",1=@database,2="users"}
LC-B: [1000|0:"search"|1:&database|2:"users"]
HLXL: {1000: {@0: "search", @1: &h_logs, @2: "error"}}
LC-R: 🜊1000🜁0 "search"🜁1 ⟁logs🜁2 "error"🜂
LC-T: {C:1000,0="search",1=@logs,2="error"}
LC-B: [1000|0:"search"|1:&logs|2:"error"]
HLXL: {1000: {@0: "search", @1: &h_cache}}
LC-R: 🜊1000🜁0 "search"🜁1 ⟁cache🜂
LC-T: {C:1000,0="search",1=@cache}
LC-B: [1000|0:"search"|1:&cache]
HLXL: {1000: {@0: "filter", @1: &h_users, @2: &h_active}}
LC-R: 🜊1000🜁0 "filter"🜁1 ⟁users🜁2 ⟁active🜂
LC-T: {C:1000,0="filter",1=@users,2=@active}
LC-B: [1000|0:"filter"|1:&users|2:&active]
HLXL: {1000: {@0: "filter", @1: &h_items, @2: &h_valid}}
LC-R: 🜊1000🜁0 "filter"🜁1 ⟁items🜁2 ⟁valid🜂
LC-T: {C:1000,0="filter",1=@items,2=@valid}
LC-B: [1000|0:"filter"|1:&items|2:&valid]
HLXL: {1000: {@0: "filter", @1: &h_records, @2: &h_status}}
LC-R: 🜊1000🜁0 "filter"🜁1 ⟁records🜁2 ⟁status🜂
LC-T: {C:1000,0="filter",1=@records,2=@status}
LC-B: [1000|0:"filter"|1:&records|2:&status]
HLXL: {1000: {@0: "filter", @1: &h_documents, @2: &h_recent}}
LC-R: 🜊1000🜁0 "filter"🜁1 ⟁documents🜁2 ⟁recent🜂
LC-T: {C:1000,0="filter",1=@documents,2=@recent}
LC-B: [1000|0:"filter"|1:&documents|2:&recent]
HLXL: {1000: {@0: "filter", @1: &h_features, @2: &h_enabled}}
LC-R: 🜊1000🜁0 "filter"🜁1 ⟁features🜁2 ⟁enabled🜂
LC-T: {C:1000,0="filter",1=@features,2=@enabled}
LC-B: [1000|0:"filter"|1:&features|2:&enabled]
HLXL: {1000: {@0: "transform", @1: &h_text, @2: &h_uppercase}}
LC-R: 🜊1000🜁0 "transform"🜁1 ⟁text🜁2 ⟁uppercase🜂
LC-T: {C:1000,0="transform",1=@text,2=@uppercase}
LC-B: [1000|0:"transform"|1:&text|2:&uppercase]
HLXL: {1000: {@0: "transform", @1: &h_data, @2: &h_json}}
LC-R: 🜊1000🜁0 "transform"🜁1 ⟁data🜁2 ⟁json🜂
LC-T: {C:1000,0="transform",1=@data,2=@json}
LC-B: [1000|0:"transform"|1:&data|2:&json]
HLXL: {1000: {@0: "transform", @1: &h_input, @2: &h_normalize}}
LC-R: 🜊1000🜁0 "transform"🜁1 ⟁input🜁2 ⟁normalize🜂
LC-T: {C:1000,0="transform",1=@input,2=@normalize}
LC-B: [1000|0:"transform"|1:&input|2:&normalize]
HLXL: {1000: {@0: "transform", @1: &h_value, @2: &h_base64}}
LC-R: 🜊1000🜁0 "transform"🜁1 ⟁value🜁2 ⟁base64🜂
LC-T: {C:1000,0="transform",1=@value,2=@base64}
LC-B: [1000|0:"transform"|1:&value|2:&base64]
HLXL: {1000: {@0: "transform", @1: &h_string, @2: &h_parseInt}}
LC-R: 🜊1000🜁0 "transform"🜁1 ⟁string🜁2 ⟁parseInt🜂
LC-T: {C:1000,0="transform",1=@string,2=@parseInt}
LC-B: [1000|0:"transform"|1:&string|2:&parseInt]
HLXL: {1000: {@0: "aggregate", @1: &h_sum, @2: &h_values}}
LC-R: 🜊1000🜁0 "aggregate"🜁1 ⟁sum🜁2 ⟁values🜂
LC-T: {C:1000,0="aggregate",1=@sum,2=@values}
LC-B: [1000|0:"aggregate"|1:&sum|2:&values]
HLXL: {1000: {@0: "aggregate", @1: &h_average, @2: &h_scores}}
LC-R: 🜊1000🜁0 "aggregate"🜁1 ⟁average🜁2 ⟁scores🜂
LC-T: {C:1000,0="aggregate",1=@average,2=@scores}
LC-B: [1000|0:"aggregate"|1:&average|2:&scores]
HLXL: {1000: {@0: "aggregate", @1: &h_max, @2: &h_value}}
LC-R: 🜊1000🜁0 "aggregate"🜁1 ⟁max🜁2 ⟁value🜂
LC-T: {C:1000,0="aggregate",1=@max,2=@value}
LC-B: [1000|0:"aggregate"|1:&max|2:&value]
HLXL: {1000: {@0: "aggregate", @1: &h_min, @2: &h_value}}
LC-R: 🜊1000🜁0 "aggregate"🜁1 ⟁min🜁2 ⟁value🜂
LC-T: {C:1000,0="aggregate",1=@min,2=@value}
LC-B: [1000|0:"aggregate"|1:&min|2:&value]
HLXL: {1000: {@0: "aggregate", @1: &h_count, @2: &h_items}}
LC-R: 🜊1000🜁0 "aggregate"🜁1 ⟁count🜁2 ⟁items🜂
LC-T: {C:1000,0="aggregate",1=@count,2=@items}
LC-B: [1000|0:"aggregate"|1:&count|2:&items]
HLXL: {1000: {@0: "read", @1: "database"}}
LC-R: 🜊1000🜁0 "read"🜁1 "database"🜂
LC-T: {C:1000,0="read",1="database"}
LC-B: [1000|0:"read"|1:"database"]
HLXL: {1000: {@0: "read", @1: "config.json"}}
LC-R: 🜊1000🜁0 "read"🜁1 "config.json"🜂
LC-T: {C:1000,0="read",1="config.json"}
LC-B: [1000|0:"read"|1:"config.json"]
HLXL: {1000: {@0: "write", @1: "output.txt", @2: &h_results}}
LC-R: 🜊1000🜁0 "write"🜁1 "output.txt"🜁2 ⟁results🜂
LC-T: {C:1000,0="write",1="output.txt",2=@results}
LC-B: [1000|0:"write"|1:"output.txt"|2:&results]
HLXL: {1000: {@0: "write", @1: "log.txt", @2: &h_data}}
LC-R: 🜊1000🜁0 "write"🜁1 "log.txt"🜁2 ⟁data🜂
LC-T: {C:1000,0="write",1="log.txt",2=@data}
LC-B: [1000|0:"write"|1:"log.txt"|2:&data]
HLXL: {1000: {@0: "write", @1: "cache", @2: &h_value}}
LC-R: 🜊1000🜁0 "write"🜁1 "cache"🜁2 ⟁value🜂
LC-T: {C:1000,0="write",1="cache",2=@value}
LC-B: [1000|0:"write"|1:"cache"|2:&value]
HLXL: {1000: {@0: "execute", @1: &h_command}}
LC-R: 🜊1000🜁0 "execute"🜁1 ⟁command🜂
LC-T: {C:1000,0="execute",1=@command}
LC-B: [1000|0:"execute"|1:&command]
HLXL: {1000: {@0: "execute", @1: &h_operation}}
LC-R: 🜊1000🜁0 "execute"🜁1 ⟁operation🜂
LC-T: {C:1000,0="execute",1=@operation}
LC-B: [1000|0:"execute"|1:&operation]
HLXL: {1000: {@0: "compute", @1: &h_result}}
LC-R: 🜊1000🜁0 "compute"🜁1 ⟁result🜂
LC-T: {C:1000,0="compute",1=@result}
LC-B: [1000|0:"compute"|1:&result]
HLXL: {1000: {@0: "validate", @1: &h_input, @2: &h_schema}}
LC-R: 🜊1000🜁0 "validate"🜁1 ⟁input🜁2 ⟁schema🜂
LC-T: {C:1000,0="validate",1=@input,2=@schema}
LC-B: [1000|0:"validate"|1:&input|2:&schema]
HLXL: {1000: {@0: "process", @1: &h_request}}
LC-R: 🜊1000🜁0 "process"🜁1 ⟁request🜂
LC-T: {C:1000,0="process",1=@request}
LC-B: [1000|0:"process"|1:&request]
HLXL: {1000: {@0: "navigate", @1: &h_home}}
LC-R: 🜊1000🜁0 "navigate"🜁1 ⟁home🜂
LC-T: {C:1000,0="navigate",1=@home}
LC-B: [1000|0:"navigate"|1:&home]
HLXL: {1000: {@0: "navigate", @1: &h_settings}}
LC-R: 🜊1000🜁0 "navigate"🜁1 ⟁settings🜂
LC-T: {C:1000,0="navigate",1=@settings}
LC-B: [1000|0:"navigate"|1:&settings]
HLXL: {1000: {@0: "navigate", @1: &h_dashboard}}
LC-R: 🜊1000🜁0 "navigate"🜁1 ⟁dashboard🜂
LC-T: {C:1000,0="navigate",1=@dashboard}
LC-B: [1000|0:"navigate"|1:&dashboard]
HLXL: {1000: {@0: "navigate", @1: &h_back}}
LC-R: 🜊1000🜁0 "navigate"🜁1 ⟁back🜂
LC-T: {C:1000,0="navigate",1=@back}
LC-B: [1000|0:"navigate"|1:&back]
HLXL: {1000: {@0: "navigate", @1: &h_forward}}
LC-R: 🜊1000🜁0 "navigate"🜁1 ⟁forward🜂
LC-T: {C:1000,0="navigate",1=@forward}
LC-B: [1000|0:"navigate"|1:&forward]
HLXL: {1000: {@0: "open", @1: &h_fileBrowser}}
LC-R: 🜊1000🜁0 "open"🜁1 ⟁fileBrowser🜂
LC-T: {C:1000,0="open",1=@fileBrowser}
LC-B: [1000|0:"open"|1:&fileBrowser]
HLXL: {1000: {@0: "open", @1: &h_terminal}}
LC-R: 🜊1000🜁0 "open"🜁1 ⟁terminal🜂
LC-T: {C:1000,0="open",1=@terminal}
LC-B: [1000|0:"open"|1:&terminal]
HLXL: {1000: {@0: "close", @1: &h_window}}
LC-R: 🜊1000🜁0 "close"🜁1 ⟁window🜂
LC-T: {C:1000,0="close",1=@window}
LC-B: [1000|0:"close"|1:&window]
HLXL: {1000: {@0: "refresh", @1: &h_page}}
LC-R: 🜊1000🜁0 "refresh"🜁1 ⟁page🜂
LC-T: {C:1000,0="refresh",1=@page}
LC-B: [1000|0:"refresh"|1:&page]
HLXL: {1000: {@0: "scroll", @1: &h_top}}
LC-R: 🜊1000🜁0 "scroll"🜁1 ⟁top🜂
LC-T: {C:1000,0="scroll",1=@top}
LC-B: [1000|0:"scroll"|1:&top]
HLXL: {1000: {@0: "scroll", @1: &h_down}}
LC-R: 🜊1000🜁0 "scroll"🜁1 ⟁down🜂
LC-T: {C:1000,0="scroll",1=@down}
LC-B: [1000|0:"scroll"|1:&down]
HLXL: {1000: {@0: "zoom", @1: &h_in}}
LC-R: 🜊1000🜁0 "zoom"🜁1 ⟁in🜂
LC-T: {C:1000,0="zoom",1=@in}
LC-B: [1000|0:"zoom"|1:&in]
HLXL: {1000: {@0: "zoom", @1: &h_out}}
LC-R: 🜊1000🜁0 "zoom"🜁1 ⟁out🜂
LC-T: {C:1000,0="zoom",1=@out}
LC-B: [1000|0:"zoom"|1:&out]
HLXL: {1000: {@0: "focus", @1: &h_input}}
LC-R: 🜊1000🜁0 "focus"🜁1 ⟁input🜂
LC-T: {C:1000,0="focus",1=@input}
LC-B: [1000|0:"focus"|1:&input]
HLXL: {1000: {@0: "select", @1: &h_all}}
LC-R: 🜊1000🜁0 "select"🜁1 ⟁all🜂
LC-T: {C:1000,0="select",1=@all}
LC-B: [1000|0:"select"|1:&all]
HLXL: {1000: {@0: "copy", @1: &h_selection}}
LC-R: 🜊1000🜁0 "copy"🜁1 ⟁selection🜂
LC-T: {C:1000,0="copy",1=@selection}
LC-B: [1000|0:"copy"|1:&selection]
HLXL: {1000: {@0: "paste", @1: &h_clipboard}}
LC-R: 🜊1000🜁0 "paste"🜁1 ⟁clipboard🜂
LC-T: {C:1000,0="paste",1=@clipboard}
LC-B: [1000|0:"paste"|1:&clipboard]
HLXL: {1000: {@0: "undo", @1: &h_last}}
LC-R: 🜊1000🜁0 "undo"🜁1 ⟁last🜂
LC-T: {C:1000,0="undo",1=@last}
LC-B: [1000|0:"undo"|1:&last]
HLXL: {1000: {@0: "redo", @1: &h_action}}
LC-R: 🜊1000🜁0 "redo"🜁1 ⟁action🜂
LC-T: {C:1000,0="redo",1=@action}
LC-B: [1000|0:"redo"|1:&action]
HLXL: {1000: {@0: "show", @1: &h_help}}
LC-R: 🜊1000🜁0 "show"🜁1 ⟁help🜂
LC-T: {C:1000,0="show",1=@help}
LC-B: [1000|0:"show"|1:&help]
HLXL: []
LC-R: 🜃🜄
LC-T: []
LC-B: [[]]
HLXL: [1, 2, 3]
LC-R: 🜃1, 2, 3🜄
LC-T: [1,2,3]
LC-B: [[0x01,0x02,0x03]]
HLXL: ["Alice", "Bob", "Carol"]
LC-R: 🜃"Alice", "Bob", "Carol"🜄
LC-T: ["Alice","Bob","Carol"]
LC-B: [["Alice","Bob","Carol"]]
HLXL: [&h_a, &h_b, &h_c]
LC-R: 🜃⟁a, ⟁b, ⟁c🜄
LC-T: [@a,@b,@c]
LC-B: [[&a,&b,&c]]
HLXL: [42, "test", true]
LC-R: 🜃42, "test", ⊤🜄
LC-T: [42,"test",TRUE]
LC-B: [[0x2a,"test",T]]
HLXL: [100, 200, 300]
LC-R: 🜃100, 200, 300🜄
LC-T: [100,200,300]
LC-B: [[0x64,0xc8,0x12c]]
HLXL: [0.1, 0.5, 0.9]
LC-R: 🜃0.1, 0.5, 0.9🜄
LC-T: [0.1,0.5,0.9]
LC-B: [[0.1,0.5,0.9]]
HLXL: [42]
LC-R: 🜃42🜄
LC-T: [42]
LC-B: [[0x2a]]
HLXL: {name: "Alice"}
LC-R: ◇name: "Alice"◆
LC-T: {name:"Alice"}
LC-B: [{name:"Alice"}]
HLXL: {x: 10, y: 20}
LC-R: ◇x: 10, y: 20◆
LC-T: {x:10,y:20}
LC-B: [{x:0x0a,y:0x14}]
HLXL: {name: "Alice", age: 30}
LC-R: ◇name: "Alice", age: 30◆
LC-T: {name:"Alice",age:30}
LC-B: [{name:"Alice",age:0x1e}]
HLXL: {debug: true, verbose: false}
LC-R: ◇debug: ⊤, verbose: ⊥◆
LC-T: {debug:TRUE,verbose:FALSE}
LC-B: [{debug:T,verbose:F}]
HLXL: {r: 255, g: 128, b: 64}
LC-R: ◇r: 255, g: 128, b: 64◆
LC-T: {r:255,g:128,b:64}
LC-B: [{r:0xff,g:0x80,b:0x40}]
HLXL: {width: 800, height: 600}
LC-R: ◇width: 800, height: 600◆
LC-T: {width:800,height:600}
LC-B: [{width:0x320,height:0x258}]
HLXL: {player: "Bob", score: 1500}
LC-R: ◇player: "Bob", score: 1500◆
LC-T: {player:"Bob",score:1500}
LC-B: [{player:"Bob",score:0x5dc}]
HLXL: {enabled: true, count: 5}
LC-R: ◇enabled: ⊤, count: 5◆
LC-T: {enabled:TRUE,count:5}
LC-B: [{enabled:T,count:0x05}]
HLXL: {}
LC-R: ◇◆
LC-T: {}
LC-B: [{}]
HLXL: {14: {@0: 42}}
LC-R: 🜊14🜁0 42🜂
LC-T: {C:14,0=42}
LC-B: [14|0:0x2a]
HLXL: {15: {@0: 3.14159}}
LC-R: 🜊15🜁0 3.14159🜂
LC-T: {C:15,0=3.14159}
LC-B: [15|0:3.14159]
HLXL: {16: {@0: "hello"}}
LC-R: 🜊16🜁0 "hello"🜂
LC-T: {C:16,0="hello"}
LC-B: [16|0:"hello"]
HLXL: {20: {@0: &h_model}}
LC-R: 🜊20🜁0 ⟁model🜂
LC-T: {C:20,0=@model}
LC-B: [20|0:&model]
HLXL: {21: {@0: null}}
LC-R: 🜊21🜁0 ∅🜂
LC-T: {C:21,0=NULL}
LC-B: [21|0:_]
HLXL: {22: {@0: true}}
LC-R: 🜊22🜁0 ⊤🜂
LC-T: {C:22,0=TRUE}
LC-B: [22|0:T]
HLXL: {22: {@0: false}}
LC-R: 🜊22🜁0 ⊥🜂
LC-T: {C:22,0=FALSE}
LC-B: [22|0:F]
HLXL: {1000: {@0: "copy", @1: &h_source, @2: &h_dest}}
LC-R: 🜊1000🜁0 "copy"🜁1 ⟁source🜁2 ⟁dest🜂
LC-T: {C:1000,0="copy",1=@source,2=@dest}
LC-B: [1000|0:"copy"|1:&source|2:&dest]
HLXL: {1000: {@0: "merge", @1: &h_datasetA, @2: &h_datasetB}}
LC-R: 🜊1000🜁0 "merge"🜁1 ⟁datasetA🜁2 ⟁datasetB🜂
LC-T: {C:1000,0="merge",1=@datasetA,2=@datasetB}
LC-B: [1000|0:"merge"|1:&datasetA|2:&datasetB]
HLXL: {1000: {@0: "join", @1: &h_users, @2: &h_orders}}
LC-R: 🜊1000🜁0 "join"🜁1 ⟁users🜁2 ⟁orders🜂
LC-T: {C:1000,0="join",1=@users,2=@orders}
LC-B: [1000|0:"join"|1:&users|2:&orders]
HLXL: {1000: {@0: "sort", @1: &h_items, @2: &h_score, @3: &h_desc}}
LC-R: 🜊1000🜁0 "sort"🜁1 ⟁items🜁2 ⟁score🜁3 ⟁desc🜂
LC-T: {C:1000,0="sort",1=@items,2=@score,3=@desc}
LC-B: [1000|0:"sort"|1:&items|2:&score|3:&desc]
HLXL: {1000: {@0: "group", @1: &h_records, @2: &h_category}}
LC-R: 🜊1000🜁0 "group"🜁1 ⟁records🜁2 ⟁category🜂
LC-T: {C:1000,0="group",1=@records,2=@category}
LC-B: [1000|0:"group"|1:&records|2:&category]
HLXL: {1000: {@0: "limit", @1: &h_results, @2: 10}}
LC-R: 🜊1000🜁0 "limit"🜁1 ⟁results🜁2 10🜂
LC-T: {C:1000,0="limit",1=@results,2=10}
LC-B: [1000|0:"limit"|1:&results|2:0x0a]
HLXL: {1000: {@0: "skip", @1: &h_items, @2: 5}}
LC-R: 🜊1000🜁0 "skip"🜁1 ⟁items🜁2 5🜂
LC-T: {C:1000,0="skip",1=@items,2=5}
LC-B: [1000|0:"skip"|1:&items|2:0x05]
HLXL: {1000: {@0: "map", @1: &h_function, @2: &h_array}}
LC-R: 🜊1000🜁0 "map"🜁1 ⟁function🜁2 ⟁array🜂
LC-T: {C:1000,0="map",1=@function,2=@array}
LC-B: [1000|0:"map"|1:&function|2:&array]
HLXL: {1000: {@0: "reduce", @1: &h_array, @2: &h_accumulator}}
LC-R: 🜊1000🜁0 "reduce"🜁1 ⟁array🜁2 ⟁accumulator🜂
LC-T: {C:1000,0="reduce",1=@array,2=@accumulator}
LC-B: [1000|0:"reduce"|1:&array|2:&accumulator]
HLXL: {1000: {@0: "flatten", @1: &h_nested}}
LC-R: 🜊1000🜁0 "flatten"🜁1 ⟁nested🜂
LC-T: {C:1000,0="flatten",1=@nested}
LC-B: [1000|0:"flatten"|1:&nested]
HLXL: {1000: {@0: "reverse", @1: &h_list}}
LC-R: 🜊1000🜁0 "reverse"🜁1 ⟁list🜂
LC-T: {C:1000,0="reverse",1=@list}
LC-B: [1000|0:"reverse"|1:&list]
HLXL: {1000: {@0: "unique", @1: &h_collection}}
LC-R: 🜊1000🜁0 "unique"🜁1 ⟁collection🜂
LC-T: {C:1000,0="unique",1=@collection}
LC-B: [1000|0:"unique"|1:&collection]
HLXL: {1000: {@0: "split", @1: &h_string, @2: ","}}
LC-R: 🜊1000🜁0 "split"🜁1 ⟁string🜁2 ","🜂
LC-T: {C:1000,0="split",1=@string,2=","}
LC-B: [1000|0:"split"|1:&string|2:","]
HLXL: {1000: {@0: "concat", @1: &h_strings}}
LC-R: 🜊1000🜁0 "concat"🜁1 ⟁strings🜂
LC-T: {C:1000,0="concat",1=@strings}
LC-B: [1000|0:"concat"|1:&strings]
HLXL: {1000: {@0: "replace", @1: &h_text, @2: &h_old, @3: &h_new}}
LC-R: 🜊1000🜁0 "replace"🜁1 ⟁text🜁2 ⟁old🜁3 ⟁new🜂
LC-T: {C:1000,0="replace",1=@text,2=@old,3=@new}
LC-B: [1000|0:"replace"|1:&text|2:&old|3:&new]
HLXL: {1000: {@0: "trim", @1: &h_string}}
LC-R: 🜊1000🜁0 "trim"🜁1 ⟁string🜂
LC-T: {C:1000,0="trim",1=@string}
LC-B: [1000|0:"trim"|1:&string]
HLXL: {1000: {@0: "contains", @1: &h_collection, @2: &h_value}}
LC-R: 🜊1000🜁0 "contains"🜁1 ⟁collection🜁2 ⟁value🜂
LC-T: {C:1000,0="contains",1=@collection,2=@value}
LC-B: [1000|0:"contains"|1:&collection|2:&value]
HLXL: {1000: {@0: "length", @1: &h_array}}
LC-R: 🜊1000🜁0 "length"🜁1 ⟁array🜂
LC-T: {C:1000,0="length",1=@array}
LC-B: [1000|0:"length"|1:&array]
HLXL: {1000: {@0: "get", @1: &h_array, @2: 5}}
LC-R: 🜊1000🜁0 "get"🜁1 ⟁array🜁2 5🜂
LC-T: {C:1000,0="get",1=@array,2=5}
LC-B: [1000|0:"get"|1:&array|2:0x05]
HLXL: {1000: {@0: "set", @1: &h_array, @2: 3, @3: &h_value}}
LC-R: 🜊1000🜁0 "set"🜁1 ⟁array🜁2 3🜁3 ⟁value🜂
LC-T: {C:1000,0="set",1=@array,2=3,3=@value}
LC-B: [1000|0:"set"|1:&array|2:0x03|3:&value]
HLXL: {1000: {@0: "append", @1: &h_list, @2: &h_value}}
LC-R: 🜊1000🜁0 "append"🜁1 ⟁list🜁2 ⟁value🜂
LC-T: {C:1000,0="append",1=@list,2=@value}
LC-B: [1000|0:"append"|1:&list|2:&value]
HLXL: {1000: {@0: "remove", @1: &h_collection, @2: &h_element}}
LC-R: 🜊1000🜁0 "remove"🜁1 ⟁collection🜁2 ⟁element🜂
LC-T: {C:1000,0="remove",1=@collection,2=@element}
LC-B: [1000|0:"remove"|1:&collection|2:&element]
HLXL: {1000: {@0: "clear", @1: &h_items}}
LC-R: 🜊1000🜁0 "clear"🜁1 ⟁items🜂
LC-T: {C:1000,0="clear",1=@items}
LC-B: [1000|0:"clear"|1:&items]
HLXL: {1000: {@0: "delete", @1: &h_record, @2: &h_id}}
LC-R: 🜊1000🜁0 "delete"🜁1 ⟁record🜁2 ⟁id🜂
LC-T: {C:1000,0="delete",1=@record,2=@id}
LC-B: [1000|0:"delete"|1:&record|2:&id]
HLXL: {1000: {@0: "update", @1: &h_object, @2: &h_field, @3: &h_value}}
LC-R: 🜊1000🜁0 "update"🜁1 ⟁object🜁2 ⟁field🜁3 ⟁value🜂
LC-T: {C:1000,0="update",1=@object,2=@field,3=@value}
LC-B: [1000|0:"update"|1:&object|2:&field|3:&value]
HLXL: {900: {@0: &h_spirv, @1: "main", @2: "compute"}}
LC-R: 🜊900🜁0 ⟁spirv🜁1 "main"🜁2 "compute"🜂
LC-T: {C:900,0=@spirv,1="main",2="compute"}
LC-B: [900|0:&spirv|1:"main"|2:"compute"]
HLXL: {900: {@0: &h_vertex, @1: "vs_main", @2: "vertex"}}
LC-R: 🜊900🜁0 ⟁vertex🜁1 "vs_main"🜁2 "vertex"🜂
LC-T: {C:900,0=@vertex,1="vs_main",2="vertex"}
LC-B: [900|0:&vertex|1:"vs_main"|2:"vertex"]
HLXL: {900: {@0: &h_fragment, @1: "fs_main", @2: "fragment"}}
LC-R: 🜊900🜁0 ⟁fragment🜁1 "fs_main"🜁2 "fragment"🜂
LC-T: {C:900,0=@fragment,1="fs_main",2="fragment"}
LC-B: [900|0:&fragment|1:"fs_main"|2:"fragment"]
HLXL: {901: {@0: "map", @1: &h_shader}}
LC-R: 🜊901🜁0 "map"🜁1 ⟁shader🜂
LC-T: {C:901,0="map",1=@shader}
LC-B: [901|0:"map"|1:&shader]
HLXL: {901: {@0: "reduce", @1: &h_kernel}}
LC-R: 🜊901🜁0 "reduce"🜁1 ⟁kernel🜂
LC-T: {C:901,0="reduce",1=@kernel}
LC-B: [901|0:"reduce"|1:&kernel]
HLXL: {901: {@0: "scan", @1: &h_compute}}
LC-R: 🜊901🜁0 "scan"🜁1 ⟁compute🜂
LC-T: {C:901,0="scan",1=@compute}
LC-B: [901|0:"scan"|1:&compute]
HLXL: {902: {@0: "render_pipeline", @1: [&h_vs, &h_fs]}}
LC-R: 🜊902🜁0 "render_pipeline"🜁1 🜃⟁vs, ⟁fs🜄🜂
LC-T: {C:902,0="render_pipeline",1=[@vs,@fs]}
LC-B: [902|0:"render_pipeline"|1:[&vs,&fs]]
HLXL: {902: {@0: "compute_pipeline", @1: [&h_kernel]}}
LC-R: 🜊902🜁0 "compute_pipeline"🜁1 🜃⟁kernel🜄🜂
LC-T: {C:902,0="compute_pipeline",1=[@kernel]}
LC-B: [902|0:"compute_pipeline"|1:[&kernel]]
HLXL: {1000: {@0: "dispatch", @1: &h_pipeline, @2: [64, 64, 1]}}
LC-R: 🜊1000🜁0 "dispatch"🜁1 ⟁pipeline🜁2 🜃64, 64, 1🜄🜂
LC-T: {C:1000,0="dispatch",1=@pipeline,2=[64,64,1]}
LC-B: [1000|0:"dispatch"|1:&pipeline|2:[0x40,0x40,0x01]]
HLXL: {1000: {@0: "bind", @1: &h_buffer, @2: 0}}
LC-R: 🜊1000🜁0 "bind"🜁1 ⟁buffer🜁2 0🜂
LC-T: {C:1000,0="bind",1=@buffer,2=0}
LC-B: [1000|0:"bind"|1:&buffer|2:0x00]
HLXL: {1000: {@0: "upload", @1: &h_data, @2: &h_gpuBuffer}}
LC-R: 🜊1000🜁0 "upload"🜁1 ⟁data🜁2 ⟁gpuBuffer🜂
LC-T: {C:1000,0="upload",1=@data,2=@gpuBuffer}
LC-B: [1000|0:"upload"|1:&data|2:&gpuBuffer]
HLXL: {1000: {@0: "download", @1: &h_gpuBuffer, @2: &h_output}}
LC-R: 🜊1000🜁0 "download"🜁1 ⟁gpuBuffer🜁2 ⟁output🜂
LC-T: {C:1000,0="download",1=@gpuBuffer,2=@output}
LC-B: [1000|0:"download"|1:&gpuBuffer|2:&output]
HLXL: {1000: {@0: "sync", @1: &h_device}}
LC-R: 🜊1000🜁0 "sync"🜁1 ⟁device🜂
LC-T: {C:1000,0="sync",1=@device}
LC-B: [1000|0:"sync"|1:&device]
HLXL: {1000: {@0: "render", @1: &h_scene, @2: &h_target}}
LC-R: 🜊1000🜁0 "render"🜁1 ⟁scene🜁2 ⟁target🜂
LC-T: {C:1000,0="render",1=@scene,2=@target}
LC-B: [1000|0:"render"|1:&scene|2:&target]
HLXL: {1000: {@0: "present", @1: &h_swapchain}}
LC-R: 🜊1000🜁0 "present"🜁1 ⟁swapchain🜂
LC-T: {C:1000,0="present",1=@swapchain}
LC-B: [1000|0:"present"|1:&swapchain]
HLXL: {1000: {@0: "train", @1: &h_model, @2: &h_data}}
LC-R: 🜊1000🜁0 "train"🜁1 ⟁model🜁2 ⟁data🜂
LC-T: {C:1000,0="train",1=@model,2=@data}
LC-B: [1000|0:"train"|1:&model|2:&data]
HLXL: {1000: {@0: "infer", @1: &h_model, @2: &h_input}}
LC-R: 🜊1000🜁0 "infer"🜁1 ⟁model🜁2 ⟁input🜂
LC-T: {C:1000,0="infer",1=@model,2=@input}
LC-B: [1000|0:"infer"|1:&model|2:&input]
HLXL: {1000: {@0: "evaluate", @1: &h_model, @2: &h_testData}}
LC-R: 🜊1000🜁0 "evaluate"🜁1 ⟁model🜁2 ⟁testData🜂
LC-T: {C:1000,0="evaluate",1=@model,2=@testData}
LC-B: [1000|0:"evaluate"|1:&model|2:&testData]
HLXL: {1000: {@0: "save", @1: &h_model, @2: "checkpoint.pt"}}
LC-R: 🜊1000🜁0 "save"🜁1 ⟁model🜁2 "checkpoint.pt"🜂
LC-T: {C:1000,0="save",1=@model,2="checkpoint.pt"}
LC-B: [1000|0:"save"|1:&model|2:"checkpoint.pt"]
HLXL: {1000: {@0: "load", @1: &h_model, @2: "weights.pt"}}
LC-R: 🜊1000🜁0 "load"🜁1 ⟁model🜁2 "weights.pt"🜂
LC-T: {C:1000,0="load",1=@model,2="weights.pt"}
LC-B: [1000|0:"load"|1:&model|2:"weights.pt"]
HLXL: {1000: {@0: "forward", @1: &h_network, @2: &h_batch}}
LC-R: 🜊1000🜁0 "forward"🜁1 ⟁network🜁2 ⟁batch🜂
LC-T: {C:1000,0="forward",1=@network,2=@batch}
LC-B: [1000|0:"forward"|1:&network|2:&batch]
HLXL: {1000: {@0: "backward", @1: &h_loss}}
LC-R: 🜊1000🜁0 "backward"🜁1 ⟁loss🜂
LC-T: {C:1000,0="backward",1=@loss}
LC-B: [1000|0:"backward"|1:&loss]
HLXL: {1000: {@0: "optimize", @1: &h_optimizer, @2: &h_gradients}}
LC-R: 🜊1000🜁0 "optimize"🜁1 ⟁optimizer🜁2 ⟁gradients🜂
LC-T: {C:1000,0="optimize",1=@optimizer,2=@gradients}
LC-B: [1000|0:"optimize"|1:&optimizer|2:&gradients]
HLXL: {1000: {@0: "embed", @1: &h_text, @2: &h_embedder}}
LC-R: 🜊1000🜁0 "embed"🜁1 ⟁text🜁2 ⟁embedder🜂
LC-T: {C:1000,0="embed",1=@text,2=@embedder}
LC-B: [1000|0:"embed"|1:&text|2:&embedder]
HLXL: {1000: {@0: "tokenize", @1: &h_text, @2: &h_tokenizer}}
LC-R: 🜊1000🜁0 "tokenize"🜁1 ⟁text🜁2 ⟁tokenizer🜂
LC-T: {C:1000,0="tokenize",1=@text,2=@tokenizer}
LC-B: [1000|0:"tokenize"|1:&text|2:&tokenizer]
HLXL: {1000: {@0: "decode", @1: &h_tokens, @2: &h_tokenizer}}
LC-R: 🜊1000🜁0 "decode"🜁1 ⟁tokens🜁2 ⟁tokenizer🜂
LC-T: {C:1000,0="decode",1=@tokens,2=@tokenizer}
LC-B: [1000|0:"decode"|1:&tokens|2:&tokenizer]
HLXL: {1000: {@0: "generate", @1: &h_model, @2: &h_prompt}}
LC-R: 🜊1000🜁0 "generate"🜁1 ⟁model🜁2 ⟁prompt🜂
LC-T: {C:1000,0="generate",1=@model,2=@prompt}
LC-B: [1000|0:"generate"|1:&model|2:&prompt]
HLXL: {1000: {@0: "sample", @1: &h_distribution, @2: &h_temperature}}
LC-R: 🜊1000🜁0 "sample"🜁1 ⟁distribution🜁2 ⟁temperature🜂
LC-T: {C:1000,0="sample",1=@distribution,2=@temperature}
LC-B: [1000|0:"sample"|1:&distribution|2:&temperature]
HLXL: {1000: {@0: "batch", @1: &h_inputs, @2: 32}}
LC-R: 🜊1000🜁0 "batch"🜁1 ⟁inputs🜁2 32🜂
LC-T: {C:1000,0="batch",1=@inputs,2=32}
LC-B: [1000|0:"batch"|1:&inputs|2:0x20]
HLXL: {1000: {@0: "collate", @1: &h_samples}}
LC-R: 🜊1000🜁0 "collate"🜁1 ⟁samples🜂
LC-T: {C:1000,0="collate",1=@samples}
LC-B: [1000|0:"collate"|1:&samples]
HLXL: {100: {@0: "main", @1: []}}
LC-R: 🜊100🜁0 "main"🜁1 🜃🜄🜂
LC-T: {C:100,0="main",1=[]}
LC-B: [100|0:"main"|1:[]]
HLXL: {101: {@0: "add", @1: 1, @2: 2}}
LC-R: 🜊101🜁0 "add"🜁1 1🜁2 2🜂
LC-T: {C:101,0="add",1=1,2=2}
LC-B: [101|0:"add"|1:0x01|2:0x02]
HLXL: {101: {@0: "multiply", @1: 5, @2: 10}}
LC-R: 🜊101🜁0 "multiply"🜁1 5🜁2 10🜂
LC-T: {C:101,0="multiply",1=5,2=10}
LC-B: [101|0:"multiply"|1:0x05|2:0x0a]
HLXL: {102: {@0: "x"}}
LC-R: 🜊102🜁0 "x"🜂
LC-T: {C:102,0="x"}
LC-B: [102|0:"x"]
HLXL: {102: {@0: "result"}}
LC-R: 🜊102🜁0 "result"🜂
LC-T: {C:102,0="result"}
LC-B: [102|0:"result"]
HLXL: {103: {@0: "x", @1: 42}}
LC-R: 🜊103🜁0 "x"🜁1 42🜂
LC-T: {C:103,0="x",1=42}
LC-B: [103|0:"x"|1:0x2a]
HLXL: {103: {@0: "name", @1: "Alice"}}
LC-R: 🜊103🜁0 "name"🜁1 "Alice"🜂
LC-T: {C:103,0="name",1="Alice"}
LC-B: [103|0:"name"|1:"Alice"]
HLXL: {103: {@0: "flag", @1: true}}
LC-R: 🜊103🜁0 "flag"🜁1 ⊤🜂
LC-T: {C:103,0="flag",1=TRUE}
LC-B: [103|0:"flag"|1:T]
HLXL: {104: {@0: "add", @1: ["a", "b"], @2: &h_body}}
LC-R: 🜊104🜁0 "add"🜁1 🜃"a", "b"🜄🜁2 ⟁body🜂
LC-T: {C:104,0="add",1=["a","b"],2=@body}
LC-B: [104|0:"add"|1:["a","b"]|2:&body]
HLXL: {104: {@0: "square", @1: ["x"], @2: &h_impl}}
LC-R: 🜊104🜁0 "square"🜁1 🜃"x"🜄🜁2 ⟁impl🜂
LC-T: {C:104,0="square",1=["x"],2=@impl}
LC-B: [104|0:"square"|1:["x"]|2:&impl]
HLXL: {105: {@0: "print", @1: ["hello"]}}
LC-R: 🜊105🜁0 "print"🜁1 🜃"hello"🜄🜂
LC-T: {C:105,0="print",1=["hello"]}
LC-B: [105|0:"print"|1:["hello"]]
HLXL: {105: {@0: "add", @1: [1, 2]}}
LC-R: 🜊105🜁0 "add"🜁1 🜃1, 2🜄🜂
LC-T: {C:105,0="add",1=[1,2]}
LC-B: [105|0:"add"|1:[0x01,0x02]]
HLXL: {105: {@0: "max", @1: [10, 20, 30]}}
LC-R: 🜊105🜁0 "max"🜁1 🜃10, 20, 30🜄🜂
LC-T: {C:105,0="max",1=[10,20,30]}
LC-B: [105|0:"max"|1:[0x0a,0x14,0x1e]]
HLXL: {106: {@0: true, @1: &h_a, @2: &h_b}}
LC-R: 🜊106🜁0 ⊤🜁1 ⟁a🜁2 ⟁b🜂
LC-T: {C:106,0=TRUE,1=@a,2=@b}
LC-B: [106|0:T|1:&a|2:&b]
HLXL: {107: {@0: &h_condition, @1: &h_body}}
LC-R: 🜊107🜁0 ⟁condition🜁1 ⟁body🜂
LC-T: {C:107,0=@condition,1=@body}
LC-B: [107|0:&condition|1:&body]

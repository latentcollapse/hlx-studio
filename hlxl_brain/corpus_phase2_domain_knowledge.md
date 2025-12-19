# Phase 2: Domain Knowledge Corpus

Total examples: 91

**Coverage:**
- File system operations (paths, wildcards, file ops)
- Data structures (lists, maps, sets, conversions)
- Control flow (conditionals, loops, pipelines, error handling)
- Common patterns (map-reduce, ETL, parallel processing)
- Realistic workflows (multi-step operations)

---

English: Get union of set1 and set2
LC-R: 🜊1000🜁0 "union"🜁1 ⟁set1🜁2 ⟁set2🜂

English: Go to /root/system
LC-R: 🜊1000🜁0 "navigate"🜁1 "/root/system"🜂

English: Prepend value to list
LC-R: 🜊1000🜁0 "prepend"🜁1 ⟁list🜁2 ⟁value🜂

English: Go to /home/user/docs
LC-R: 🜊1000🜁0 "navigate"🜁1 "/home/user/docs"🜂

English: Load data then filter then save
LC-R: 🜊1000🜁0 "pipeline"🜁1 🜊14🜁0 🜊1000🜁0 "load"🜁1 "data.json"🜂🜁1 🜊1000🜁0 "filter"🜁1 ⟁data🜁2 ⟁valid🜂🜁2 🜊1000🜁0 "save"🜁1 "output.json"🜁2 ⟁result🜂🜂🜂

English: If x greater than 10 then process
LC-R: 🜊1000🜁0 "if"🜁1 🜊1000🜁0 "gt"🜁1 ⟁x🜁2 10🜂🜁2 🜊1000🜁0 "process"🜂🜂

English: Find **/*.py
LC-R: 🜊1000🜁0 "find"🜁1 "**/*.py"🜂

English: Locate files a.csv, b.csv, c.csv
LC-R: 🜊1000🜁0 "find"🜁1 "{a,b,c}.csv"🜂

English: Get last element from list
LC-R: 🜊1000🜁0 "get"🜁1 ⟁list🜁2 -1🜂

English: Rename draft.md to final.md
LC-R: 🜊1000🜁0 "rename"🜁1 "draft.md"🜁2 "final.md"🜂

English: Reverse the list
LC-R: 🜊1000🜁0 "reverse"🜁1 ⟁list🜂

English: Create empty map
LC-R: 🜊15🜂

English: If valid then accept else reject
LC-R: 🜊1000🜁0 "if"🜁1 ⟁valid🜁2 🜊1000🜁0 "accept"🜂🜁3 🜊1000🜁0 "reject"🜂🜂

English: Search for data/*.json
LC-R: 🜊1000🜁0 "find"🜁1 "data/*.json"🜂

English: Get intersection of set1 and set2
LC-R: 🜊1000🜁0 "intersection"🜁1 ⟁set1🜁2 ⟁set2🜂

English: Create set from values a, b, c
LC-R: 🜊1000🜁0 "set"🜁1 🜊14🜁0 ⟁a🜁1 ⟁b🜁2 ⟁c🜂🜂

English: Convert set to list
LC-R: 🜊1000🜁0 "to_list"🜁1 ⟁set🜂

English: While condition do action
LC-R: 🜊1000🜁0 "while"🜁1 ⟁condition🜁2 🜊1000🜁0 "action"🜂🜂

English: Remove key from map
LC-R: 🜊1000🜁0 "remove"🜁1 ⟁map🜁2 "key"🜂

English: Add element to set
LC-R: 🜊1000🜁0 "add"🜁1 ⟁set🜁2 ⟁element🜂

English: Set key to value in map
LC-R: 🜊1000🜁0 "set"🜁1 ⟁map🜁2 "key"🜁3 ⟁value🜂

English: Extract data from API, transform to schema, load into database
LC-R: 🜊1000🜁0 "pipeline"🜁1 🜊14🜁0 🜊1000🜁0 "fetch"🜁1 "https://api.example.com/data"🜂🜁1 🜊1000🜁0 "transform"🜁1 ⟁data🜁2 ⟁to_schema🜂🜁2 🜊1000🜁0 "insert"🜁1 ⟁database🜁2 ⟁transformed🜂🜂🜂

English: Try operation catch error
LC-R: 🜊1000🜁0 "try"🜁1 🜊1000🜁0 "operation"🜂🜁2 🜊1000🜁0 "catch"🜁1 ⟁error🜂🜂

English: Convert string to number
LC-R: 🜊1000🜁0 "to_number"🜁1 "42"🜂

English: Create directory logs
LC-R: 🜊1000🜁0 "mkdir"🜁1 "logs"🜂

English: Change to ../parent/folder
LC-R: 🜊1000🜁0 "navigate"🜁1 "../parent/folder"🜂

English: Create empty list
LC-R: 🜊14🜂

English: Iterate from 0 to 10
LC-R: 🜊1000🜁0 "iterate"🜁1 0🜁2 10🜁3 🜊1000🜁0 "process"🜁1 ⟁i🜂🜂

English: Move temp.log to archive.log
LC-R: 🜊1000🜁0 "move"🜁1 "temp.log"🜁2 "archive.log"🜂

English: Get length of list
LC-R: 🜊1000🜁0 "length"🜁1 ⟁list🜂

English: Convert list to set
LC-R: 🜊1000🜁0 "to_set"🜁1 ⟁list🜂

English: Append value to list
LC-R: 🜊1000🜁0 "append"🜁1 ⟁list🜁2 ⟁value🜂

English: Get first element from list
LC-R: 🜊1000🜁0 "get"🜁1 ⟁list🜁2 0🜂

English: Authenticate with API, fetch user data, enrich with profile, cache results
LC-R: 🜊1000🜁0 "pipeline"🜁1 🜊14🜁0 🜊1000🜁0 "authenticate"🜁1 "api.example.com"🜁2 ⟁credentials🜂🜁1 🜊1000🜁0 "fetch"🜁1 "/users"🜁2 ⟁token🜂🜁2 🜊1000🜁0 "enrich"🜁1 ⟁users🜁2 ⟁get_profile🜂🜁3 🜊1000🜁0 "cache"🜁1 ⟁enriched🜁2 3600🜂🜂🜂

English: Sort the list
LC-R: 🜊1000🜁0 "sort"🜁1 ⟁list🜂

English: Execute with timeout
LC-R: 🜊1000🜁0 "timeout"🜁1 🜊1000🜁0 "execute"🜁1 ⟁task🜂🜁2 5000🜂

English: Find *.txt
LC-R: 🜊1000🜁0 "find"🜁1 "*.txt"🜂

English: Remove empty directory cache
LC-R: 🜊1000🜁0 "rmdir"🜁1 "cache"🜂

English: Locate test JavaScript files
LC-R: 🜊1000🜁0 "find"🜁1 "test_*.js"🜂

English: Find data/*.json
LC-R: 🜊1000🜁0 "find"🜁1 "data/*.json"🜂

English: If condition then action
LC-R: 🜊1000🜁0 "if"🜁1 ⟁condition🜁2 🜊1000🜁0 "action"🜂🜂

English: Match value with cases
LC-R: 🜊1000🜁0 "match"🜁1 ⟁value🜁2 🜊15🜁0 "case1"🜁1 🜊1000🜁0 "action1"🜂🜁2 "case2"🜁3 🜊1000🜁0 "action2"🜂🜂🜂

English: Get all keys from map
LC-R: 🜊1000🜁0 "keys"🜁1 ⟁map🜂

English: Go to ../parent/folder
LC-R: 🜊1000🜁0 "navigate"🜁1 "../parent/folder"🜂

English: List files in current directory
LC-R: 🜊1000🜁0 "ls"🜁1 "."🜂

English: Read, transform, validate, write
LC-R: 🜊1000🜁0 "pipeline"🜁1 🜊14🜁0 🜊1000🜁0 "read"🜁1 "input.txt"🜂🜁1 🜊1000🜁0 "transform"🜁1 ⟁data🜁2 ⟁normalize🜂🜁2 🜊1000🜁0 "validate"🜁1 ⟁result🜁2 ⟁schema🜂🜁3 🜊1000🜁0 "write"🜁1 "output.txt"🜁2 ⟁validated🜂🜂🜂

English: Change to /home/user/docs
LC-R: 🜊1000🜁0 "navigate"🜁1 "/home/user/docs"🜂

English: Search for **/*.py
LC-R: 🜊1000🜁0 "find"🜁1 "**/*.py"🜂

English: Create list with values 1, 2, 3
LC-R: 🜊14🜁0 1🜁1 2🜁2 3🜂

English: Check if map has key
LC-R: 🜊1000🜁0 "has"🜁1 ⟁map🜁2 "key"🜂

English: Search for test_*.js
LC-R: 🜊1000🜁0 "find"🜁1 "test_*.js"🜂

English: Map transform over list then reduce with sum
LC-R: 🜊1000🜁0 "pipeline"🜁1 🜊14🜁0 🜊1000🜁0 "map"🜁1 ⟁list🜁2 🜊1000🜁0 "transform"🜁1 ⟁item🜂🜂🜁1 🜊1000🜁0 "reduce"🜁1 ⟁mapped🜁2 🜊1000🜁0 "sum"🜂🜂🜂

English: Find {a,b,c}.csv
LC-R: 🜊1000🜁0 "find"🜁1 "{a,b,c}.csv"🜂

English: Change to ./relative/path
LC-R: 🜊1000🜁0 "navigate"🜁1 "./relative/path"🜂

English: Navigate to ../parent/folder
LC-R: 🜊1000🜁0 "navigate"🜁1 "../parent/folder"🜂

English: Get difference of set1 and set2
LC-R: 🜊1000🜁0 "difference"🜁1 ⟁set1🜁2 ⟁set2🜂

English: Get value for key from map
LC-R: 🜊1000🜁0 "get"🜁1 ⟁map🜁2 "key"🜂

English: Process items in parallel with 4 workers
LC-R: 🜊1000🜁0 "parallel"🜁1 ⟁items🜁2 🜊1000🜁0 "process"🜁1 ⟁item🜂🜁3 4🜂

English: Navigate to /root/system
LC-R: 🜊1000🜁0 "navigate"🜁1 "/root/system"🜂

English: Execute with cache for 3600 seconds
LC-R: 🜊1000🜁0 "cache"🜁1 🜊1000🜁0 "execute"🜁1 ⟁task🜂🜁2 3600🜂

English: Find test_*.js
LC-R: 🜊1000🜁0 "find"🜁1 "test_*.js"🜂

English: Filter valid items, map to values, sum results
LC-R: 🜊1000🜁0 "pipeline"🜁1 🜊14🜁0 🜊1000🜁0 "filter"🜁1 ⟁items🜁2 ⟁valid🜂🜁1 🜊1000🜁0 "map"🜁1 ⟁filtered🜁2 ⟁get_value🜂🜁2 🜊1000🜁0 "sum"🜁1 ⟁values🜂🜂🜂

English: Slice list from index 1 to 5
LC-R: 🜊1000🜁0 "slice"🜁1 ⟁list🜁2 1🜁3 5🜂

English: Locate JSON files in data folder
LC-R: 🜊1000🜁0 "find"🜁1 "data/*.json"🜂

English: Navigate to /home/user/docs
LC-R: 🜊1000🜁0 "navigate"🜁1 "/home/user/docs"🜂

English: Find all log files, parse errors, group by type, generate report
LC-R: 🜊1000🜁0 "pipeline"🜁1 🜊14🜁0 🜊1000🜁0 "find"🜁1 "**/*.log"🜂🜁1 🜊1000🜁0 "map"🜁1 ⟁files🜁2 🜊1000🜁0 "parse_errors"🜁1 ⟁file🜂🜂🜁2 🜊1000🜁0 "group_by"🜁1 ⟁errors🜁2 "type"🜂🜁3 🜊1000🜁0 "generate_report"🜁1 ⟁grouped🜂🜂🜂

English: Check if set contains element
LC-R: 🜊1000🜁0 "contains"🜁1 ⟁set🜁2 ⟁element🜂

English: Process items in batches of 100
LC-R: 🜊1000🜁0 "batch"🜁1 ⟁items🜁2 100🜁3 🜊1000🜁0 "process"🜁1 ⟁batch🜂🜂

English: Get all values from map
LC-R: 🜊1000🜁0 "values"🜁1 ⟁map🜂

English: Query database, transform records, export to multiple formats
LC-R: 🜊1000🜁0 "pipeline"🜁1 🜊14🜁0 🜊1000🜁0 "query"🜁1 ⟁database🜁2 "SELECT * FROM users"🜂🜁1 🜊1000🜁0 "transform"🜁1 ⟁records🜁2 ⟁normalize🜂🜁2 🜊1000🜁0 "export"🜁1 ⟁transformed🜁2 🜊14🜁0 "json"🜁1 "csv"🜁2 "xml"🜂🜂🜂🜂

English: Search for {a,b,c}.csv
LC-R: 🜊1000🜁0 "find"🜁1 "{a,b,c}.csv"🜂

English: Repeat action 5 times
LC-R: 🜊1000🜁0 "repeat"🜁1 5🜁2 🜊1000🜁0 "action"🜂🜂

English: Validate input or use default
LC-R: 🜊1000🜁0 "or"🜁1 🜊1000🜁0 "validate"🜁1 ⟁input🜂🜁2 ⟁default🜂

English: Convert number to string
LC-R: 🜊1000🜁0 "to_string"🜁1 42🜂

English: Copy file.txt to backup.txt
LC-R: 🜊1000🜁0 "copy"🜁1 "file.txt"🜁2 "backup.txt"🜂

English: Read config.yaml
LC-R: 🜊1000🜁0 "read"🜁1 "config.yaml"🜂

English: Read config, validate schema, check permissions, apply settings
LC-R: 🜊1000🜁0 "pipeline"🜁1 🜊14🜁0 🜊1000🜁0 "read"🜁1 "config.yaml"🜂🜁1 🜊1000🜁0 "validate"🜁1 ⟁config🜁2 ⟁schema🜂🜁2 🜊1000🜁0 "check_permissions"🜁1 ⟁validated🜂🜁3 🜊1000🜁0 "apply"🜁1 ⟁settings🜂🜂🜂

English: Load sales data, filter by date range, calculate metrics, create visualization
LC-R: 🜊1000🜁0 "pipeline"🜁1 🜊14🜁0 🜊1000🜁0 "load"🜁1 "sales.csv"🜂🜁1 🜊1000🜁0 "filter"🜁1 ⟁data🜁2 🜊1000🜁0 "between"🜁1 ⟁date🜁2 "2024-01-01"🜁3 "2024-12-31"🜂🜂🜁2 🜊1000🜁0 "aggregate"🜁1 ⟁filtered🜁2 🜊15🜁0 "total"🜁1 ⟁sum🜁2 "average"🜁3 ⟁mean🜂🜂🜁3 🜊1000🜁0 "visualize"🜁1 ⟁metrics🜁2 "chart"🜂🜂🜂

English: Go to ./relative/path
LC-R: 🜊1000🜁0 "navigate"🜁1 "./relative/path"🜂

English: Merge map1 with map2
LC-R: 🜊1000🜁0 "merge"🜁1 ⟁map1🜁2 ⟁map2🜂

English: Search then sort then limit
LC-R: 🜊1000🜁0 "pipeline"🜁1 🜊14🜁0 🜊1000🜁0 "search"🜁1 ⟁database🜁2 "query"🜂🜁1 🜊1000🜁0 "sort"🜁1 ⟁results🜁2 ⟁desc🜂🜁2 🜊1000🜁0 "limit"🜁1 ⟁sorted🜁2 10🜂🜂🜂

English: Change to /root/system
LC-R: 🜊1000🜁0 "navigate"🜁1 "/root/system"🜂

English: For each item in list do process
LC-R: 🜊1000🜁0 "for_each"🜁1 ⟁list🜁2 🜊1000🜁0 "process"🜁1 ⟁item🜂🜂

English: Search for *.txt
LC-R: 🜊1000🜁0 "find"🜁1 "*.txt"🜂

English: Locate all Python files recursively
LC-R: 🜊1000🜁0 "find"🜁1 "**/*.py"🜂

English: Write to output.txt
LC-R: 🜊1000🜁0 "write"🜁1 "output.txt"🜁2 ⟁data🜂

English: Delete old.dat
LC-R: 🜊1000🜁0 "delete"🜁1 "old.dat"🜂

English: List all files recursively
LC-R: 🜊1000🜁0 "ls"🜁1 "-R"🜂

English: Navigate to ./relative/path
LC-R: 🜊1000🜁0 "navigate"🜁1 "./relative/path"🜂

English: Locate all text files
LC-R: 🜊1000🜁0 "find"🜁1 "*.txt"🜂

English: Load CSV, filter rows, aggregate by group, save results
LC-R: 🜊1000🜁0 "pipeline"🜁1 🜊14🜁0 🜊1000🜁0 "load"🜁1 "data.csv"🜁2 "csv"🜂🜁1 🜊1000🜁0 "filter"🜁1 ⟁rows🜁2 🜊1000🜁0 "gt"🜁1 ⟁score🜁2 80🜂🜂🜁2 🜊1000🜁0 "group_by"🜁1 ⟁filtered🜁2 "category"🜂🜁3 🜊1000🜁0 "save"🜁1 "results.json"🜁2 ⟁grouped🜂🜂🜂


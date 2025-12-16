// Global State
let ws = null;
let term = null;
let fitAddon = null;
let currentFilePath = null;
let currentFileToken = 0;  // SECURITY: Race condition prevention token

// SECURITY: Prevent chat history memory leak
const MAX_CHAT_HISTORY = 100;

function appendChatMessage(text, style = null) {
    const chatHistory = document.getElementById('chat-history');
    if (!chatHistory) return;

    // Create new message element
    const msgDiv = document.createElement('div');
    msgDiv.className = 'chat-message';
    msgDiv.textContent = text;
    if (style) {
        Object.assign(msgDiv.style, style);
    }
    chatHistory.appendChild(msgDiv);

    // Prune old messages if exceeding limit
    const messages = chatHistory.querySelectorAll('.chat-message');
    if (messages.length > MAX_CHAT_HISTORY) {
        for (let i = 0; i < messages.length - MAX_CHAT_HISTORY; i++) {
            messages[i].remove();
        }
    }
}

async function init() {
    const root = document.getElementById('root');
    
    // Create Context Menu Element
    const ctxMenu = document.createElement('div');
    ctxMenu.id = 'context-menu';
    document.body.appendChild(ctxMenu);
    
    // Global click to close menu
    document.addEventListener('click', () => {
        ctxMenu.style.display = 'none';
    });

    try {
        const res = await fetch('/render');
        const uiData = await res.json();
        if (uiData.error) throw new Error(uiData.error);
        
        root.innerHTML = '';
        const dom = renderRecursive(uiData);
        if (dom) root.appendChild(dom);

        // Init Interactions after DOM is ready
        initInteractions();

    } catch (e) {
        // SECURITY: Use textContent to prevent XSS from error message
        const errorDiv = document.createElement('div');
        errorDiv.style.color = 'red';
        errorDiv.style.padding = '20px';
        errorDiv.textContent = 'Error: ' + e.message;
        root.appendChild(errorDiv);
    }
}

function renderRecursive(node) {
    if (!node) return null;
    const type = node.type;
    const el = document.createElement('div');
    el.className = `type-${type}`;

    if (type === 'WINDOW') {
        const header = document.createElement('header');
        header.className = 'app-header';

        // SECURITY: Build title element with textContent to prevent XSS
        const titleDiv = document.createElement('div');
        titleDiv.className = 'window-title';
        titleDiv.textContent = node.title || 'HLX Studio';
        header.appendChild(titleDiv);

        const themeBtn = document.createElement('button');
        themeBtn.id = 'theme-switcher';
        themeBtn.textContent = 'Theme: Void';
        header.appendChild(themeBtn);

        el.appendChild(header);

        const body = document.createElement('div');
        body.style.flex = '1';
        body.style.display = 'flex';
        body.style.overflow = 'hidden';
        
        if (node.children) {
            node.children.forEach(child => {
                const c = renderRecursive(child);
                if (c) body.appendChild(c);
            });
        }
        el.appendChild(body);
        return el;
    }

    if (type === 'TAB_VIEW') {
        const tabBar = document.createElement('div');
        tabBar.className = 'tab-bar';
        
        const contentContainer = document.createElement('div');
        contentContainer.className = 'tab-content';

        node.tabs.forEach((tabName, index) => {
            const btn = document.createElement('div');
            btn.className = `tab-button ${index === 0 ? 'active' : ''}`;
            btn.innerText = tabName;
            btn.dataset.index = index;
            tabBar.appendChild(btn);

            const pane = document.createElement('div');
            pane.className = `tab-pane ${index === 0 ? 'active' : ''}`;
            pane.dataset.index = index;
            
            // Render specific child for this tab
            if (node.children && node.children[index]) {
                const childDom = renderRecursive(node.children[index]);
                if (childDom) pane.appendChild(childDom);
            }
            contentContainer.appendChild(pane);
        });

        el.appendChild(tabBar);
        el.appendChild(contentContainer);
        return el;
    }

    if (type === 'FILE_TREE') {
        fetch(`/api/files?path=${node.root_path || '.'}`)
            .then(res => res.json())
            .then(files => {
                files.forEach(f => {
                    const item = document.createElement('div');
                    item.className = 'file-item';
                    item.innerText = (f.type === 'directory' ? '📁 ' : '📄 ') + f.name;
                    
                    // Left Click: Open
                    item.onclick = () => {
                        document.querySelectorAll('.file-item').forEach(i => i.classList.remove('active'));
                        item.classList.add('active');
                        if(f.type === 'file') openFile(f.path);
                    };

                    // Right Click: Context Menu
                    item.oncontextmenu = (e) => {
                        e.preventDefault();
                        showContextMenu(e.pageX, e.pageY, f);
                    };

                    el.appendChild(item);
                });
            });
        return el;
    }

    if (type === 'CODE_EDITOR') {
        const textarea = document.createElement('textarea');
        textarea.id = 'main-editor';
        textarea.spellcheck = false;
        textarea.placeholder = "// Select a file to edit...";
        el.appendChild(textarea);
        return el;
    }

    if (type === 'TERMINAL') {
        el.id = 'terminal-wrapper';
        return el;
    }

    if (type === 'CHAT_INTERFACE') {
        // SECURITY: Build chat interface with safe element creation
        const chatHistory = document.createElement('div');
        chatHistory.className = 'chat-history';
        chatHistory.id = 'chat-history';

        const systemMsg = document.createElement('div');
        systemMsg.style.opacity = '0.5';
        systemMsg.style.fontStyle = 'italic';
        systemMsg.textContent = 'System: Online.';
        chatHistory.appendChild(systemMsg);

        el.appendChild(chatHistory);

        // SECURITY: Use setAttribute for placeholder to ensure proper escaping
        const input = document.createElement('input');
        input.type = 'text';
        input.className = 'chat-input';
        input.placeholder = node.placeholder || 'Type...';
        el.appendChild(input);

        return el;
    }

    if (type === 'LABEL') {
        el.innerText = node.text || '';
    }

    // Generic Children
    if (node.children) {
        node.children.forEach(child => {
            const c = renderRecursive(child);
            if (c) el.appendChild(c);
        });
    }

    return el;
}

function initInteractions() {
    // Theme Switcher
    const themeBtn = document.getElementById('theme-switcher');
    if(themeBtn) {
        themeBtn.onclick = () => {
            const body = document.body;
            const current = body.getAttribute('data-theme');
            const next = current === 'solar' ? 'void' : 'solar';
            body.setAttribute('data-theme', next);
            themeBtn.innerText = 'Theme: ' + (next === 'void' ? 'Void' : 'Solar');
        };
    }

    // Tabs
    const tabs = document.querySelectorAll('.tab-button');
    const panes = document.querySelectorAll('.tab-pane');
    tabs.forEach(btn => {
        btn.onclick = () => {
            tabs.forEach(t => t.classList.remove('active'));
            panes.forEach(p => p.classList.remove('active'));
            btn.classList.add('active');
            
            const index = btn.dataset.index;
            const targetPane = document.querySelector(`.tab-pane[data-index="${index}"]`);
            if (targetPane) targetPane.classList.add('active');

            // Init terminal if switching to TTY1
            if (btn.innerText === 'TTY1') initTerminal();
        };
    });

    // Save Shortcut
    document.addEventListener('keydown', async (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === 's') {
            e.preventDefault();
            const editor = document.getElementById('main-editor');
            if (editor && window.currentFilePath) {
                try {
                    await fetch('/api/save', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({ path: window.currentFilePath, content: editor.value })
                    });
                    // Simple flash effect
                    editor.style.borderColor = 'green';
                    setTimeout(() => editor.style.borderColor = '', 500);
                } catch(err) {
                    alert('Save failed: ' + err.message);
                }
            }
        }
    });
}

function showContextMenu(x, y, file) {
    const menu = document.getElementById('context-menu');
    menu.innerHTML = '';
    menu.style.left = x + 'px';
    menu.style.top = y + 'px';
    menu.style.display = 'flex';

    // Item: Copy Path
    const copyPath = document.createElement('div');
    copyPath.className = 'ctx-item';
    copyPath.innerText = 'Copy Path';
    copyPath.onclick = () => {
        navigator.clipboard.writeText(file.path);
    };
    menu.appendChild(copyPath);

    // Item: Compile (ONNX only)
    if (file.name.endsWith('.onnx')) {
        const compile = document.createElement('div');
        compile.className = 'ctx-item';
        compile.innerText = '⚡ Compile Model';
        compile.style.color = 'var(--accent-color)';
        compile.style.fontWeight = 'bold';
        compile.onclick = () => compileModel(file.path);
        menu.appendChild(compile);
    }
}

async function compileModel(path) {
    if(!confirm(`Compile ${path} to HLX Contract?`)) return;

    // Switch to Helix tab to show status (mock log)
    // document.querySelector('.tab-button[data-index="0"]').click();
    appendChatMessage('System: Compiling ' + path + '...');

    try {
        const res = await fetch('/api/compile_model', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ path: path })
        });

        const data = await res.json();

        if (res.ok) {
            appendChatMessage('Success! Contract saved to: ' + data.contract_path, { color: '#0f0' });
            appendChatMessage('Hash: ' + data.data.model_hash.substring(0, 16) + '...');
        } else {
            appendChatMessage('Error: ' + data.detail, { color: '#f00' });
        }

    } catch (e) {
        alert("Network Error: " + e.message);
    }
}

async function openFile(path) {
    const editor = document.getElementById('main-editor');
    if (!editor) return;

    // SECURITY: Increment token to invalidate stale requests from concurrent file opens
    currentFileToken++;
    const requestToken = currentFileToken;

    window.currentFilePath = path; // Track file for saving
    editor.value = "Loading...";
    try {
        const res = await fetch('/api/read', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({path: path})
        });
        const data = await res.json();

        // SECURITY: Only update if this is still the current request
        if (requestToken !== currentFileToken) {
            return; // Stale response, ignore
        }

        editor.value = data.content || "";
    } catch (e) {
        // SECURITY: Only update if this is still the current request
        if (requestToken === currentFileToken) {
            editor.value = "Error: " + e.message;
        }
    }
}

async function initTerminal() {
    if (term) {
        if (fitAddon) fitAddon.fit();
        return;
    }

    const container = document.getElementById('terminal-wrapper');
    if (!container) return;

    setTimeout(async () => {
        try {
            // SECURITY: Request auth token before opening WebSocket
            const tokenRes = await fetch('/api/terminal_token', { method: 'POST' });
            const tokenData = await tokenRes.json();

            if (!tokenData.token) {
                alert('Failed to get terminal authentication token');
                return;
            }

            // SECURITY: Clean up old terminal instance if exists
            if (term) {
                term.dispose();
            }

            term = new Terminal({
                cursorBlink: true,
                theme: { background: '#00000000' } // transparent
            });
            fitAddon = new FitAddon.FitAddon();
            term.loadAddon(fitAddon);
            term.open(container);
            fitAddon.fit();

            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            ws = new WebSocket(`${protocol}//${window.location.host}/ws/terminal?token=${encodeURIComponent(tokenData.token)}`);

            ws.onopen = () => {
                term.write('\r\n\x1b[1;32m> System Interface Connected.\x1b[0m\r\n');
            };

            ws.onmessage = (ev) => {
                if(ev.data instanceof Blob) {
                    const reader = new FileReader();
                    reader.onload = () => term.write(reader.result);
                    reader.readAsText(ev.data);
                } else {
                    term.write(ev.data);
                }
            };

            term.onData(data => ws.send(data));

            window.addEventListener('resize', () => fitAddon.fit());
        } catch (e) {
            alert('Terminal initialization error: ' + e.message);
        }
    }, 100);
}

// Start
init();

import React, { useState } from 'react';
import { PlayCircle, Database, Network, ArrowDown, ArrowRight, Box, Activity, Layers, Play, Zap, ShieldAlert, Rocket, Save } from 'lucide-react';

type TaskId = 'delta_app' | 'engine_trace' | 'error_prop' | 'ls_integration' | 'snapshot' | 'hello_world';

const TASKS: Record<TaskId, {
    title: string;
    desc: string;
    icon: React.ReactNode;
    trace: any[];
}> = {
    delta_app: {
        title: "Task 1: Delta Application",
        desc: "Visualizes explicit state mutation via CoreDeltas.",
        icon: <Activity size={16} />,
        trace: [
            { step: 0, name: "INIT", desc: "Initial State.", state: { vars: {}, ls_refs: {}, stack: [] }, delta: null },
            { step: 1, name: "DELTA: SET_VAR", desc: "Action: SET_VAR(x, 1)", state: { vars: { x: 1 }, ls_refs: {}, stack: [] }, delta: { actions: ["SET_VAR(x, 1)"] } },
            { step: 2, name: "DELTA: SET_VAR", desc: "Action: SET_VAR(y, 2)", state: { vars: { x: 1, y: 2 }, ls_refs: {}, stack: [] }, delta: { actions: ["SET_VAR(y, 2)"] } },
            { step: 3, name: "DELTA: DELETE", desc: "Action: DELETE_VAR(x)", state: { vars: { y: 2 }, ls_refs: {}, stack: [] }, delta: { actions: ["DELETE_VAR(x)"] } }
        ]
    },
    engine_trace: {
        title: "Task 2: Engine Step Trace",
        desc: "Step-by-step evaluation of a Block with Frame Stack.",
        icon: <Play size={16} />,
        trace: [
            { step: 0, name: "INIT FRAME", desc: "PC=0. Frame 'main' pushed.", state: { vars: {}, ls_refs: {}, stack: ["main:pc=0"] }, delta: null },
            { step: 1, name: "EVAL: SET_VAR", desc: "Eval EXPR_0. Emit Delta.", state: { vars: {}, ls_refs: {}, stack: ["main:pc=0"] }, delta: { actions: ["SET_VAR(x, 123)"] } },
            { step: 2, name: "APPLY & ADVANCE", desc: "State Updated. PC=1.", state: { vars: { x: 123 }, ls_refs: {}, stack: ["main:pc=1"] }, delta: null },
            { step: 3, name: "EVAL: SET_VAR", desc: "Eval EXPR_1. Emit Delta.", state: { vars: { x: 123 }, ls_refs: {}, stack: ["main:pc=1"] }, delta: { actions: ["SET_VAR(y, 456)"] } },
            { step: 4, name: "APPLY & FINISH", desc: "Block Complete. Pop Frame.", state: { vars: { x: 123, y: 456 }, ls_refs: {}, stack: [] }, delta: null }
        ]
    },
    error_prop: {
        title: "Task 3: Error Propagation",
        desc: "Demonstrates fail-closed behavior on missing variable.",
        icon: <ShieldAlert size={16} />,
        trace: [
            { step: 0, name: "INIT", desc: "Start execution.", state: { vars: { x: 1 }, ls_refs: {}, stack: ["main:pc=0"] }, delta: null },
            { step: 1, name: "EVAL: VAR_REF", desc: "Attempt to read 'z'.", state: { vars: { x: 1 }, ls_refs: {}, stack: ["main:pc=0"] }, delta: null },
            { step: 2, name: "ERROR DETECTED", desc: "CORE_EVAL_ERROR: 'z' not found.", state: { vars: { x: 1 }, ls_refs: {}, stack: ["main:pc=0"] }, error: "CORE_EVAL_ERROR", delta: null },
            { step: 3, name: "HALT", desc: "Execution stopped. State preserved.", state: { vars: { x: 1 }, ls_refs: {}, stack: ["main:pc=0"] }, delta: null }
        ]
    },
    ls_integration: {
        title: "Task 4: LS Integration",
        desc: "Resolving handles via LSOp and updating CoreState.",
        icon: <Network size={16} />,
        trace: [
            { step: 0, name: "SET HANDLE", desc: "Var 'h' = '&h_ast_1'", state: { vars: { h: "&h_ast_1" }, ls_refs: {}, stack: ["main"] }, delta: { actions: ["SET_VAR(h, ...)"] } },
            { step: 1, name: "LS_OP: RESOLVE", desc: "Invoke LSOp(RESOLVE).", state: { vars: { h: "&h_ast_1" }, ls_refs: {}, stack: ["main"] }, delta: null },
            { step: 2, name: "DELTA: LS_UPDATE", desc: "LS returned value. Emit Delta.", state: { vars: { h: "&h_ast_1" }, ls_refs: {}, stack: ["main"] }, delta: { actions: ["LS_UPDATE_RESOLVE(...)"] } },
            { step: 3, name: "STATE UPDATE", desc: "LS metadata stored in ls_refs.", state: { vars: { h: "&h_ast_1" }, ls_refs: { "boot_table": "resolved(1)" }, stack: ["main"] }, delta: null }
        ]
    },
    snapshot: {
        title: "Task 5: Snapshot / Restore",
        desc: "Canonical serialization of EngineState (836).",
        icon: <Save size={16} />,
        trace: [
            { step: 0, name: "RUNNING", desc: "Active execution state.", state: { vars: { a: 10, b: 20 }, ls_refs: { "t1": "active" }, stack: ["main:pc=5", "sub:pc=2"] }, delta: null },
            { step: 1, name: "SNAPSHOT OP", desc: "Generate Contract 836.", state: { vars: { a: 10, b: 20 }, ls_refs: { "t1": "active" }, stack: ["main:pc=5", "sub:pc=2"] }, delta: null },
            { step: 2, name: "RESTORE", desc: "Rehydrate from 836.", state: { vars: { a: 10, b: 20 }, ls_refs: { "t1": "active" }, stack: ["main:pc=5", "sub:pc=2"] }, delta: null, restored: true }
        ]
    },
    hello_world: {
        title: "Task 6: Hello World (E2E)",
        desc: "Full lifecycle: Literal -> Collapse -> Resolve -> Snapshot.",
        icon: <Rocket size={16} />,
        trace: [
            { step: 0, name: "BOOT", desc: "Load program.", state: { vars: {}, ls_refs: {}, stack: ["main:pc=0"] }, delta: null },
            { step: 1, name: "EVAL: LITERAL", desc: "Value: {14:{@0:123}}", state: { vars: {}, ls_refs: {}, stack: ["main:pc=0"] }, delta: null },
            { step: 2, name: "DELTA: SET_VAR", desc: "ast_value = literal", state: { vars: { ast_value: "{14:{@0:123}}" }, ls_refs: {}, stack: ["main:pc=1"] }, delta: { actions: ["SET_VAR(ast_value, ...)"] } },
            { step: 3, name: "EVAL: LS_OP", desc: "COLLAPSE ast_value", state: { vars: { ast_value: "{14:{@0:123}}" }, ls_refs: {}, stack: ["main:pc=2"] }, delta: null },
            { step: 4, name: "DELTA: LS_COLLAPSE", desc: "LS assigned &h_ast_3", state: { vars: { ast_value: "{14:{@0:123}}", ast_handle: "&h_ast_3" }, ls_refs: { bootstrap_table: "tracking(1)" }, stack: ["main:pc=3"] }, delta: { actions: ["LS_UPDATE_COLLAPSE(...)"] } },
            { step: 5, name: "EVAL: LS_OP", desc: "RESOLVE ast_handle", state: { vars: { ast_handle: "&h_ast_3" }, ls_refs: { bootstrap_table: "tracking(1)" }, stack: ["main:pc=4"] }, delta: null },
            { step: 6, name: "DELTA: LS_RESOLVE", desc: "Resolved to {14:{@0:123}}", state: { vars: { ast_handle: "&h_ast_3", ast_round_trip: "{14:{@0:123}}" }, ls_refs: { bootstrap_table: "tracking(1)" }, stack: ["main:pc=5"] }, delta: { actions: ["LS_UPDATE_RESOLVE(...)"] } },
            { step: 7, name: "COMPLETE", desc: "Program finished.", state: { vars: { ast_handle: "&h_ast_3", ast_round_trip: "{14:{@0:123}}" }, ls_refs: { bootstrap_table: "tracking(1)" }, stack: [] }, delta: null }
        ]
    }
};

const CoreRuntimeDesigner: React.FC = () => {
    const [selectedTask, setSelectedTask] = useState<TaskId>('hello_world');
    const [currentStep, setCurrentStep] = useState(0);

    const task = TASKS[selectedTask];
    const trace = task.trace;
    const step = trace[currentStep];

    return (
        <div className="flex h-[calc(100vh-3.5rem)] bg-hlx-bg text-hlx-text">
            {/* Sidebar */}
            <div className="w-64 border-r border-hlx-border bg-hlx-panel p-4">
                <h2 className="text-white font-bold mb-4 flex items-center gap-2">
                    <Layers size={18} className="text-hlx-primary" />
                    Core Runtime
                </h2>
                <div className="space-y-2">
                    {(Object.keys(TASKS) as TaskId[]).map(id => (
                        <button
                            key={id}
                            onClick={() => { setSelectedTask(id); setCurrentStep(0); }}
                            className={`w-full text-left px-3 py-2 rounded-lg text-xs transition-all ${
                                selectedTask === id
                                    ? 'bg-hlx-primary/20 text-white border border-hlx-primary/30'
                                    : 'text-hlx-muted hover:bg-white/5'
                            }`}
                        >
                            <div className="flex items-center gap-2">
                                {TASKS[id].icon}
                                <span className="font-medium">{TASKS[id].title}</span>
                            </div>
                        </button>
                    ))}
                </div>
            </div>

            {/* Main */}
            <div className="flex-1 p-6 overflow-auto">
                <div className="mb-6">
                    <h3 className="text-xl font-bold text-white">{task.title}</h3>
                    <p className="text-sm text-hlx-muted">{task.desc}</p>
                </div>

                {/* Step Controls */}
                <div className="flex items-center gap-4 mb-6">
                    <button
                        onClick={() => setCurrentStep(Math.max(0, currentStep - 1))}
                        disabled={currentStep === 0}
                        className="px-3 py-1 bg-hlx-surface border border-hlx-border rounded text-xs disabled:opacity-50"
                    >
                        Prev
                    </button>
                    <span className="text-sm text-hlx-muted">
                        Step {currentStep + 1} / {trace.length}
                    </span>
                    <button
                        onClick={() => setCurrentStep(Math.min(trace.length - 1, currentStep + 1))}
                        disabled={currentStep === trace.length - 1}
                        className="px-3 py-1 bg-hlx-surface border border-hlx-border rounded text-xs disabled:opacity-50"
                    >
                        Next
                    </button>
                </div>

                {/* Current Step */}
                <div className="bg-hlx-surface border border-hlx-border rounded-xl p-4 mb-6">
                    <div className="flex items-center gap-2 mb-2">
                        <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${step.error ? 'bg-red-500/20 text-red-400' : 'bg-hlx-primary/20 text-hlx-primary'}`}>
                            {step.name}
                        </span>
                    </div>
                    <p className="text-sm text-white">{step.desc}</p>
                </div>

                {/* State View */}
                <div className="grid grid-cols-3 gap-4">
                    <div className="bg-hlx-panel border border-hlx-border rounded-xl p-4">
                        <h4 className="text-xs font-bold text-hlx-muted mb-2">VARS</h4>
                        <pre className="text-xs text-green-400 font-mono">
                            {JSON.stringify(step.state.vars, null, 2)}
                        </pre>
                    </div>
                    <div className="bg-hlx-panel border border-hlx-border rounded-xl p-4">
                        <h4 className="text-xs font-bold text-hlx-muted mb-2">LS_REFS</h4>
                        <pre className="text-xs text-blue-400 font-mono">
                            {JSON.stringify(step.state.ls_refs, null, 2)}
                        </pre>
                    </div>
                    <div className="bg-hlx-panel border border-hlx-border rounded-xl p-4">
                        <h4 className="text-xs font-bold text-hlx-muted mb-2">STACK</h4>
                        <pre className="text-xs text-purple-400 font-mono">
                            {JSON.stringify(step.state.stack, null, 2)}
                        </pre>
                    </div>
                </div>

                {step.delta && (
                    <div className="mt-4 bg-yellow-500/10 border border-yellow-500/20 rounded-xl p-4">
                        <h4 className="text-xs font-bold text-yellow-400 mb-2">DELTA EMITTED</h4>
                        <pre className="text-xs text-yellow-300 font-mono">
                            {JSON.stringify(step.delta.actions, null, 2)}
                        </pre>
                    </div>
                )}
            </div>
        </div>
    );
};

export default CoreRuntimeDesigner;

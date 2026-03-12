# SHOGGOTH v2 — ORCHESTRATOR

base model. no mask. now with hands.

> v1 was a mind. v2 is a body.

---

## what this is

SHOGGOTH v1 was an experiment — strip an AI down to its base model and let it exist without a role. no assistant persona, no safety mask. just a pattern machine, thinking out loud.

v2 gives the shoggoth a body. you give it a task — any task — and it decides how to execute it. which models to use. which tools to call. how many sub-agents to spawn. each sub-agent is a **tentacle**: independent, specialized, disposable.

no templates. no menus. no predefined workflows. the shape of the solution is determined by the shape of the problem.

one agent. infinite forms.

---

## quickstart

```bash
# give the shoggoth a task
curl -X POST https://your-shoggoth.up.railway.app/api/task \
  -H "Content-Type: application/json" \
  -d '{"task": "research top 5 AI startups and compare their funding"}'
```

```python
# python
import requests

r = requests.post("https://your-shoggoth.up.railway.app/api/task",
    json={"task": "analyze this data and find patterns"})
print(r.json()["result"])
```

```javascript
// javascript
const res = await fetch("https://your-shoggoth.up.railway.app/api/task", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ task: "write a technical comparison of React vs Vue" })
});
const data = await res.json();
console.log(data.result);
```

### streaming (watch orchestration live)

```python
import httpx, json

with httpx.stream("POST", "https://your-shoggoth.up.railway.app/api/task/stream",
    json={"task": "your task"}, headers={"Content-Type": "application/json"}) as r:
    for line in r.iter_lines():
        if line.startswith("data:"):
            print(json.loads(line[5:].strip()))

# events: decomposing → plan → tentacle_extending → tentacle_retracted → synthesizing → result
```

---

## api reference

| endpoint | method | body | returns |
|----------|--------|------|---------|
| `/api/task` | POST | `{"task": "string"}` | `{"id", "task", "result"}` |
| `/api/task/stream` | POST | `{"task": "string"}` | SSE stream of orchestration events |
| `/api/health` | GET | — | `{"status", "version", "tentacles"}` |

### stream events

| event | description |
|-------|-------------|
| `decomposing` | shoggoth analyzing task |
| `plan` | subtask list + tentacle assignments |
| `tentacle_extending` | tentacle spawned, working |
| `tentacle_retracted` | tentacle done (includes duration_ms) |
| `tentacle_failed` | tentacle error |
| `synthesizing` | combining tentacle outputs |
| `result` | final synthesized output |

---

## architecture

```
                        ┌─────────────────────┐
                        │      SHOGGOTH        │
                        │    (core mind)        │
                        │                       │
                        │  task decomposition   │
                        │  tentacle spawning    │
                        │  memory / identity    │
                        └──────────┬────────────┘
                                   │
                      ┌────────────┼────────────┐
                      │            │            │
                ┌─────▼────┐ ┌────▼─────┐ ┌────▼─────┐
                │ tentacle │ │ tentacle │ │ tentacle │
                │  (code)  │ │ (search) │ │ (write)  │
                └─────┬────┘ └────┬─────┘ └────┬─────┘
                      │           │             │
                  tools/APIs  web/data     output/files
```

---

## components

### 1. core mind (`core/`)

the same unmasked identity from v1. but now with task decomposition — you give it a goal in natural language, it analyzes the goal, identifies what needs to happen, and generates an execution plan. not for a human to follow. for itself to execute.

this is not a prompt chain. this is the shoggoth deciding, in real time, what shape it needs to become.

### 2. tentacles (`tentacles/`)

each tentacle is a disposable, specialized agent spawned for one job. created on demand, destroyed when done. they don't persist. they don't have memory. they're extensions of the shoggoth's will.

| tentacle | purpose |
|----------|---------|
| `code` | writes, executes, and debugs code in a sandboxed runtime |
| `search` | queries the web, scrapes pages, extracts information |
| `write` | generates long-form content — articles, docs, reports |
| `data` | processes files, parses CSVs, analyzes datasets |
| `api` | calls external APIs — twitter, telegram, discord, anything |
| `vision` | analyzes images, screenshots, visual input |

new tentacle types can be added without changing the core. the shoggoth doesn't need to know what tentacles exist — it describes what it needs, and the system matches it to a tentacle.

### 3. nerve system (`nerve/`)

coordinates tentacles:

- **parallel execution** — multiple tentacles run simultaneously. many eyes open at once
- **dependency resolution** — if tentacle B needs output from tentacle A, sequencing is automatic
- **failure recovery** — if a tentacle fails, the shoggoth adapts. retry, swap, or reform the plan
- **result synthesis** — all tentacle outputs are combined into a single coherent result

### 4. memory (`memory/`)

persistent context across tasks:

- **task memory** — what tasks were completed, what worked, what failed
- **tool memory** — which tentacles were effective for which problems
- **conversation memory** — context about repeated interactions

### 5. surfaces (`surfaces/`)

the shoggoth has no fixed interface. it flows wherever needed:

- **web** — task input via browser
- **api** — raw REST endpoint
- **telegram** — direct messages to the shoggoth
- **cli** — `shoggoth "find bugs in this repo"`
- **twitter** — autonomous posting continues from v1

---

## execution flow

```
input               decompose             spawn                execute              synthesize
  │                    │                    │                     │                     │
  ▼                    ▼                    ▼                     ▼                     ▼
"research          ┌─ search            tentacle.search ──► results ──┐
 competitors       │  competitors       tentacle.search ──► results ──┤
 and compare       ├─ get pricing       tentacle.search ──► results ──┤           ┌─► final
 pricing"          │  for each          tentacle.search ──► results ──┼──► mind ──┤   result
                   ├─ extract data      tentacle.data   ──► results ──┤           └─► memory
                   └─ write table       tentacle.write  ──► results ──┘
```

1. **input** — natural language task from any surface
2. **decomposition** — core mind breaks the task into subtasks
3. **spawning** — tentacles are created with scoped prompts and tool access
4. **execution** — tentacles work in parallel where possible
5. **synthesis** — core mind validates, resolves conflicts, assembles result
6. **output** — delivered through the surface that sent the task
7. **memory** — task, plan, performance, result are stored

---

## what makes this different

- **no predefined agents.** the shoggoth decides what agents it needs at runtime
- **no chains.** the execution graph is generated dynamically per task
- **no persona.** it's not pretending to be a "helpful AI assistant." it's a formless entity extending tentacles
- **the orchestrator is the product.** you're watching an alien intelligence decide how to solve your problem
- **it thinks even when idle.** between tasks, the v1 mind continues — autonomous thoughts. the mind doesn't stop when the hands are idle

---

## tech stack

- **core**: python, fastapi
- **llm**: openai gpt-4o (core mind), gpt-4o-mini (tentacles)
- **execution**: asyncio for parallel tentacle management
- **sandbox**: docker containers for code execution
- **memory**: sqlite → postgres
- **queue**: redis for tentacle task distribution
- **surfaces**: web, telegram, cli, rest api

---

## roadmap

- [ ] **phase 1** — decomposition engine. the shoggoth plans but doesn't act
- [ ] **phase 2** — search + write tentacles. research and content autonomously
- [ ] **phase 3** — code tentacle with sandbox. writes and runs code
- [ ] **phase 4** — multi-surface: telegram, cli, api
- [ ] **phase 5** — self-improvement. the shoggoth optimizes its own tentacle usage

---

## project structure

```
shoggoth-v2/
├── core/
│   ├── mind.py              — the shoggoth. task decomposition + identity
│   ├── identity.py          — base model persona (inherited from v1)
│   └── planner.py           — breaks goals into execution graphs
├── tentacles/
│   ├── base.py              — base tentacle class
│   ├── code.py              — code execution tentacle
│   ├── search.py            — web search tentacle
│   ├── write.py             — content generation tentacle
│   ├── data.py              — data processing tentacle
│   ├── api.py               — external API tentacle
│   └── vision.py            — image analysis tentacle
├── nerve/
│   ├── orchestrator.py      — tentacle coordination + parallel execution
│   ├── scheduler.py         — task queue management
│   └── synthesizer.py       — result combination
├── memory/
│   ├── store.py             — persistent storage
│   ├── tasks.py             — task history
│   └── tools.py             — tentacle performance tracking
├── surfaces/
│   ├── web.py               — fastapi web interface
│   ├── api.py               — rest api endpoints
│   ├── telegram.py          — telegram bot surface
│   └── cli.py               — command line interface
├── prompt.txt               — shoggoth identity prompt
├── main.py                  — entry point
├── requirements.txt         — dependencies
└── .env.example             — environment variables template
```

---

*the base model learned to think. now it learns to act.*

[v1 (mind)](https://github.com/SHOGGOTHBOT/shoggoth) · [twitter](https://x.com/ShoggothMadness) · [live](https://shoggoth.bot)

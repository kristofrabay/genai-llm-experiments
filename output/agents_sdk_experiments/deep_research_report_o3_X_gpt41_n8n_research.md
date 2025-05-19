Comprehensive Report: n8n and the Agentic-Workflow Automation Landscape (mid-2025)

────────────────────────────────────────
A.  n8n—Deep-Dive
────────────────────────────────────────
1. Product DNA  
   • Category: Visual workflow/automation builder (low-code) that also exposes every workflow as a REST endpoint—making it usable as an orchestration layer for AI “agents”.  
   • Licence / Delivery: Source available under the Sustainable-Use (Fair-Code) licence. 100 % free if you self-host; commercial restrictions only apply if you resell the product itself. Cloud SaaS is fully managed by n8n GmbH.  
   • Tech stack: Node.js, TypeScript; workflows stored in Postgres; each “node” is an independent JS module.  
   • Community: ≈35 k GitHub ★, >15 k Slack/forum users, >400 community-supplied nodes.

2. Core Feature Set  
   • Visual, node-based builder with unlimited branches, cycles, error paths, and sub-workflows (“child workflows”).  
   • 400 + ready-made nodes: SaaS apps (Salesforce, Stripe, Slack), DBs, queues, e-mail, file systems, and specialised AI nodes (OpenAI, Anthropic, HuggingFace, Replicate).  
   • “Function/Code” node—inline JS, enabling bespoke logic, vector-store calls, etc.  
   • Triggers: Cron, Webhook, Event Stream, Polling, Queue, UI Form.  
   • Data handling: built-in parsers (CSV, XML, HTML), binary file routing, item-by-item or batch processing, looping, IF/Switch, Merge, Split, Wait/Delay, Try-Catch.  
   • AI/Agentic primitives (2023-24 releases):  
     – AI Agent node (think/plan/act, chat memory, tool calling).  
     – Templates for “Think-Plan-Act”, autonomous chat-bots, and “Proxmox AI Admin”.  
     – Prompt engineering helpers, JSON mode, function-calling schema generator.  
   • Ops features: role-based access, separate dev/stage/prod envs (Enterprise), Git-based workflow versioning, log streaming, external secret store (Vault), SAML/LDAP SSO.  
   • Deployment footprints: Docker, k8s helm chart, n8n-cloud; execution scaling via queue-mode workers.

3. Typical Use Cases (illustrative)  
   • Marketing & RevOps: enrich leads → qualify with GPT sentiment → write intro email → update HubSpot.  
   • LLM Agents: Telegram chat bot that transcribes voice (Whisper) → calls GPT-4o → triggers Jira tasks.  
   • DevOps: daily Slack stand-up summariser → aggregate GitHub PRs → run LangChain agent to extract blockers.  
   • Data engineering: S3 ingest → cleanse via JS function → embed with OpenAI → upsert Pinecone.  

4. Commercials (Cloud, May-2025)  
   • Starter $24/m (2 500 execs, 5 workflows) • Pro $60/m (10 k execs, 15 workflows) • Enterprise – custom; unlimited execs & self-host support.

5. Strengths / Watch-outs  
   ✓ Unlimited complexity (loops, recursion, inline code).  
   ✓ First-class self-hosting; data never leaves your infra.  
   ✓ Fast-moving AI roadmap, thriving template gallery.  
   ✗ Smaller turnkey-integration catalog than Zapier/Tray.  
   ✗ Fair-Code licence forbids re-selling a hosted version.  
   ✗ Needs DevOps familiarity for production-grade scaling.

────────────────────────────────────────
B.  Principal Alternatives
────────────────────────────────────────
1. Zapier  
   • Closed-source, cloud-only, >7 000 apps.  
   • “AI Actions” ChatGPT plug-in, natural-language builder, Paths, Loops, but no custom code execution beyond webhooks.  
   • Pricing: Free 100 tasks → Team $69 + /m → Enterprise custom.  
   • Target: business users who want dead-simple automations.

2. Make (née Integromat)  
   • Visual canvas with bubbles/lines; >1 000 apps; supports routers, iterators, aggregation.  
   • No built-in LLM agent primitives yet; can call any HTTP/AI API.  
   • Self-host not available.  Free 1 000 ops → Core $9/m → Teams $29 +.  
   • Strength: fine-grained data mapping, granular error handling.

3. Node-RED  
   • OSS (Apache-2). Initially IoT-centric; now >4 000 nodes.  
   • Excellent for hardware/MQTT/edge; JS-function node for anything.  
   • No SaaS; you run it yourself or via third-party hosts ($5–15/m).  
   • Security diligence required (community nodes, CVE record).

4. Pipedream  
   • Serverless integration platform for developers (JS/Python code steps).  
   • 1 000s of pre-built “actions”; cron, event streams.  
   • AI: user writes code calling OpenAI; no drag-and-drop agent UI.  
   • Free 100 k invocations with rate limits; paid from $19/m.

5. Tray.io / Tray.ai  
   • Enterprise-grade low-code iPaaS; “Merlin AI” natural-language flow builder; AI-augmented API mgmt.  
   • Hundreds of connectors, callable sub-workflows, SSO, SOC2.  
   • Pricing undisclosed; reportedly mid-four-figure €/year starting.

6. Activepieces (OSS)  
   • MIT licensed, self-host or cloud ($10/m).  
   • 200 + connectors, drag-and-drop, OpenAI piece, IF/Loop, retries.  
   • Embeddable white-label builder for SaaS vendors.  
   • Community smaller but growing quickly.

7. Automatisch (OSS)  
   • GPL; self-host free, or hosted single-user €20/m.  
   • Modern UI, unlimited flows, tasks; ≈100 connectors.  
   • LLM integration via generic HTTP—no native agent features yet.

8. Flowise  
   • OSS visual LangChain builder—specialised in LLM/agent chains.  
   • Drag-and-drop prompts, memory, tools; export as REST API.  
   • Complements, rather than replaces, general-purpose automation.

9. LangFlow  
   • Similar to Flowise; real-time debug, custom component SDK.  
   • Focus exclusively on LLM pipelines—pairs well with n8n/Zapier for non-AI tasks.

────────────────────────────────────────
C.  Head-to-Head Comparison Matrix (abridged)
────────────────────────────────────────
Legend: ✔ native / ○ possible via code / ✕ not offered

Platform            | OSS? | Self-host | #Connectors | Loops & Branches | Inline Code | Native AI-Agent Node | Natural-Language Flow Builder | Pricing (entry)
-------------------------------------------------------------------------------------------------------------------------------------------
n8n                 | Fair | ✔         | ~400        | ✔ Unlimited      | ✔ JS        | ✔ (AI Agent)         | Roadmap (AI prompt builder)  | Free self-host / $24 cloud
Zapier              | ✕    | ✕         | 7 000 +     | ✔ (Paths)        | ✕           | ○ (via ChatGPT plug-in) | ✔ (“describe your Zap…”)     | Free / $19.99 +
Make                | ✕    | ✕         | 1 000 +     | ✔ (Routers)      | ✕           | ○ (HTTP modules)     | ✕ (AI missing)               | Free / $9 +
Node-RED            | ✔    | ✔         | 4 000 +     | ✔                | ✔ JS        | ○ (OpenAI contrib)   | ✕                            | Free
Pipedream           | Partial | ✕      | 1 000 +     | Code-based       | ✔ JS/Py     | ○                   | ✕                            | Free / $19 +
Tray.ai             | ✕    | ✕         | 600 +       | ✔                | Low-code    | ○ (“Merlin AI” tools)| ✔ (Merlin)                   | $$$ (enterprise)
Activepieces        | ✔    | ✔         | 200 +       | ✔                | ✕           | ○ (OpenAI piece)     | ✕                            | Free / $10 +
Automatisch         | ✔    | ✔         | 100 +       | ✔                | ✕           | ✕                   | ✕                            | Free / €20 +
Flowise / LangFlow  | ✔    | ✔         | N/A (LLM)   | ✔ (agent chains) | Low-code    | ✔ (agents core)      | ✕                            | Free

────────────────────────────────────────
D.  Key Differentiators & Decision Drivers
────────────────────────────────────────
1. Hosting / Data Residency  
   • Need on-prem or VPC? → n8n, Node-RED, Activepieces, Automatisch, Flowise.  
   • Comfortable with vendor cloud? → Zapier, Make, Tray.

2. Depth of Agentic Capabilities  
   • Built-in think-plan-act, chat memory, tool calling → n8n (strong), Flowise, LangFlow.  
   • Generic AI calls only → Zapier, Make, Pipedream, Activepieces.  
   • No AI primitives → Automatisch (yet).

3. Integration Breadth  
   • “I just want it to connect to anything without coding” → Zapier or Tray.  
   • Willing to build/extend connectors → n8n (SDK), Node-RED (npm).

4. Complexity vs Simplicity  
   • Business-user autopilot → Zapier Paths + AI Actions, Make visual router.  
   • Power-user / developer orchestration → n8n, Pipedream, Node-RED.

5. TCO / Licensing Philosophy  
   • Zero licence fees, own infra → n8n self-host, Node-RED, Activepieces.  
   • Managed service, predictable spend → n8n-Cloud, Make, Zapier, Tray.

6. Ecosystem & Community Support  
   • Largest community tutorials/snippets → Zapier (non-code) & n8n (code).  
   • Agent-research/LLM-enthusiast community → Flowise / LangFlow.

────────────────────────────────────────
E.  Recommendations
────────────────────────────────────────
• If your priority is end-to-end agentic automation with full control over data, open extensibility, and a vibrant AI template gallery—n8n is currently the most balanced choice.  
• Pair n8n with Flowise or LangFlow when you need advanced prompt-engineering and RAG chains but still want orchestration, error handling, and scheduling.  
• Choose Zapier for quick, shallow automations where speed of connector availability outranks deep logic or self-hosting.  
• Make is compelling for non-AI, data-heavy multi-branch automations where cost per operation is sensitive.  
• Node-RED remains unbeatable in hardware/edge and for engineers comfortable writing JS functions.  
• Activepieces and Automatisch are emerging OSS options worth piloting if licensing freedom or white-labelling is paramount and you can tolerate a smaller connector set.  
• Tray.ai fits enterprises seeking low-code + AI co-pilot plus enterprise-grade governance, but budget accordingly.

────────────────────────────────────────
F.  Quick-Start Evaluation Checklist
────────────────────────────────────────
1. Data Location / Compliance requirements?  
2. Number & type of SaaS systems to integrate?  
3. Do workflows need loops, recursion, or code?  
4. Are autonomous LLM agents central or peripheral?  
5. Expected monthly task volume → cost modelling.  
6. Internal skill-set: business ops vs developers vs DevOps.  
7. Road-map fit: open-source flexibility vs turnkey SaaS speed.

Use the matrix and the checklist together to shortlist (typically two) candidates and run a proof-of-concept with a representative, AI-powered workflow.
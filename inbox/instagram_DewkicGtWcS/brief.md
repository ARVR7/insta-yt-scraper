# Brief: instagram reel DewkicGtWcS

- url: https://www.instagram.com/reel/DewkicGtWcS/
- author: saurabhs.builds
- posted: 2026-10-21T14:01:20Z
- duration_s: 70
- likes: 6668  comments: 2630  comments/likes: 0.39
- audio language: en
- needs_visual_review: yes  (view /home/runner/work/_temp/prep_instagram_DewkicGtWcS/sheet.jpg)
- recipe_hint: no
- gaps: none

## Caption / description
Companies are quietly moving away from traditional MCP 👀

The problem: every tool call sends its result back through the model, and every tool’s definition sits in the model’s context the whole time. Scale that to thousands of tools and you hit a wall.

Cloudflare’s fix is Code Mode:
→ Turn the tools into a TypeScript API
→ The model sees one tool: run_code
→ It writes a small script that runs in a locked sandbox
→ Only the final answer comes back to the model

Anthropic published the same pattern. One example went from 150,000 tokens to 2,000 (-98.7%).

Comment “LINK” and I’ll DM you Cloudflare’s full blog post 🔗

#AI #MCP #AIAgents

Hashtags: #ai #mcp #aiagents

## Transcript
language: en (1.00)
[0s] There's a new shift happening in the AI industry.
[2s] Companies are moving away from the traditional MCPs
[5s] and picking a completely different architecture instead.
[7s] Let's break it down in 30 seconds.
[8s] So we all know the drill.
[9s] If an AI agent wants to use the tool, you use an MCP.
[12s] MCP is the standard.
[13s] It's how an AI agent discovers the tools and calls them.
[15s] But this technique has a fundamental problem.
[17s] You would think that everything is smooth, but it's not.
[19s] For example, my agent needs to find a customer.
[21s] That's one tool called.
[22s] Then it has to flesh the customer's order.
[23s] That's a second tool called.
[24s] Every single result goes back to the model
[27s] before the next step starts.
[28s] And every tools definition sits inside the model's context
[32s] throughout the whole time.
[33s] Now scale that to thousands of tools.
[35s] Cloudflare hit this exact wall.
[37s] So they build something they call code mode.
[39s] Instead of handing the model a big list of tools,
[41s] they convert the tools into TypeScript API.
[43s] The model now sees just one tool, which is run code.
[45s] It writes a small script and that script
[47s] runs inside a lock sandbox.
[49s] The in-between data never comes inside the model.
[52s] Only the final answer does.
[53s] And their reason is models are simply better than writing code
[56s] than at calling tools directly.
[57s] Anthropic published the same pattern.
[59s] One example dropped 150,000 tokens to just 2,000 tokens.
[64s] I found this architecture completely fascinating.
[66s] If you want the complete block from Cloudflare's engineers,
[69s] just comment, link, and I will DM it to you.

## On-screen text (OCR, noisy: words may run together)
[0s] THE SHIFT
[0s] Al agents·a new architecture
[3s] what everyone used
[9s] HOWMCPWORKS
[9s] the standard·discover tools→call them
[9s] Al Agent
[12s] uses
[15s] THEPROBLEM
[15s] every result goes back through the model
[18s] MODEL
[21s] ①find_customer()
[21s] result→model
[21s] fetch_orders()
[21s] TOOLS
[27s] OLDMCP
[27s] 100s of tool schemas·context bloat
[30s] MCPServer1
[30s] MCPServer2
[30s] Agent
[30s] MCPServer3
[30s] MCPServer4
[30s] MODELCONTEXT WINDOW
[33s] ×1000
[36s] cloudflare·tools →typescript api
[39s] CODEMODE
[39s] search_db
[39s] get_order
[39s] send_email
[39s] +997more
[42s] interface API
[42s] findCustomer(id)
[42s] getorders(cid)
[42s] sendEmail(to)
[42s] seesonly
[42s] /.alltools
[42s] TypeScript API
[45s] LOCKED SANDBOX
[45s] in-between data never touches the model
[45s] script.ts
[48s] SANDBOX
[48s] orders[]
[48s] customer
[48s] filter()
[51s] raw data staysinside
[51s] onlythefinalanswer
[54s] WHYITWORKS
[54s] what models are actually good at
[54s] Models write code better than they call tools.
[54s] Writingcode
[57s] ANTHROPIC·SAME PATTERN
[57s] tokens used foronetask
[60s] 150,000
[66s] blog.cloudflare.com/code-mode
[66s] SEPTEMBER 26,2025
[66s] Code Mode:the better
[66s] way to use MCP
[66s] KentonVarda and Sunil Pai
[66s] 12MINUTEREAD
[66s] COPYURL

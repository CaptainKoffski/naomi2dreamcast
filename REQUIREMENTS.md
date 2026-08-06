# The repo
This repo is an umbrella repo for Naomi2Dreamcast porting project. It's goals are
 - Store full Sega Naomi games list with their metadata
 - Store links to specific games' porting repos
 - Store assessments of games portability
 - Store general knowledge base and guidelines (information applicable for any port)

# The project
Naomi2Dreamcast project is a project about porting games from Sega Naomi arcade system to Sega Dreamcast home gaming console.

The final goal is to port as much games as possible, ideally, the full library.

# The next step
We have already prepared table with full games library in `GAME_FORMATS.md`. We have prepared full romset in the `naomi` folder.
We have prepared toolset for converting roms to `.dat` format (friendly for disassembling).
The next step should be deep analysis of the romset from portability perspective.
We want to work on these ports progressively, starting from games which easy to port, getting more and more experience
up to the hardest ones. This is why we need this initial assessment.
But before that we need to define criterias, format of output documents, tooling and approach.

# Task
AI to help me to 
 - Define criteria for games portability assessment
 - Define uniform template (format) for storing assessment results
 - Define if we need any tools to prepare besides the existing ones

# What games to take
We need to assess all the games in the Naomi library except those which were already officially exported to Dreamcast.
It simply makes no sense to port them, thus we don't need to spend time assessing them.
The column `DC port` is to help.

# Repo structure
There must be a summary table (I suppose `GAME_FORMATS.md` should be enough) containing
 - Links to assessment md documents
 - Evaluation number reflecting the potential ease of portability

Each game assessment must be in a separate MD file, we don't want to have a single spaghetti hard-to-read doc.
Each of these assessment documents must follow strict uniform pattern (template) in order to provide transparent understandable comparability
between the games. It must be crystal clear not only which criteria were used and not only how they affect the final general assessment score,
but also why and how these criteria scores were gathered.

# Successful case
`Cleopatra Fortune Plus` was successfully fan-ported to Dreamcast.

It is stored here: `../cleopatra`.

# Approach
The concrete criteria to be defined by AI after thorough brainstorming.
However, having a successful case of porting `Cleopatra Fortune Plus`, I have clear general understanding
of where to look

## RAM, VRAM, ARAM assessment via dynamic execution
In the phase 5 of `Cleopatra Fortune Plus` porting we checked if the arcade version exceeds the Dreamcast memory limits.
The main problem of porting games from Naomi to Dreamcast is memory difference, Naomi has much more memory than Dreamcast.
`Cleopatra Fortune Plus` is an ideal candidate for porting on the first place because it completely fits
the Dreamcast memory limitations. The 5th phase dynamic tests confirmed that.

We can do this memory checks preemptively. The more a game uses RAM/VRAM/ARAM, the harder it will be to port it.
A non-interactive test must be enough for initial assessment. As we see from the `Cleopatra Fortune Plus` case,
memory measurements during attraction/demo phase of the game show very much about its memory consumption.
So, as approach here I would like to run a game in our instrumented flycast, wait for it to run
for some time - show companies logo, title screen, attraction mode, instructions, etc - collect logs and assess consumption.
No humans inputs. The waiting time must, say 300-400 seconds, just like we did during `Cleopatra Fortune Plus` testing.
The metrics we need collect from this data are TBD. From the first glance, peak and average values should be enough for comparison.

One caveat to avoid. During VRAM testing of `Cleopatra Fortune Plus` we initially mistakenly assessed peak memory consumption as
9.4 mb, exceeding the Dreamcast limit. This was during the Naomi logo show time, rendered by Naomi BIOS and not the game itself.
The game itself never surpassed the Dreamcast limit and this result is just a noise. We need to avoid it during data collection
or data assessment phase.

Another possible caveat. I'm not 100% sure, but, possibly, running several instances of flycast in parallel can lead to interference.
We need either define how to clearly distinguish one run from another or don't run them in parallel at all.
Spending more time is OK if the assessment will be more precise.

# Disassembling, cart structure, etc
I can imagine a game ideally passing other checks but having inconvenient / hard-to-port guts. So, I suppose, we should also
disassemble games and check what's going on inside.

Another possible thing to assess is if the game is far from our already successful case, `Cleopatra Fortune Plus`.
Although I don't know if it is important or not and, if it is, to what extent. I also don't know if it must be
a separate criteria or get into general `guts are good for porting`.

I also suppose that we probably need to derive assets from roms and check them. I suppose, in theory,
we can find something inconvenient to port (say, an asset exceeding the whole Dreamcast VRAM) or addressed a weird way,
or packed somehow strange, or something else.

I suppose this approach can give us other details I cannot imagine right now. I need AI to think about other details
we can collect.

I suppose this approach can produce multiple criteria, it's up to AI to define what.

In order to do dissassembling and, possibly, for assets derivation, `.dat` rom format can be required. In order to convert roms to `.dat`,
we have prepared tooling. See `tools/dat-extract/README.md` for more details. Remove `.dat` once assessment is done, so we not clutter
the SSD.

## Controls
A game can be hard to port simply because of exotic controls. Just imagine, we assess `World Club Champion Football` series
and it appears that the game from memory consumption criteria is perfect, and it is very easy to adapt it to Dreamcast
from the disassembling perspective. But yet it is almost impossible to do so because of very exotic controls
(it is a card collection game). Or `Inu no Osanpo`. It is not that close to impossible, like `World Club Champion Football`,
I can imagine how we can, in theory, adapt controls to Dreamcast gamepad or even Fishing Controller,
but it still promise to be significantly more tricky than a shmup or puzzle game convertion.

So AI agent during assessment must also thoroughly google about the games' controls in order to consider this as well.

## Other metrics / criteries / approaches
The metrics / criteries / approaches described above is my vision about what must be collected.
I understand this can be not full (and with a high chance this is not full). I need AI agent to thoroughly think
about what also measure, how to measure, how to collect data and which metrics to collect.
The more precise this assessment will be, the easier the future work will be for us.

## Different criteria to a general number
There will be a lot of criteria, and they must be converted somehow to a general ease-to-port number.
I cannot say which approach to choose for that. Possibly, we need to assess each criteria separately (say, from 0 to 100) and then
sum them, or multiply, or get the biggest/smallest num, or just a separate AI agent to assess the overall result with basement
on these numbers. I don't know which approach is the best and I need AI agent to thoroughly think about it.
The more precise and descriptive it is - the better.

# Tooling

## Flycast
For dynamic testing we used instrumented flycast. Fork is here: https://github.com/CaptainKoffski/flycast4naomi2dreamcast.
Local copy is here: `../flycast4naomi2dreamcast`. Feel free to clone or use the local copy, up to you.
Please use it for dynamic assessments. If you need to add more instrumentation here - go ahead.

Regarding screenshots and video. Please, do not try to shot screenshots or video via MacOS (if it is required of course).
It is unsafe and I will not accept this. Our instrumented Flycast already can shot screenshots, so use it.
It cannot shoot videos, and I doubt it is required, but if it is, better instrument flycast.

## Disassembling
For disassembling we used Ghidra. Please use the same version as we used in `Cleopatra Fortune Plus` in order to get
uniform maps.

## Other tools
If AI agent needs any other tools - additional emulators, disassemblers, anything - go ahead, grab it and instrument if required.
We need to get deep understanding about the games and the best order and possibly approach to port them in the future.

If there is a tool an AI agent needs but cannot install or setup for some reason, it is better to ask human to do this
than default to something worse fit or dismiss a criteria / approach.

## Prepare before go
AI to check that all the tools can be run before getting to assessments
AI to prepare and instrument all the tools (to extent it is possible preemptively) before getting to assessments.
If it appears that an instrumentation or a tool is required and this understanding occurs during a game assessment,
it is OK to prepare such instrumentation and re-assess previously assessed games if necessary,
in order to get uniform result with high comparability.

# Knowledge base
If any lessons learned during preparation or games' assessments, and this information can help AI agents
in the future during porting, such info must be saved to knowledge base, in analogy with `Cleopatra Fortune Plus` repo.

# Run pre-check
The games in the `naomi` folder must be running. However, there is no guaranteed the roms in the folders are full
or can be run with flycast. Please, check if the game runs in the emulator before jumping into deep detailed analysis.
If a game cannot start, with a high chance it doesn't work at all and thus we cannot port it.
Try to understand what's the reason, if it is not in tooling but in the game itself, just skip it with corresponding
note in the games' table.

# Other
- The repo's remote is in GitHub, so as MD dialect we use `GitHub-flavoured markdown`.

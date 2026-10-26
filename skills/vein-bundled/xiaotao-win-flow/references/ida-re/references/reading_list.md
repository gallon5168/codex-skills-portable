# Reverse Engineering Reading List & References

A curated set of books and online resources for getting good at reverse engineering, with a note
on what each is best for. Point the user here when they ask how to learn or go deeper.

## Contents
- [Where to start](#where-to-start)
- [Books — foundations](#books--foundations)
- [Books — IDA & Ghidra](#books--ida--ghidra)
- [Books — malware analysis](#books--malware-analysis)
- [Books — platform-specific](#books--platform-specific)
- [Books — assembly, tooling, and exploitation](#books--assembly-tooling-and-exploitation)
- [Online resources](#online-resources)
- [Practice](#practice)
- [Primary documentation](#primary-documentation)

---

## Where to start

A reasonable path: *Practical Malware Analysis* (technique + labs) → *The IDA Pro Book* (master
the tool) → *Practical Binary Analysis* (modern foundations) → then specialize by platform
(*Windows Internals*, *The Art of Mac Malware*, *Learning Linux Binary Analysis*). Pair all of it
with constant hands-on practice on crackmes.one and the MCP's own sample dataset.

---

## Books — foundations

- **Practical Binary Analysis** — Dennis Andriesse (No Starch, 2018). Modern, Linux/ELF-centric foundation: binary formats, disassembly theory, dynamic instrumentation, taint analysis, symbolic execution. The best single "how binaries really work" book.
- **Practical Reverse Engineering** — Bruce Dang, Alexandre Gazet, Elias Bachaalany (Wiley, 2014). x86/x64/ARM, Windows kernel, and obfuscation/deobfuscation. Concise and high-signal.
- **Reversing: Secrets of Reverse Engineering** — Eldad Eilam (Wiley, 2005). The classic conceptual intro. Tooling is dated, but the mental models hold up.

## Books — IDA & Ghidra

- **The IDA Pro Book (2nd ed.)** — Chris Eagle (No Starch, 2011). The definitive IDA reference: navigation, types, FLIRT, scripting/IDAPython, the SDK. Older than IDA 9 but still the canonical text on how IDA thinks.
- **The Ghidra Book** — Chris Eagle & Kara Nance (No Starch, 2020). Definitive Ghidra guide; useful cross-tool even for IDA users (concepts transfer; includes an "Appendix: Ghidra for IDA Users").
- **Ghidra Software Reverse Engineering for Beginners (2nd ed.)** — David Álvarez Pérez & Ravikant Tiwari (Packt, 2024). Current; headless mode, scripting/automation, plugins, kernel debugging, binary diffing, modern ransomware.

## Books — malware analysis

- **Practical Malware Analysis** — Michael Sikorski & Andrew Honig (No Starch, 2012). The field's standard text. Static + dynamic, anti-analysis, with an excellent set of hands-on labs. Start here for malware.
- **Evasive Malware** — Kyle Cucci (No Starch, 2024). Very current, focused on anti-analysis, anti-debugging, sandbox evasion, and how to defeat them. Excellent complement to PMA.
- **Learning Malware Analysis** — Monnappa K A (Packt, 2018). Hands-on, includes memory forensics with Volatility.
- **Malware Analysis and Detection Engineering** — Abhijit Mohanta & Anoop Saldanha (Apress, 2020). Broad coverage from triage to detection engineering.
- **The Art of Memory Forensics** — Ligh, Case, Levy, Walters (Wiley, 2014). Adjacent but invaluable for analyzing what malware does in memory.

## Books — platform-specific

- **Windows Internals, Parts 1 & 2 (7th ed.)** — Russinovich, Solomon, Ionescu, Allievi (Microsoft Press). Essential background for any serious Windows RE: processes, memory, the object manager, the Native API. A reference, not a read-through.
- **The Art of Mac Malware, Vol. 1: Analysis** — Patrick Wardle (No Starch, 2022). The book for macOS RE/malware; Mach-O, Objective-C, persistence. Freely readable online (taomm.org).
- **Learning Linux Binary Analysis** — Ryan "elfmaster" O'Neill (Packt, 2016). Deep ELF internals, ptrace, process memory, ELF viruses/forensics.
- **Rootkits and Bootkits** — Alex Matrosov, Eugene Rodionov, Sergey Bratus (No Starch, 2019). Firmware, bootkits, and kernel-mode RE; modern and rigorous.

## Books — assembly, tooling, and exploitation

*(Exploitation titles here are for understanding the vulnerabilities you discover, not for building weaponized exploits.)*

- **Modern X86 Assembly Language Programming** — Daniel Kusswurm (Apress), or **Assembly Language for x86 Processors** — Kip Irvine. Solidify x86/x64 (and SIMD) fundamentals.
- **Black Hat Python (2nd ed.)** — Justin Seitz & Tim Arnold (No Starch, 2021). Building your own RE/security tooling in Python.
- **Game Hacking** — Nick Cano (No Starch, 2016). A surprisingly good, hands-on path into dynamic analysis, memory scanning, and hooking.
- **The Antivirus Hacker's Handbook** — Joxean Koret & Elias Bachaalany (Wiley, 2015). RE applied to AV internals.
- **Hacking: The Art of Exploitation (2nd ed.)** — Jon Erickson (No Starch, 2008). Classic foundations linking C, assembly, and memory-corruption concepts.
- **The Shellcoder's Handbook (2nd ed.)** — Anley, Heasman, Lindner, Richarte (Wiley, 2007). Deeper on vulnerability classes.
- **A Bug Hunter's Diary** — Tobias Klein (No Starch, 2011). Real vulnerability-discovery walkthroughs.

---

## Online resources

- **mrexodia/ida-pro-mcp** — github.com/mrexodia/ida-pro-mcp. The MCP server this skill targets: README, prompt-engineering notes, and the companion **mcp-reversing-dataset** repo of sample binaries and prompts for practice.
- **onethawt/reverseengineering-reading-list** — github.com/onethawt/reverseengineering-reading-list. A large, well-maintained index of RE articles, books, papers, and tools.
- **Hex-Rays documentation & IDAPython API** — docs.hex-rays.com. Authoritative reference for IDA, the decompiler, FLIRT/Lumina, and the IDAPython API you'll use via `py_eval`. The Hex-Rays blog has deep decompiler/scripting posts.
- **OALabs (OpenAnalysis)** — youtube + openanalysis.net. Practical, current malware RE walkthroughs and tooling; one of the best free resources for real-world technique.
- **MalwareUnicorn workshops** — malwareunicorn.org/workshops (RE101 / RE102). Excellent structured introductions.
- **MalwareTech** — malwaretech.com. Beginner-friendly malware RE challenges and courses.
- **Azeria Labs** — azeria-labs.com. The go-to for ARM/ARM64 assembly and exploitation.
- **Compiler Explorer** — godbolt.org. See exactly how source compiles to assembly across compilers/flags; the fastest way to build "what does this pseudocode pattern come from" intuition.
- **Mandiant/Google FLARE tooling** — `capa` (capability detection from binaries) and `FLOSS` (automatic string deobfuscation) pair extremely well with IDA during triage.
- **Helper libraries** — `capstone` (disassembly), `unicorn` (CPU emulation, great for solving decoders), `LIEF`/`pefile` (binary parsing). Useful from `py_eval` or alongside IDA.

## Practice

- **crackmes.one** — graded crackmes from beginner to brutal; the standard practice ground.
- **mcp-reversing-dataset** (mrexodia) — purpose-built to exercise an MCP-driven workflow.
- **ROP Emporium**, **pwn.college**, **Nightmare** — exploitation/RE practice; the RE portions sharpen static and dynamic skills.
- **Flare-On Challenge** — Mandiant's annual RE CTF; past challenges + write-ups are a goldmine.

## Primary documentation

When you need ground truth on instructions, ABIs, or formats:

- **Intel® 64 and IA-32 Architectures Software Developer's Manuals (SDM)** — instruction semantics for x86/x64.
- **ARM Architecture Reference Manuals** — AArch32/AArch64 instruction and system reference.
- **System V AMD64 ABI** — the Linux/macOS x64 calling convention and object model.
- **Microsoft x64 calling convention / ABI docs** — the Windows x64 convention, shadow space, unwind data.
- **PE/COFF specification** (Microsoft), **ELF / System V ABI** (Tool Interface Standard), **Mach-O** (Apple) — the binary container formats you'll be parsing.

# 🛡️ Cybersecurity Threat Intelligence Log

This repository tracks real-world cybersecurity threats,
vulnerabilities, and exploitation activity for continuous learning.

---
## 📅 2026-10-23

### 📰 Critical Flaw in Python’s Popular Pillow Image Library Allows Code Execution via a Crafted Image
**Category:** 🔴 Vulnerability
**Time:** 11:20 UTC

**Summary:**  
Pillow, the most widely used image library for Python, can be made to run operating system commands on a server by specifying the name of a file it is told to open.  The flaw,&nbsp;CVE-2026-112900, is in the way Pillow handles EPS images, which it opens by passing the file's name to Ghostscript, a separate program it runs to turn the image into pixels, without checking the name first.

🔗 [Read Full Article](https://thehackernews.com/2026/10/critical-flaw-in-pythons-popular-pillow.html)


---

### 📰 Researchers Demonstrate Node2Shell RCE Exploit on Node.js Build Using Crafted Brotli Data
**Category:** 🔴 Vulnerability
**Time:** 11:20 UTC

**Summary:**  
Malicious Brotli data can make an application on an official build of Node.js run attacker-supplied code, security researchers at Imperva have&nbsp;demonstrated.  Their "Node2Shell" proof of concept ran code on the official Node.js 24.22.0 image for Linux arm64, with no debugger or custom build, by feeding crafted data to the bundled Brotli decoder (CVE-2026-111497). Node.js disclosed the flaw

🔗 [Read Full Article](https://thehackernews.com/2026/10/researchers-demonstrate-node2shell-rce.html)


---

### 📰 Critical x402 SDK Flaw Could Let Malicious APIs Drain AI Agents’ Token Balances
**Category:** 📰 News
**Time:** 11:20 UTC

**Summary:**  
AI agents paying for API calls with the&nbsp;x402 SDKs&nbsp;could sign a payment for their full balance of a supported token if a malicious API asked for it,&nbsp;security firm V12 said&nbsp;on October 22.  The cause was the SDKs' default client, which set no spending limit until releases on August 18 added one. The risk was limited to agents who automatically signed payments and whose apps set

🔗 [Read Full Article](https://thehackernews.com/2026/10/critical-x402-sdk-flaw-could-let.html)


---

### 📰 PHP2Shell Exploit Attempts Hit Millions as Attackers Try to Deploy Mirai Malware
**Category:** 🔴 Vulnerability
**Time:** 11:20 UTC

**Summary:**  
Threat actors have been observed unsuccessfully attempting to exploit the newly disclosed PHP2Shell vulnerabilities to rope infected systems into a Mirai botnet variant called Potassium, as it emerges that weaponizing the flaws may be harder than previously thought.  The attacks aim to exploit CVE-2026-109618 and CVE-2026-109619 (CVSS scores: 9.2), which can result in unauthenticated remote

🔗 [Read Full Article](https://thehackernews.com/2026/10/php2shell-exploit-attempts-hit-millions.html)


---


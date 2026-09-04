<!-- Public GitHub profile README. Keep client names, private repo names and deployment details out. -->

<picture>
  <source media="(max-width: 600px)" srcset="assets/profile-hero-mobile.svg">
  <img src="assets/profile-hero.svg" alt="MZS, practical systems builder in Perth, Western Australia">
</picture>

<div align="center">

# Mark S

**15 years helping people feel confident with their technology, the handyman of digital integrations.**

Former integrator, somehow now a hands-on developer. I build and repair systems for
real work: web apps, automation, self-hosted infrastructure, geospatial tools,
digital signage and recovery paths.

**[Portfolio and CV](https://mzs.au)**

</div>

---

## What I build

I am usually at my best where software meets the awkward bit: existing hardware,
inherited systems, valuable data, or a workflow that has outgrown the tools around it.

- **Product and automation:** web tools, dashboards, sign-in, reporting, scheduling and browser extensions.
- **Geospatial and field data:** drone and LiDAR portals, photogrammetry, 3D Tiles and WebGL viewers.
- **Platforms and infrastructure:** self-hosted AI, Linux, Docker, Cloudflare, Nextcloud and release pipelines.
- **Recovery and handover:** inherited code, data recovery, release packaging and documentation people can use.

## Selected public work

These are the useful public pieces I can show. Where a project builds on someone
else's work, I say so.

<h3><a href="https://github.com/msegec/t3code_rookie">T3 Code: features and releases</a></h3>

My active fork tracks a fast-moving upstream desktop app while keeping the features I
use. Its [release workflow](https://github.com/msegec/t3code_rookie/blob/main/.github/workflows/mzs-fleet-build.yml)
restacks the changes, runs the checks, then publishes checksum-backed Linux and macOS
builds with updater metadata.

Public product proposals include
[project accents](https://github.com/pingdotgg/t3code/pull/7972),
[file uploads](https://github.com/pingdotgg/t3code/pull/8151) and
[repository discovery](https://github.com/pingdotgg/t3code/pull/8329). They show the
other side of the work: interface details, persistence, failure paths and regression
coverage.

<h3><a href="https://github.com/Ylianst/MeshAgent/pull/390">MeshAgent Linux session fix</a></h3>

A small upstream proposal after reproducing a remote desktop failure caused by
multiple active `logind` sessions. The two-line patch selects the real graphical
session instead of the display-less user manager.

<h3><a href="https://github.com/msegec/odysseus-hmm">Odysseus safety telemetry</a></h3>

An experiment on a self-hosted AI workspace. Three focused commits add observe-only
traffic classifiers, provenance logging, admin endpoints and standard-library tests
without turning the safety layer into a blocker.

<h3><a href="https://github.com/msegec/threedtilesviewer">Nextcloud 3D Tiles viewer</a></h3>

An original work-in-progress prototype joining Nextcloud file access with browser-based
3D Tiles rendering, mobile layouts, coordinate handling and compressed geometry.

## How I work

- Start with the real workflow.
- Ship a small working slice, then improve it.
- Prefer systems the owner can control and understand.
- Treat tests, logs, screenshots and release files as part of the handover.
- Keep private names, hosts and deployment details private.

## Toolbox

**Languages:** `TypeScript` `JavaScript` `Python` `PHP` `Go` `Swift` `Kotlin` `C` `C++`

**Web and data:** `Node.js` `Astro` `WebGL` `3D Tiles` `WordPress` `SQL`

**Systems:** `Linux` `Docker` `Cloudflare` `Nextcloud` `GitHub Actions` `Raspberry Pi` `Orange Pi`

The stack changes with the job. The preference does not: boring enough to understand,
visible enough to debug, and owned by the person who has to live with it.

## Recent GitHub activity

<!-- Refresh this block and both SVGs with python3 scripts/update-github-activity.py. -->
<!-- activity:start -->
**2,895 contributions** across **107 active days**, with a **41-day current streak**. **2,869 private contributions** appear only as aggregate counts. Public activity includes **7 commits** and **8 pull requests**.

<picture>
  <source media="(max-width: 600px)" srcset="assets/github-activity-mobile.svg">
  <img src="assets/github-activity.svg" alt="GitHub contribution calendar for the 12 months to 4 September 2026">
</picture>

<sub>GitHub API snapshot: 4 September 2026 at 13:02 AWST. Private repository, client, host and deployment details are omitted.</sub>
<!-- activity:end -->

## What I am working on

Right now I am hardening local AI tooling, desktop release systems and small Linux
machines that need to run unattended. Geospatial viewers and operational web tools
remain the longer thread.

For the fuller work history, projects and contact details, visit **[mzs.au](https://mzs.au)**.

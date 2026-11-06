# Source compilation (Meteor + Baritone)

This repository's `files/` directory is a **binary archive**; those JARs do not contain the full buildable source projects. Original historical JARs are preserved unchanged.

## Compile upstream source on GitHub Actions

Open **Actions → Build Meteor and Baritone from source → Run workflow**. Pick `meteor`, `baritone` or `both`, then enter an upstream **branch, tag, or commit** for each selected project. Choose **Run workflow**. Completed JARs appear under the run's **Artifacts** section as ZIP files. The workflow never replaces existing archived JARs automatically.

| Project | Source | Examples of refs | Build JDK for inspected current branches |
| --- | --- | --- | --- |
| Meteor Client | [MeteorDevelopment/meteor-client](https://github.com/MeteorDevelopment/meteor-client) | `master`, `1.21.11`, `1.21.10` | 25 |
| Baritone | [cabaletta/baritone](https://github.com/cabaletta/baritone) | `1.21.11`, `1.21.10`, `1.20.1`, `1.16.5` | 21 |

For Baritone old branches, the workflow chooses a *starting* JDK by the branch name. Older Gradle/Forge configurations are not guaranteed to compile on modern CI; check logs and adjust the toolchain or pin a compatible Gradle distribution per ref.

For Meteor historical Minecraft releases, **do not change just the Minecraft version property** and expect a successful backport: each historic release needs its matching source commit, mappings and dependencies. Not all historical release commits are represented by upstream branches or tags. A JAR alone is not sufficient to reconstruct reproducible source. Use `git log` or upstream release history to locate a matching commit and enter its SHA.

## Version and provenance rules

- Never label a JAR for a Minecraft version without verifying its loader metadata and launching it with that exact Minecraft/loader combination.
- GitHub Actions compilation does not prove runtime compatibility; test builds in a separate Minecraft installation.
- Current Meteor and Baritone do **not** need to be compiled together as one project; choose matching compatible Minecraft versions and loaders.
- Keep existing `files/` artifacts intact, including `extra/`. Upload any newly verified, legally distributable artifacts separately, documenting upstream commit SHA and the SHA-256 checksum.
- Only use builds where authorized, and respect the upstream project licenses and servers' policies.

This first workflow provides **on-demand compilation**, not an exhaustive rebuild of every historical version and not an automatic scheduled sync.


The archive's master branch now stores JARs in `meteor/<loader>/<minecraft-version>/` and `baratone/<loader>/<minecraft-version>/`. GitHub Actions artifacts must be verified and deliberately committed to those folders; an artifact download is not automatically a repository file. Source branches do not exist for every historical Minecraft release.

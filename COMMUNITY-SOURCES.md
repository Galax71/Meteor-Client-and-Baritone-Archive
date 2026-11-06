# Additional community archive sources

The official upstream repositories remain the primary compilation sources. The following public archives were discovered on GitHub and are **candidates only**, not automatically trusted source revisions:

| Repository | Observed content | Use |
|---|---|---|
| [ManInMyVan/meteor-archive](https://github.com/ManInMyVan/meteor-archive) | Historical JAR archive (152 JAR paths observed) | Compare Minecraft version coverage; inspect binaries and licensing before any import |
| [ModxVoldHunter/meteor-client-archive](https://github.com/ModxVoldHunter/meteor-client-archive) | Source tree with Gradle build files | Investigate historical source commits, verify origin and changes before building |
| [ShlokTheAmazing/MeteorClientArchive](https://github.com/ShlokTheAmazing/MeteorClientArchive) | Search result; contents not verified | Inspect before use |
| [purpleceilingstars/meteor-archive-and-Baritone-archive](https://github.com/purpleceilingstars/meteor-archive-and-Baritone-archive) | Similar binary archive (102 JAR paths observed) | Compare completeness; may duplicate this repository |

## Safety and provenance rules

1. Do not execute arbitrary build scripts from an unverified third-party archive automatically. Check source commits, licensing, modifications, and Gradle scripts first.
2. Do not treat archived binary JARs as newly compiled source builds.
3. Record origin URL, source commit SHA, Minecraft version, loader, SHA-256 and whether runtime testing was performed for each imported build.
4. Preserve original archive JARs and do not overwrite version folders with conflicting files.
5. Never claim all historical Minecraft versions are supported without evidence.

The existing `build-matrix.json` intentionally uses verified official upstream branch names only. Community sources can be added to that matrix after provenance review and build validation.

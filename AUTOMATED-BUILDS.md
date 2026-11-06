# Automated source-version compilation

Run **Actions → Compile full source-version matrix → Run workflow**. Choose `all`, `meteor`, or `baratone`. By default, outputs remain downloadable workflow artifacts; enable **publish** to commit new successful loader JARs to `master`.

The [build-matrix.json](build-matrix.json) manifest lists *confirmed existing upstream branches*, not every Minecraft version ever released. Extend it with **verified** source refs and matching JDK versions. A branch may exist yet fail to build because its historical dependencies or Gradle wrapper are no longer available.

- Builds run independently with `fail-fast: false`; one failure does not cancel others.
- The collector checks that each JAR is a readable ZIP and contains loader metadata. This is **structural validation, not a Minecraft launch/runtime test**.
- Baritone's current multi-loader Gradle builds can emit Fabric, Forge, and NeoForge JARs; only loader-labelled and metadata-bearing JARs are collected. Older branches can require separate `-Pbaritone.fabric_build` or `-Pbaritone.forge_build` commands and may fail this workflow.
- The archive stores new files at `meteor/fabric/<minecraft-version>/` and `baratone/<loader>/<minecraft-version>/`, preserving any existing files.
- The scheduled monthly run compiles but **does not publish**. Manual publish requires opting in.
- Successful Actions builds do not establish that every loader/Minecraft version works in-game. Test manually before advertising runtime support.
- GitHub-hosted runner quotas, artifact retention, storage limits and repository permissions apply. Binary publishing to Git can increase repository size substantially.
- The previous manual `build-upstream.yml` remains available for custom refs.

Sources: https://github.com/MeteorDevelopment/meteor-client and https://github.com/cabaletta/baritone

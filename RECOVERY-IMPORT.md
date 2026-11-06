# Recovered JAR imports

The [Recover historical JARs](.github/workflows/recover-found.yml) GitHub Actions workflow runs on updates to the importer or manually using **Actions → Recover historical JARs → Run workflow**.

Files are stored in `source/<original-site>/<mod>/<loader>/<minecraft-version>/<original-filename>.jar`.

Currently configured discovery sources:
- [Baritone official GitHub releases](https://github.com/cabaletta/baritone/releases), with exact Minecraft release-description mapping and Forge, Fabric, NeoForge, standalone variants.
- [ManInMyVan historical archive](https://github.com/ManInMyVan/meteor-archive), using documented historical Minecraft-version mapping.

The [Meteor official archive](https://meteorclient.com/archive), Internet Archive, and Wayback Machine remain research leads and **are not automatically imported** by this initial importer. Never infer that a source was downloaded just because it is linked in the README.

The workflow verifies JAR/ZIP structure and available official SHA256 digests, writes `RECOVERED-SOURCES.json`, and commits successfully downloaded files. These are **not** malware-scanned or game-launch-tested. Third-party files should be treated as untrusted. Existing archive folders remain unchanged. GitHub Actions must be enabled and its token must have write access for automatic commits.

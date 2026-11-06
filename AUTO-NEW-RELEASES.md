# Automatic new-release downloads

The [Recover historical JARs](.github/workflows/recover-found.yml) workflow runs **daily at 07:17 UTC**, as well as manually and when importer files change. GitHub Actions scheduled runs can be delayed, and GitHub may disable schedules after prolonged repository inactivity.

Each run checks the official Baritone GitHub releases and the ManInMyVan historical community archive for new JARs, plus curated entries in `EXTERNAL-DOWNLOADS.json`. New downloads are stored under `source/<website>/<mod>/<loader>/<minecraft-version>/` and recorded in `RECOVERED-SOURCES.json`.

Existing exact destination filenames are skipped without redownloading. JAR ZIP structure is checked and SHA-256 recorded; release asset SHA-256 is verified when supplied. A successful run does not guarantee every release is supported or imported.

**Limitations:** This does not yet automatically discover new Meteor Client releases from meteorclient.com or new Internet Archive uploads. Community archive version mappings are historical and may not include future Meteor versions. For truly complete coverage, additional verified official-source discovery adapters are required. No new binaries are claimed imported by this workflow edit alone.

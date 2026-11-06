# External download sources

Add verified direct HTTPS JAR URLs to `EXTERNAL-DOWNLOADS.json`, including official sites, Internet Archive item downloads, or other mod distribution sites. Each entry needs `url`, `mod`, `loader`, `minecraft_version`, `filename`, and optionally `sha256`. The workflow imports them under `source/<website>/<mod>/<loader>/<version>/` and records SHA-256 and URL in `RECOVERED-SOURCES.json`.

The list is currently empty: no independent website JAR URL has been verified for inclusion. Search pages are not direct downloads. Only add authorized mod releases, and validate file origin and compatibility before use.

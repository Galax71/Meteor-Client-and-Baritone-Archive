# Independent website recovery

The scheduled recovery importer now discovers official download URLs from [meteorclient.com/archive](https://meteorclient.com/archive) on every run. It follows only the official site's `/api/download` and `/api/downloadBaritone` links with explicit Minecraft versions. Files are saved under `source/meteorclient.com/<mod>/fabric/<version>/`, with URL and SHA-256 recorded in `RECOVERED-SOURCES.json`.

The [Meteor Archive independent website](https://meteorarchive.github.io/) advertises Discord CDN links for 1.19.3, 1.19.4 and 1.20.1, but these links have not been confirmed live or safe; they are not automatically executed as trusted downloads.

Additional independent sites discovered during research include [baritoneclient.net](https://www.baritoneclient.net/), [baritonebot.github.io](https://baritonebot.github.io/download/) and [baritonemc.net](https://baritonemc.net/download/). Their custom or third-party JARs are **not automatically imported**, because authenticity and loader/version metadata are unverified. A website merely listing a Minecraft version does not prove that its binary supports that version.

Verified direct URLs from additional websites can be added to `EXTERNAL-DOWNLOADS.json`. The importer validates ZIP/JAR structure and records hashes; that does not establish binary safety or in-game compatibility. The latest workflow run must finish before any new imports can be claimed.

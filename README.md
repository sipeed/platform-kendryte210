# platform-kendryte210
[![Build Status](https://api.travis-ci.org/sipeed/platform-kendryte210.svg?branch=master)](https://travis-ci.org/sipeed/platform-kendryte210)
[![Build status](https://ci.appveyor.com/api/projects/status/s78chv6nek6s30nm?svg=true)](https://ci.appveyor.com/project/Zepan/platform-kendryte210)

# Usage

1. [Install PlatformIO](http://platformio.org)
2. Create PlatformIO project and configure a platform option in [platformio.ini](http://docs.platformio.org/page/projectconf.html) file:

## Stable version

```ini
[env:stable]
platform = kendryte210
board = ...
...
```

## Development version

```ini
[env:development]
platform = https://github.com/sipeed/platform-kendryte210.git
board = ...
...
```

# Configuration

Please navigate to [documentation](http://docs.platformio.org/page/platforms/kendryte210.html).

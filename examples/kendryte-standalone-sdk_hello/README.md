How to build PlatformIO based project
=====================================

1. [Install PlatformIO Core](https://docs.platformio.org/page/core.html)
2. Download [development platform with examples](https://github.com/sipeed/platform-kendryte210/archive/master.zip)
3. Extract ZIP archive
4. Run these commands:

```shell
# Change directory to example
$ cd platform-kendryte210/examples/kendryte-standalone-sdk_hello

# Build project
$ pio run

# Upload firmware
$ pio run --target upload

# Build specific environment
$ pio run -e sipeed-maix-go

# Upload firmware for the specific environment
$ pio run -e sipeed-maix-go --target upload

# Clean build files
$ pio run --target clean
```

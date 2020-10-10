from os.path import isdir, join

from SCons.Script import DefaultEnvironment

env = DefaultEnvironment()

FRAMEWORK_DIR = env.PioPlatform().get_package_dir("framework-kendryte-freertos-sdk")
assert FRAMEWORK_DIR and isdir(FRAMEWORK_DIR)

TOOLCHAIN_DIR = env.PioPlatform().get_package_dir("toolchain-kendryte210")
assert TOOLCHAIN_DIR and isdir(TOOLCHAIN_DIR)

env.SConscript("_bare.py", exports="env")

env.Replace(

    ASFLAGS = ["-x", "assembler-with-cpp"],

    CCFLAGS = [
        "-mcmodel=medany",
        "-mabi=lp64f",
        "-march=rv64imafc",
        "-fno-common",
        "-ffunction-sections",
        "-fdata-sections",
        "-fstrict-volatile-bitfields",
        "-ffast-math",
        "-fno-math-errno",
        "-fsingle-precision-constant",
        "-O2",
        "-ggdb",
        "-Wall",
        "-Werror=all",
        "-Wno-error=unused-function",
        "-Wno-error=unused-but-set-variable",
        "-Wno-error=unused-variable",
        "-Wno-error=deprecated-declarations",
        "-Wno-error=maybe-uninitialized",
        "-Wextra",
        "-Werror=frame-larger-than=65536",
        "-Wno-unused-parameter",
        "-Wno-unused-function",
        "-Wno-implicit-fallthrough",
        "-Wno-sign-compare",
        "-Wno-error=missing-braces",
        "-Wno-error=return-type",
        "-Wno-error=pointer-sign",
        "-Wno-missing-braces",
        "-Wno-strict-aliasing",
        "-Wno-implicit-fallthrough",
        "-Wno-missing-field-initializers",
        "-Wno-int-to-pointer-cast",
        "-Wno-error=comment",
        "-Wno-error=logical-not-parentheses",
        "-Wno-error=duplicate-decl-specifier",
        "-Wno-error=parentheses",
        "-Wno-error=maybe-uninitialized"
    ]
)

env.Append(

    ASFLAGS=env.get("CCFLAGS", [])[:],

    LINKFLAGS = [
        "-Wl,--start-group",
        "-lc",
        "-lgcc",
        "-lm",
        "-Wl,--end-group",
        join(TOOLCHAIN_DIR, "lib", "gcc", "riscv64-unknown-elf", "8.2.0", "crti.o"),
        join(TOOLCHAIN_DIR, "lib", "gcc", "riscv64-unknown-elf", "8.2.0", "crtbegin.o"),
    ],

    CPPPATH = [
        join(FRAMEWORK_DIR, "lib", "arch", "include"),
        join(FRAMEWORK_DIR, "lib", "bsp"),
        join(FRAMEWORK_DIR, "lib", "bsp", "include"),
        join(FRAMEWORK_DIR, "lib", "bsp", "config"),
        join(FRAMEWORK_DIR, "lib", "bsp", "device"),
        join(FRAMEWORK_DIR, "lib", "bsp", "syscalls"),
        join(FRAMEWORK_DIR, "lib", "drivers"),
        join(FRAMEWORK_DIR, "lib", "drivers", "src", "misc", "ws2812b"),
        join(FRAMEWORK_DIR, "lib", "drivers", "src", "network"),
        join(FRAMEWORK_DIR, "lib", "drivers", "src", "storage"),
        join(FRAMEWORK_DIR, "lib", "drivers", "include"),
        join(FRAMEWORK_DIR, "lib", "drivers", "include", "misc", "ws2812b"),
        join(FRAMEWORK_DIR, "lib", "drivers", "include", "network"),
        join(FRAMEWORK_DIR, "lib", "drivers", "include", "storage"),
        join(FRAMEWORK_DIR, "lib", "freertos"),
        join(FRAMEWORK_DIR, "lib", "freertos", "conf"),
        join(FRAMEWORK_DIR, "lib", "freertos", "include"),
        join(FRAMEWORK_DIR, "lib", "freertos", "include", "kernel"),
        join(FRAMEWORK_DIR, "lib", "freertos", "portable"),
        join(FRAMEWORK_DIR, "lib", "hal"),
        join(FRAMEWORK_DIR, "lib", "hal", "include"),
        join(FRAMEWORK_DIR, "lib", "posix"),
        join(FRAMEWORK_DIR, "lib", "posix", "include"),
        join(FRAMEWORK_DIR, "lib", "utils", "include"),
        join(FRAMEWORK_DIR, "third_party", "fatfs", "source"),
        join(FRAMEWORK_DIR, "third_party", "lwip", "src", "include"),
        join(FRAMEWORK_DIR, "third_party")
    ],

    LIBS = [
        "c", "gcc", "m", "stdc++", "atomic"
    ]

)

if not env.BoardConfig().get("build.ldscript", ""):
    env.Replace(LDSCRIPT_PATH=join(FRAMEWORK_DIR, "lds", "kendryte.ld"))

env.Append(CRTEND=[
    join(TOOLCHAIN_DIR, "lib", "gcc", "riscv64-unknown-elf", "8.2.0", "crtend.o"),
    join(TOOLCHAIN_DIR, "lib", "gcc", "riscv64-unknown-elf", "8.2.0", "crtn.o")
])

env.Append(LINKCOM=" $CRTEND")

#
# Target: Build Core Library
#

libs = [
    env.BuildLibrary(
        join("$BUILD_DIR", "sdk-bsp"),
        join(FRAMEWORK_DIR, "lib", "bsp")),

    env.BuildLibrary(
        join("$BUILD_DIR", "sdk-drivers"),
        join(FRAMEWORK_DIR, "lib", "drivers")),

    env.BuildLibrary(
        join("$BUILD_DIR", "sdk-freertos"),
        join(FRAMEWORK_DIR, "lib", "freertos")),

    env.BuildLibrary(
        join("$BUILD_DIR", "sdk-hal"),
        join(FRAMEWORK_DIR, "lib", "hal")),

    env.BuildLibrary(
        join("$BUILD_DIR", "sdk-posix"),
        join(FRAMEWORK_DIR, "lib", "posix")),

    env.BuildLibrary(
        join("$BUILD_DIR", "third_party-fatfs"),
        join(FRAMEWORK_DIR, "third_party", "fatfs", "source")),

    env.BuildLibrary(
        join("$BUILD_DIR", "third_party-lwipcore"),
        join(FRAMEWORK_DIR, "third_party", "lwip", "src", "core")),
        
    env.BuildLibrary(
        join("$BUILD_DIR", "third_party-lwipapi"),
        join(FRAMEWORK_DIR, "third_party", "lwip", "src", "api")),

    env.BuildLibrary(
        join("$BUILD_DIR", "third_party-lwiparch"),
        join(FRAMEWORK_DIR, "third_party", "lwip", "src", "arch")),

    env.BuildLibrary(
        join("$BUILD_DIR", "third_party-lwipnetif"),
        join(FRAMEWORK_DIR, "third_party", "lwip", "src", "netif")),
]

env.Prepend(LIBS=libs)

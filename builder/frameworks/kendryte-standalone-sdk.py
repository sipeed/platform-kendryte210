

from os.path import isdir, join

from SCons.Script import DefaultEnvironment

env = DefaultEnvironment()

FRAMEWORK_DIR = env.PioPlatform().get_package_dir("framework-kendryte-standalone-sdk")
assert FRAMEWORK_DIR and isdir(FRAMEWORK_DIR)
TOOLCHAIN_DIR = env.PioPlatform().get_package_dir("toolchain-kendryte210")
assert TOOLCHAIN_DIR and isdir(TOOLCHAIN_DIR)

env.SConscript("_bare.py", exports="env")

env.Append(

    CCFLAGS = [
        "-ffast-math",
        "-fno-math-errno",
        "-fsingle-precision-constant",
    ],

    CPPDEFINES = [
        ("NNCASE_TARGET", "k210"),
        "TCB_SPAN_NO_EXCEPTIONS",
        "TCB_SPAN_NO_CONTRACT_CHECKING"
    ],

    LINKFLAGS = [
        "-Wl,--start-group",
        # explicitly add C runtime initialization and end like SDK, otherwise "undefined reference to `__dso_handle'"
        join(TOOLCHAIN_DIR, "lib", "gcc", "riscv64-unknown-elf", "8.2.0", "crti.o"),
        join(TOOLCHAIN_DIR, "lib", "gcc", "riscv64-unknown-elf", "8.2.0", "crtbegin.o"),
        "-lgcc",
        "-lm",
        "-lc",
        join(TOOLCHAIN_DIR, "lib", "gcc", "riscv64-unknown-elf", "8.2.0", "crtend.o"),
        join(TOOLCHAIN_DIR, "lib", "gcc", "riscv64-unknown-elf", "8.2.0", "crtn.o"),
        "-Wl,--end-group",
    ],

    CPPPATH = [
        join(FRAMEWORK_DIR, "lib", "bsp"),
        join(FRAMEWORK_DIR, "lib", "bsp", "include"),
        join(FRAMEWORK_DIR, "lib", "drivers"),
        join(FRAMEWORK_DIR, "lib", "drivers", "include"),
        join(FRAMEWORK_DIR, "lib", "freertos"),
        join(FRAMEWORK_DIR, "lib", "freertos", "include"),
        join(FRAMEWORK_DIR, "lib", "freertos", "portable"),
        join(FRAMEWORK_DIR, "lib", "freertos", "conf"),
        join(FRAMEWORK_DIR, "lib", "utils", "include"),
        join(FRAMEWORK_DIR, "lib", "nncase"),
        join(FRAMEWORK_DIR, "lib", "nncase", "include"),
        join(FRAMEWORK_DIR, "lib", "nncase", "v0"),
        join(FRAMEWORK_DIR, "lib", "nncase", "v0", "include"),
        join(FRAMEWORK_DIR, "lib", "nncase", "v1"),
        join(FRAMEWORK_DIR, "lib", "nncase", "v1", "include"),
        join(FRAMEWORK_DIR, "lib", "nncase", "include"),
        join(FRAMEWORK_DIR, "third_party", "xtl", "include"),
        join(FRAMEWORK_DIR, "third_party", "gsl-lite", "include"),
        join(FRAMEWORK_DIR, "third_party", "mpark-variant", "include"),
        join(FRAMEWORK_DIR, "third_party", "nlohmann_json", "include")
    ],

    LIBPATH = [
        join(FRAMEWORK_DIR, "lib", "nncase", "v1", "lib"),
    ],

    LIBS = [
       "gcc", "m", "c", "nncase.runtime", "nncase.rt_modules.k210", "stdc++",
    ]

)

if not env.BoardConfig().get("build.ldscript", ""):
    env.Replace(LDSCRIPT_PATH=join(FRAMEWORK_DIR, "lds", "kendryte.ld"))

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
        join("$BUILD_DIR", "nncase"),
        join(FRAMEWORK_DIR, "lib", "nncase")),
]

env.Prepend(LIBS=libs)
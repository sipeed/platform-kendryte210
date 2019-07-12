

from os.path import isdir, join

from SCons.Script import DefaultEnvironment

env = DefaultEnvironment()

FRAMEWORK_DIR = env.PioPlatform().get_package_dir("framework-kendryte-standalone-sdk")
assert FRAMEWORK_DIR and isdir(FRAMEWORK_DIR)

env.SConscript("_bare.py", exports="env")

env.Append(

    LINKFLAGS = [
        "-Wl,--start-group",
        "-lc",
        "-lgcc",
        "-lm",
        "-Wl,--end-group"
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
    ],

    LIBPATH = [

    ],

    LIBS = [
        "c", "gcc", "m"
    ]

)

env.Replace(
    LDSCRIPT_PATH = join(FRAMEWORK_DIR,"lds","kendryte.ld")
)

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
]

env.Prepend(LIBS=libs)
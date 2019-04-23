

from os.path import isdir, join 

from SCons.Script import DefaultEnvironment

env = DefaultEnvironment()

FRAMEWORK_DIR = env.PioPlatform().get_package_dir("framework-kendryte210-standalone-sdk")
assert FRAMEWORK_DIR and isdir(FRAMEWORK_DIR)

env.SConscript("_bare.py", exports="env")

env.Append(

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
        join(FRAMEWORK_DIR, "lib", "freertos", "portable"),
        join(FRAMEWORK_DIR, "lib", "freertos", "conf"),
        join(FRAMEWORK_DIR, "lib", "freertos", "include"),
        join(FRAMEWORK_DIR, "lib", "utils", "include"),
        join(FRAMEWORK_DIR, "lib", "bsp", "include"),
        join(FRAMEWORK_DIR, "lib", "drivers", "include"),
    ]
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
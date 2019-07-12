

from os.path import isdir, join 

from SCons.Script import DefaultEnvironment

env = DefaultEnvironment()

FRAMEWORK_DIR = env.PioPlatform().get_package_dir("framework-maixduino")
assert FRAMEWORK_DIR and isdir(FRAMEWORK_DIR)
SDK_DIR = join(FRAMEWORK_DIR, "cores", "arduino", "kendryte-standalone-sdk")

env.SConscript("_bare.py", exports="env")

env.Append(

    CCFLAGS = [
        "-Wno-error=unused-const-variable",
        "-Wno-error=narrowing",
        "-Wno-error=unused-value"
    ],

    CPPDEFINES = [
        ("ARDUINO", 10805),
        ("ARDUINO_VARIANT", '\\"%s\\"' % env.BoardConfig().get("build.variant").replace('"', "")),
        ("ARDUINO_BOARD", '\\"%s\\"' % env.BoardConfig().get("build.board_def").replace('"', ""))
    ],

    LINKFLAGS = [
        "-Wl,--start-group",
        "-lc",
        "-lgcc",
        "-lm",
        "-Wl,--end-group"
    ],

    CPPPATH = [
        join(FRAMEWORK_DIR, "cores", "arduino"),
        join(FRAMEWORK_DIR, "cores", "arduino", "hal"),
        join(FRAMEWORK_DIR, "cores", "arduino", "hal", "include"),
        join(SDK_DIR, "lib", "bsp"),
        join(SDK_DIR, "lib", "bsp", "include"),
        join(SDK_DIR, "lib", "drivers"),
        join(SDK_DIR, "lib", "drivers", "include"),
        join(SDK_DIR, "lib", "freertos"),
        join(SDK_DIR, "lib", "freertos", "include"),
        join(SDK_DIR, "lib", "freertos", "portable"),
        join(SDK_DIR, "lib", "freertos", "conf"),
        join(SDK_DIR, "lib", "utils", "include"),
    ],
    
    LIBPATH = [

    ],
    
    LIBS = [ 
        "c", "gcc", "m"
    ],

    LIBSOURCE_DIRS=[
        join(FRAMEWORK_DIR, "libraries")
    ],
    
)

env.Replace(
    LDSCRIPT_PATH = join(SDK_DIR,"lds","kendryte.ld")
)

#
# Target: Build Core Library
#

libs = []

if "build.variant" in env.BoardConfig():
    env.Append(
        CPPPATH=[
            join(FRAMEWORK_DIR, "variants",
                 env.BoardConfig().get("build.variant"))
        ]
    )
    libs.append(env.BuildLibrary(
        join("$BUILD_DIR", "FrameworkArduinoVariant"),
        join(FRAMEWORK_DIR, "variants", env.BoardConfig().get("build.variant"))
    ))

envsafe = env.Clone()

libs.append(envsafe.BuildLibrary(
    join("$BUILD_DIR", "FrameworkArduino"),
    join(FRAMEWORK_DIR, "cores", "arduino")
))



env.Prepend(LIBS=libs)

from SCons.Script import Import

Import("env")

board_config = env.BoardConfig()

env.Append(
    ASFLAGS = ["-x", "assembler-with-cpp"],

    CCFLAGS = [
        "-mcmodel=medany",
        "-mabi=lp64f",
        "-march=rv64imafc",
        "-fno-common",
        "-ffunction-sections",
        "-fdata-sections",
        "-fstrict-volatile-bitfields",
        "-fno-zero-initialized-in-bss",
        "-Os",
        "-ggdb",
        "-Wall",
        "-Werror=all",
        "-Wno-error=unused-function",
        "-Wno-error=unused-but-set-variable",
        "-Wno-error=unused-variable",
        "-Wno-error=deprecated-declarations",
        "-Wno-multichar",
        "-Wextra",
        "-Werror=frame-larger-than=65536",
        "-Wno-unused-parameter",
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
    ],

    CFLAGS = [
        "-std=gnu11",
        "-Wno-pointer-to-int-cast",
        "-Wno-old-style-declaration"
    ],

    CXXFLAGS = [
        "-std=gnu++17"
    ],

    CPPDEFINES = [
        "CONFIG_LOG_ENABLE",  #debug flags
        ("CONFIG_LOG_LEVEL", "LOG_INFO"),
        ("DEBUG", "1"),
        "__riscv64",
        "K210",
        ("ARCH", "K210"),
        ("F_CPU", "$BOARD_F_CPU")
    ],
    
    ASDEFINES = [
        "CONFIG_LOG_ENABLE",  #debug flags
        ("CONFIG_LOG_LEVEL", "LOG_INFO"),
        ("DEBUG", "1"),
        "__riscv64"
    ],

    LINKFLAGS = [
        "-nostartfiles",
        "-static",
        "-Wl,--gc-sections",
        "-Wl,-static",
        "-Wl,--start-group",
        "-Wl,--whole-archive",
        "-Wl,--no-whole-archive",
        "-Wl,--end-group",
        "-Wl,-EL",
        "-Wl,--no-relax"
        #"-T ${SDK_ROOT}/lds/kendryte.ld"
    ]
)

# copy CCFLAGS to ASFLAGS (-x assembler-with-cpp mode)
env.Append(ASFLAGS=env.get("CCFLAGS", [])[:])

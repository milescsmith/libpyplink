# lifted from https://github.com/sdispater/pendulum
import shutil
from distutils.command.build_ext import build_ext
from distutils.core import Distribution, Extension
from distutils.errors import CCompilerError, DistutilsExecError, DistutilsPlatformError
from pathlib import Path

import numpy as np
from Cython.Build import cythonize

# C Extensions

extensions = [
    Extension(
        "plink_ng.pgenlib",
        include_dirs=[np.get_include()],
        sources=[
            'src/plink_ng/pgenlib.pyx',
            'src/plink_ng/c/pgenlib_ffi_support.cc',
            'src/plink_ng/c/include/pgenlib_misc.cc',
            'src/plink_ng/c/include/pgenlib_read.cc',
            'src/plink_ng/c/include/pgenlib_write.cc',
            'src/plink_ng/c/include/plink2_base.cc',
            'src/plink_ng/c/include/plink2_bits.cc'
            ],
        language = "c++",
        # do not compile as c++11, since cython doesn't yet support
        # overload of uint32_t operator
        # extra_compile_args = ["-std=c++11", "-Wno-unused-function"],
        # extra_link_args = ["-std=c++11"],
        extra_compile_args = ["-std=c++98", "-Wno-unused-function", "-Wno-macro-redefined"],
        extra_link_args = ["-std=c++98"],
    ),
]


class BuildFailed(Exception):
    pass


class ExtBuilder(build_ext):
    # This class allows C extension building to fail.

    built_extensions = []

    def run(self):
        try:
            build_ext.run(self)
        except (DistutilsPlatformError, FileNotFoundError):
            print(
                "  Unable to build the C extensions"
            )

    def build_extension(self, ext):
        try:
            build_ext.build_extension(self, ext)
        except (CCompilerError, DistutilsExecError, DistutilsPlatformError, ValueError):
            print(
                f"  Unable to build the '{ext.name}' C extension"
            )


def build(setup_kwargs):
    """
    This function is mandatory in order to build the extensions.
    """
    distribution = Distribution(
        {
            "name": "Pgenlib",
            "ext_modules": cythonize(
                extensions, compiler_directives={"language_level": "3"}
            ),
        }
    )
    distribution.package_dir = "plink_ng"

    cmd = ExtBuilder(distribution)
    cmd.ensure_finalized()
    cmd.run()

    # Copy built extensions back to the project
    for output in cmd.get_outputs():
        output = Path(output)
        relative_extension = Path("src").joinpath(output.relative_to(cmd.build_lib))
        if not output.exists():
            continue

        shutil.copyfile(output, relative_extension)
        mode = relative_extension.stat().st_mode
        mode |= (mode & 0o444) >> 2
        relative_extension.chmod(mode)

    return setup_kwargs


if __name__ == "__main__":
    build({})

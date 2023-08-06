import sys
sys.exit("""\
You have downloaded a manylinux1 wheel (.whl), probably due to using
an outdated version of pip.

manylinux1 is not supported by this project.

You can attempt to download and build a source distribution, but this may
fail to compile, or compile without important features.

We recommend that you upgrade to the latest version of pip and try again.
""")

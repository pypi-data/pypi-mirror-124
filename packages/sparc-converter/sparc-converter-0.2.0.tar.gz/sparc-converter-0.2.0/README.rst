
SPARC Converter
===============

Python applications to convert data from one format to another.

Usage
-----

Basic usage instructions::

 usage: sparc-convert [-h] [-o OUTPUT_DIR] {web-gl} ...

 Convert SPARC data.

 positional arguments:
   {web-gl}              Choose a command
     web-gl              export to WebGL

 optional arguments:
   -h, --help            show this help message and exit
   -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                         specify the output directory


Usage instructions for *web-gl* command::

  usage: sparc-convert web-gl [-h] [-p PREFIX] argon_doc

  positional arguments:
    argon_doc             an Argon document

  optional arguments:
    -h, --help            show this help message and exit
    -p PREFIX, --prefix PREFIX
                          set web-gl output prefix

Example
-------

::

  sparc-convert web-gl <path-to-argon-file>/CubeSquareLine.neon -o webgl

# vdscript_to_cpf
This script converts VirtualDub or VirtualDub2 .vdscript files into Cuttermaran .cpf project files.
This script was tested and works with:
- Python 3.12.5     
- VirtualDub2 (build 44282) .vdscript files
- Cuttermaran 1.70

Features:
- Convert VirtualDub(.vdscript) cuts into Cuttermaran(.cpf) format.
- Automatically adds segment identifiers as comments for each cut.

Usage:
1. Specify the paths for the .vdscript file, .cpf file, video file, and audio file.
2. Run the script.

Note: Works best with .vdscript files processed by "vdscript_range_adjuster", which is another one of my python scripts. It can be found on GitHub. If your cut-in/cut-out points have already been aligned with keyframes, "vdscript_range_adjuster" is not necessary.

Version History:
v1.0.0 - Initial script with basic conversion functionality.
v1.1.0 - Added segment identifying feature for all output .cpf files.
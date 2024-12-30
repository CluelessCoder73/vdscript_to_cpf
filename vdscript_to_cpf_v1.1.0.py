import re
import os

# ----------------------------------------------------------------------
# Script: vdscript_to_cpf_v1.1.0.py
# Description:
# This script converts VirtualDub or VirtualDub2 .vdscript files into 
# Cuttermaran .cpf project files. It is designed to help users quickly 
# create Cuttermaran project files from existing VirtualDub cuts.
# 
# This script was tested and works with:
# - Python 3.12.5     
# - VirtualDub2 (build 44282) .vdscript files
# - Cuttermaran 1.70
#
# Features:
# - Convert VirtualDub(.vdscript) cuts into Cuttermaran(.cpf) format.
# - Automatically adds segment identifiers as comments for each cut.
#
# Usage:
# 1. Specify the paths for the .vdscript file, .cpf file, video file, and audio file.
# 2. Run the script.
#
# Note: Works best with .vdscript files processed by "vdscript_range_adjuster", 
# which is another one of my python scripts. It can be found on GitHub. 
# If your cut-in/cut-out points have already been aligned with keyframes, 
# "vdscript_range_adjuster" is not necessary.
#
# Version History:
# v1.0.0 - Initial script with basic conversion functionality.
# v1.1.0 - Added segment identifying feature for all output .cpf files.
# ----------------------------------------------------------------------

def parse_vdscript(filepath):
    """
    Parses the .vdscript file to extract cut ranges as start and end frame numbers.

    Args:
        filepath (str): Path to the .vdscript file.

    Returns:
        list: A list of dictionaries representing cut segments with start and adjusted end frames.
    """
    cut_segments = []

    with open(filepath, 'r') as file:
        lines = file.readlines()
    
    # Regex to match VirtualDub subset lines (e.g., VirtualDub.subset.AddRange(412,208);)
    subset_pattern = re.compile(r'VirtualDub\.subset\.AddRange\((\d+),(\d+)\);')

    for line in lines:
        match = subset_pattern.match(line)
        if match:
            start_frame = int(match.group(1))
            frame_count = int(match.group(2))
            end_frame = start_frame + frame_count - 1  # Adjusting for inclusive behavior in Cuttermaran
            
            # Append the segment to the list
            cut_segments.append({
                "start": start_frame,
                "end": end_frame
            })

    return cut_segments

def write_cpf_file(output_filepath, video_filepath, audio_filepath, cut_segments):
    """
    Writes the cut segments to a Cuttermaran .cpf file.

    Args:
        output_filepath (str): Path to save the .cpf file.
        video_filepath (str): Path to the video file.
        audio_filepath (str): Path to the audio file.
        cut_segments (list): List of dictionaries representing cut segments.
    """
    if os.path.exists(output_filepath):
        print(f"Error: The file {output_filepath} already exists. Please choose a different filename or remove the existing file.")
        return
    
    with open(output_filepath, 'w') as file:
        # Write the XML header
        file.write('<?xml version="1.0" standalone="yes"?>\n')
        file.write('<StateData xmlns="http://cuttermaran.kickme.to/StateData.xsd">\n')
        
        # Write the used video and audio files
        file.write(f'  <usedVideoFiles FileID="0" FileName="{video_filepath}" />\n')
        file.write(f'  <usedAudioFiles FileID="1" FileName="{audio_filepath}" StartDelay="0" />\n')
        
        # Write each cut segment with comments
        for i, segment in enumerate(cut_segments):
            file.write(f'  <!-- Segment {i + 1} -->\n')
            file.write(f'  <CutElements refVideoFile="0" StartPosition="{segment["start"]}" EndPosition="{segment["end"]}">\n')
            file.write(f'    <cutAudioFiles refAudioFile="1" />\n')
            file.write('  </CutElements>\n')
        
        # Write the current files section
        file.write('  <CurrentFiles refVideoFiles="0">\n')
        file.write('    <currentAudioFiles refAudioFiles="1" />\n')
        file.write('  </CurrentFiles>\n')
        
        # Close the XML
        file.write('</StateData>\n')
    
    print(f"Cuttermaran project file saved as {output_filepath}")

# Main function to perform the conversion
def convert_vdscript_to_cpf(vdscript_filepath, cpf_filepath, video_filepath, audio_filepath):
    """
    Main function to convert a .vdscript file to a .cpf file for Cuttermaran.

    Args:
        vdscript_filepath (str): Path to the .vdscript file.
        cpf_filepath (str): Path to save the .cpf file.
        video_filepath (str): Path to the video file.
        audio_filepath (str): Path to the audio file.
    """
    cut_segments = parse_vdscript(vdscript_filepath)
    write_cpf_file(cpf_filepath, video_filepath, audio_filepath, cut_segments)

# Usage example - EDIT THESE VALUES
if __name__ == "__main__":
    vdscript_filepath = r"C:\New folder\test.vdscript"  # Path to the .vdscript file
    cpf_filepath = r"C:\New folder\output.cpf"  # Path to save the .cpf file
    video_filepath = r"C:\New folder\test.m2v"  # Path to the video file
    audio_filepath = r"C:\New folder\test.mp2"  # Path to the audio file
    
    convert_vdscript_to_cpf(vdscript_filepath, cpf_filepath, video_filepath, audio_filepath)


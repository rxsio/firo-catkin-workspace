import os
import json
import sys


def merge_compile_commands(build_directory):
    compile_commands = []

    # Collect all compile_commands.json files in the build directory
    for package in os.listdir(build_directory):
        file_path = os.path.join(build_directory, package,
                                 'compile_commands.json')
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                compile_commands.extend(json.load(file))

    # Dump the merged compile_commands.json file
    compile_commands.sort(key=lambda x: x['file'])
    compile_commands_path = os.path.join(build_directory,
                                         'compile_commands.json')
    with open(compile_commands_path, 'w') as file:
        json.dump(compile_commands, file, indent=4)


if __name__ == '__main__':
    # Optional argument: path to the build directory
    if len(sys.argv) > 1:
        build_directory = sys.argv[1]
    else:
        build_directory = 'build'
    merge_compile_commands(build_directory)

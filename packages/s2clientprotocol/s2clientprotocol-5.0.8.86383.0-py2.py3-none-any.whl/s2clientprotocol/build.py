##
## This file is auto-generated by ../s2client-api-build/buildpylib/update_version_file.py
##
import subprocess

def game_version():
    return "5.0.8.86383.0"


def read_command_output(cmd):
    lines = []
    handle = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    while True:
        line = handle.stdout.readline()
        if line != '':
            lines.append(line.rstrip())
        else:
            break
    return lines


def git_commit_hash():
    git_version_cmd = ['git', 'rev-parse', 'HEAD']
    lines = read_command_output(git_version_cmd)
    if len(lines) == 0 or len(lines) > 1:
        raise Exception("invalid output '{}' from '{}'".format(
            '\\n'.join(lines),
            ' '.join(git_version_cmd)))

    git_commit_hash = (''.join(lines))[0:8]

    return git_commit_hash


if __name__ == '__main__':
    print("Game version: {}".format(game_version()))
    print("Git commit hash: {}".format(git_commit_hash()))
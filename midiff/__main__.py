import tools
import argparse


def main():
    midiff = tools.MidiffTools()

    parser = argparse.ArgumentParser(description="View the difference between MIDI files in a human readable format.")
    parser.add_argument("repo", help="Path to the git repository", nargs='?', default=".")
    parser.add_argument("--diff", nargs=2, help="Provide the path to 2 midi files and compare them.")
    parser.add_argument("--configure-difftool", nargs=1,
                        help="Give the diff tool command to use to compare files with `$1` and `$2` as placeholders "
                             "for the two files you want to compare. Current diff tool is: `" + midiff.diff_tool_cmd +
                             "`.")
    parser.add_argument("--configure-clear", nargs=1, type=str,
                        help="Set to false if you want to remove the temporary files when midiff is done. Clearing "
                             "the files may cause problems on asynchronous diff tools such as VS Code. Currently "
                             "set to " + str(midiff.settings["clear"]).lower() + ".")
    args = parser.parse_args()

    # Configuration
    if args.configure_difftool is not None:
        diff_cmd = args.configure_difftool[0]
        if '$1' not in diff_cmd:
            print("Error: could not find '$1' placeholder in the difftool command `" + diff_cmd + "`.")
            exit(-1)
        if '$2' not in diff_cmd:
            print("Error: could not find '$2' placeholder in the difftool command `" + diff_cmd + "`.")
            exit(-1)
        midiff.settings["diff-tool"] = diff_cmd
        print("Now using diff tool command: `" + diff_cmd + "`")

    elif args.configure_clear is not None:
        if args.configure_clear[0].lower() not in ["true", "false"]:
            print("Error, expected `true` or `false`, not " + args.configure_clear[0] + ".")
            exit(-1)
        midiff.settings["clear"] = args.configure_clear[0].lower() == "true"
        print("Clear the files is not set to " + str(midiff.settings["clear"]).lower() + ".")

    # Compare two files
    elif args.diff is not None:
        midiff.compare_midi_files(args.diff[0], args.diff[1])

    # Use Git
    else:
        midiff = tools.MidiffTools(args.repo)
        midiff.git_diff()


if __name__ == "__main__":
    main()

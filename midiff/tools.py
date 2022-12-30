import py_midicsv as pm
import os
import tempfile
import json
import subprocess
import git


class MidiffTools:
    s_settings_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "settings.json")

    def __init__(self, git_repo_path_i=None):
        self.settings = {}
        self.created_files = []
        self.diff_tool_cmd = "diff $1 $2"
        self.read_settings()
        self.git_tools = None
        self.git_files = []
        self.setup_git(git_repo_path_i)

    def __del__(self):
        self.write_settings()
        # Delete the tmp files
        if self.settings['clear']:
            for file in self.created_files:
                os.remove(file)

    def setup_git(self, git_repo_path_i):
        if git_repo_path_i is None:
            return
        self.git_tools = GitTools(git_repo_path_i)
        for path, head in self.git_tools.heads.items():
            tmp = self.create_non_existing_tmp_file("HEAD_" + os.path.basename(path), ".mid")
            with open(tmp, "wb") as f:
                f.write(head)
            self.git_files.append([path, tmp])

    def read_settings(self) -> None:
        """
        Get the settings dict
        :return: settings as a dict
        """
        with open(self.s_settings_path, "r") as f:
            self.settings = json.loads(f.read())
        self.diff_tool_cmd = self.settings["diff-tool"]

    def write_settings(self) -> None:
        """
        Write the settings json file
        :return: None
        """
        with open(self.s_settings_path, "w") as f:
            f.write(json.dumps(self.settings, indent=4))

    def create_non_existing_tmp_file(self, file_name_i: str, extension_i: str) -> str:
        """
        Create an empty file in the temp directory from the given file name and
        return the path to this file name.
        :param file_name_i: file name
        :param extension_i: Extension of the file
        :return: path to the temporary file
        """
        output_tmp_file_path = os.path.join(tempfile.gettempdir(), file_name_i)
        if os.path.exists(output_tmp_file_path + extension_i):
            i = 0
            while os.path.isfile(output_tmp_file_path + "_" + str(i) + extension_i):
                i += 1
            output_tmp_file_path + "_" + str(i) + extension_i
        else:
            output_tmp_file_path += extension_i
        with open(output_tmp_file_path, "w") as _:
            self.created_files.append(output_tmp_file_path)
        return output_tmp_file_path

    def create_temp_csv_midi_file(self, midi_file_path_i: str) -> str:
        """
        Create a temporary csv file containing the MIDI data in
        midi_file_path_i. Return the file name, so you can work with it.
        :param midi_file_path_i: path to the midi file to parse :return:
        path to the temporary csv file
        """
        file_name_c = os.path.basename(midi_file_path_i)
        output_tmp_file_path_c = self.create_non_existing_tmp_file(file_name_c, ".csv")

        csv_string = pm.midi_to_csv(midi_file_path_i)
        with open(output_tmp_file_path_c, "w") as f:
            f.writelines(csv_string)
        return output_tmp_file_path_c

    def open_diff_tool(self, file_1_i: str, file_2_i: str) -> None:
        """
        Open the difftool from the settings with the two provided files
        :param file_1_i: First file to compare
        :param file_2_i: Second file to compare
        :return: None
        """
        command_c = self.diff_tool_cmd.replace("$1", '"' + file_1_i + '"').replace("$2", '"' + file_2_i + '"')
        subprocess.run(command_c, shell=True)

    def compare_midi_files(self, file_1_i: str, file_2_i: str) -> None:
        """
        Creates two temporary csv files from the provided midi files and
        compare the results using the difftool.
        :param file_1_i: First midi file to compare
        :param file_2_i: Second midi file to compare
        :return: None
        """
        csv_1 = self.create_temp_csv_midi_file(file_1_i)
        csv_2 = self.create_temp_csv_midi_file(file_2_i)
        self.open_diff_tool(csv_1, csv_2)

    def git_diff(self):
        if not self.git_files:
            print("No midi files have been modified since last revision.")
        for files in self.git_files:
            self.compare_midi_files(files[0], files[1])


class GitTools:
    def __init__(self, repo_path_i):
        self.repo_path = repo_path_i
        try:
            self.repo = git.Repo(repo_path_i)
        except git.exc.InvalidGitRepositoryError:
            print("Could not find a git repository in '" + repo_path_i + "'. Please run midiff in a git repository.")
            exit(-1)
        self.modified_midi_files_relative = []
        self.heads = {}
        self.get_modified_midi_files_list_and_heads()

    def get_modified_midi_files_list_and_heads(self) -> None:
        """
        Save the list of all the changed midi files
        """
        for item in self.repo.index.diff(None):
            if item.a_path.lower().endswith("mid") or item.a_path.lower().endswith("midi"):
                self.modified_midi_files_relative = item.a_path
                self.heads[os.path.join(self.repo_path, item.a_path)] = self.get_head_version_of_file(item.a_path)

    def get_head_version_of_file(self, file_path_i: str) -> bytes:
        """
        Return the content of the file in the HEAD revision
        :param file_path_i: file to view. Must be relative to the git repo
        :return: head version
        """
        olddir = os.path.abspath(".")
        os.chdir(self.repo_path)
        output = subprocess.check_output(["git", "show", "HEAD:" + file_path_i])
        os.chdir(olddir)
        return output

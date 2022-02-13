import os
import shutil
from util_module import bash


class Organic:
    _FOLDER_BASE_NAME = "smells"
    _FILE_BASE_NAME = "smells"
    """Organic run:

    Attributes
        repo_name -- name of the repository
        smell_detector -- path to the Organic jar, output_file}
        output_folder -- path to the result folder
        source_path -- path to the project's source code analyzed
    """
    def __init__(self, repo_name, smell_detector, output_folder, source_path, commit):
        self.repo_name = repo_name
        self.detector = smell_detector
        self.output_folder = os.path.join(output_folder, repo_name, Organic._FOLDER_BASE_NAME)
        self.output_file = os.path.join(self.output_folder, '{}_{}'.format(Organic._FILE_BASE_NAME, commit))
        self.source = source_path

        self.command = f"java -jar {self.detector} -sf {self.output_file} -src {self.source}"

    def detect_smells(self):
        # check if folder exists, deleting if so
        # if os.path.exists(self.output_folder):
        #     shutil.rmtree(self.output_folder)

        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)  # It creates all the intermediate folders

        print("::: Detecting code smells :::")
        bash.run_command(self.command, False)
        print("::: Done :::")

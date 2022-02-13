import os
import git  # let's import only git so we don't confuse the submodules from Pydriller
import shutil


class RepositoryClone:
    _FOLDER_BASE_NAME = "source"

    @staticmethod
    def clone(repo_name, repo_url, repo_branch, output_folder) -> str:
        repo_local_path = os.path.join(output_folder, repo_name, RepositoryClone._FOLDER_BASE_NAME)

        # check if folder exists, deleting if so
        if os.path.exists(repo_local_path):
            shutil.rmtree(repo_local_path)

        os.makedirs(repo_local_path)  # It creates all the intermediate folders

        git.Repo.clone_from(repo_url, repo_local_path, branch=repo_branch)

        return repo_local_path

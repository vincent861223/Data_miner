from genericpath import exists
from pydriller import Repository
from util_module import RepositoryClone
from pydriller import Git
from smell_detector import Organic
import threading
import os
import json
from scipy.stats import fisher_exact


class Project:

    def __init__(self, name, url, branch, starting_commit, ending_commit, output_folder, smell_detector):
        self.repository = Repository(url, from_commit=starting_commit, to_commit=ending_commit)

        self.name = name
        self.branch = branch
        self.url = url
        self.starting_commit = starting_commit
        self.ending_commit = ending_commit
        self.output_folder = output_folder
        self.smell_detector = smell_detector

        self.git = None

        self.author_modified_files = {}  # {author_name: nº modified files}
        self.commit_most_modified_lines = {'hash': None, 'lines': 0}  # int insertion + deletion lines
        self.repo_local_path = RepositoryClone.clone(self.name, self.url, self.branch, output_folder)
        print(self.repo_local_path)
        self.git = Git(self.repo_local_path)

    def __str__(self):
        return f'Project name: {self.name}; commits -> start: {self.starting_commit}; end {self.ending_commit}'

    def collect_statistic(self):
        """
        Generator is similar to a function tha returns an array but instead of building an array containing all the
        values and returning them all at once, a generator yields the values one at a time, which requires less memory
        and allows the caller to get started processing the first few values immediately.
        """
        generator = self.repository.traverse_commits()

        for commit in generator:
            self.process_commit(commit)

    def process_commit(self, commit):
        author_name = commit.author.name
        modified_files = commit.files

        if author_name in self.author_modified_files:
            self.author_modified_files[author_name] += modified_files
        else:
            self.author_modified_files[author_name] = modified_files

        modified_lines = commit.lines
        if self.commit_most_modified_lines['lines'] < modified_lines:
            self.commit_most_modified_lines = {'hash': commit.hash, 'lines': modified_lines}

    def get_statistic(self):
        author_name = max(self.author_modified_files, key=self.author_modified_files.get)

        _hash, _line = self.commit_most_modified_lines.values()

        return f'Project name: {self.name}:\n' \
               f'\tThe author with most modifications is {author_name} with ' \
               f'{self.author_modified_files[author_name]} modified files.\n' \
               f'\tThe commit with most modified lines is {_hash} with {_line} modified lines'

    def detect_smells(self, commit):
        smells_file = os.path.join(self.output_folder, self.name, "smells", "smells_{}".format(commit))
        if os.path.exists(smells_file):
            return 
 
        self.git.checkout(commit)      # We can open the terminal and see the checkout result

        organic = Organic(self.name, self.smell_detector, self.output_folder, self.repo_local_path, commit)
        organic.detect_smells()

    def detect_smells_all(self):
        for commit in self.repository.traverse_commits():
            self.detect_smells(commit.hash)
    
    def get_smells_counts(self, commit):
        smells_file = os.path.join(self.output_folder, self.name, "smells", "smells_{}".format(commit))
        
        stat = {}
        try:
            with open(smells_file, 'r') as f:
                files = json.load(f)
        except:
            return None
        
        smells = [smell for methods in files for smell in methods['methods']]

        for smell in smells:
            class_file = smell['sourceFile']['fileRelativePath'] 
            class_file = os.path.relpath(class_file, os.path.join(self.output_folder, self.name, 'source'))
            if 'test' in class_file: continue
            n_smells = len(smell['smells'])
            if not class_file in stat:
                stat[class_file] = {'n_smells': 0, 'changed': False}
            stat[class_file]['n_smells'] += n_smells 
        return stat
    
    def analyze(self):
        #self.get_smells_counts(self.starting_commit)
        stats = {}

        for commit in self.repository.traverse_commits():
            stat = self.get_smells_counts(commit.hash)
            if not stat: continue
            for modified_file in commit.modified_files:
                modified_file = modified_file.new_path
                if modified_file and 'test' in modified_file: continue
                if modified_file in stat:
                    stat[modified_file]['changed'] = True
                # else:
                    # print(modified_file)
            stats[commit.hash] = stat
        
        output_file = os.path.join(self.output_folder, self.name, 'smells_changes')
        with open(output_file, 'w') as f:
            json.dump(stats, f, sort_keys=True, indent=4)

    def summary(self):
        stat_file = os.path.join(self.output_folder, self.name, 'smells_changes')
        with open(stat_file, 'r') as f:
            stats = json.load(f) 

        cum_stats = {} 
        n_commit = 0
        for commit, stat in stats.items():
            n_commit += 1
            for file, res in stat.items():
                if file not in cum_stats: 
                    cum_stats[file] = {'smells': False, 'changed': False}
                if res['n_smells'] > 0:
                    cum_stats[file]['smells'] = True 
                if res['changed']: 
                    cum_stats[file]['changed'] = True 

        count = {'smell_change': 0, 'smell_nchange': 0, 'nsmell_change': 0, 'nsmell_nchange': 0}
        for file, res in cum_stats.items():
            smell_s = 'smell'
            change_s = 'change'
            if not res['smells']:
                smell_s = 'nsmell'
            if not res['changed']:
                change_s = 'nchange'
            count[smell_s + '_' + change_s] += 1

        table = [[count['smell_change'], count['smell_nchange']], [count['nsmell_change'], count['nsmell_nchange']]]
        oddsr, p = fisher_exact(table, alternative='two-sided')
        print('Total commits: ', n_commit)
        print(count, 'p: {}'.format(p))


        # counts = {}
        # for commit, stat in stats.items():
        #     count = {'smell_change': 0, 'smell_nchange': 0, 'nsmell_change': 0, 'nsmell_nchange': 0}
        #     for file, res in stat.items():
        #         smell_s = 'smell'
        #         change_s = 'change'
        #         if res['n_smells'] == 0:
        #             smell_s = 'nsmell'
        #         if not res['changed']:
        #             change_s = 'nchange'
        #         count[smell_s + '_' + change_s] += 1
        #     table = [[count['smell_change'], count['smell_nchange']], [count['nsmell_change'], count['nsmell_nchange']]]
        #     oddsr, p = fisher_exact(table, alternative='two-sided')
        #     print(commit, count, 'p: {}'.format(p))

        #     counts[commit] = count

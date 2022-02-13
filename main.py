from util_module import RepositoryLoader
from settings import Settings
from git_miner import Project


class Main:

    def __init__(self):
        self.repositories = []
        self.settings = Settings()
        self.projects = self._load_projects()


    def _load_projects(self):
        projects = []
        repository_loader = RepositoryLoader(self.settings.get_repository_file_path())
        loaded_projects = repository_loader.load()
        smell_detector = self.settings.get_smell_detector_path()

        for p in loaded_projects:
            project = Project(
                p['repo_name'],
                p['git_url'],
                p['branch'],
                p['starting_commit'],
                p['ending_commit'],
                self.settings.get_output_folder_path(),
                smell_detector
            )

            projects.append(project)

        return projects

    def start(self):
        
        for p in self.projects:
            p.collect_statistic()
            print(str(p.get_statistic()))

    # Smell collector test
    def collect_smells(self):
        for p in self.projects:
            p.detect_smells_all()
    
    def analyze(self):
       for p in self.projects:
           p.analyze() 
           p.summary()


main = Main()
main.collect_smells()
main.analyze()


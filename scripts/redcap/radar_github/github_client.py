from github import Github
import json

class GitHubClient:
    def __init__(self, github_token):
        self.client = Github(github_token)
        self.user = self.client.get_user()

    def create_repo(self, repo_name):
        new_repo = self.user.create_repo(repo_name)
        return new_repo

    def get_repo(self, repo_name):
        repo = self.client.get_repo(repo_name)
        return repo
    
    def create_branch(self, repo, branch):
        master_ref = repo.get_git_ref("heads/master")
        repo.create_git_ref(f"refs/heads/{branch}", master_ref.object.sha)

    def write_json_file(self, repo, branch, file_path: str, data: dict, commit_message: str):
        content = json.dumps(data)
        repo.create_file(file_path, commit_message, content, branch=branch)

    def commit_json_file(self, repo, file_path, data, branch, commit_message):
        content = json.dumps(data)
        file = repo.get_contents(file_path)
        repo.update_file(file.path, commit_message, content, file.sha, branch=branch)

    def get_json_file(self, repo, file_path, branch):
        file = repo.get_contents(file_path, ref=branch)
        content = file.decoded_content.decode()
        data = json.loads(content)
        return data
    
    def update_or_create_file(self, repo, file_path, data, branch, commit_message):
        content = data
        try:
            file = repo.get_contents(file_path, ref=branch)
            if file.decoded_content.decode() != content:
                repo.update_file(file.path, commit_message, content, file.sha, branch=branch)
                print(f"File {file_path} has been updated.")
            else:
                print(f"File {file_path} has not changed.")
        except Exception as e:
            repo.create_file(file_path, commit_message, content, branch=branch)
            print(f"File {file_path} has been created.")


    def get_tree(self, repo, branch):
        tree = repo.get_git_tree(sha=branch, recursive=True)
        return tree
    
    def get_all_json_files(self, repo, branch):
        tree = self.get_tree(repo, branch)
        json_files = [f for f in tree.tree if f.path.endswith(".json")]
        return json_files
    
    def get_project_files(self, repo, branch, project):
        tree = self.get_tree(repo, branch)
        project_files = [f for f in tree.tree if project in f.path]
        return project_files
    


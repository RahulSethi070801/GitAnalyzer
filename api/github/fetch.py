import os
import json
import base64
from github import Github, Auth, UnknownObjectException
from dotenv import load_dotenv

load_dotenv()

class GitHubRepoFetcher:
    def __init__(self):
        self.pat = os.getenv("GITHUB_PAT")
        self.auth = Auth.Token(self.pat)
        self.g = Github(auth=self.auth)
        self.output = {
            "repo_name": "",
            "files": [],
            "submodules": []
        }
        # Patterns to exclude from results
        self.excluded_patterns = {
            '.DS_Store', '___MACOSX', '.o', '.swp', '.swiftpm',
            'bwspblob', 'dsclbool', 'lg1Scomp', 'moDDblob', 
            'ph1Scomp', 'vSrnlong', 'Ilocblob', 'modDblob'
        }

    def _get_default_branch(self, repo):
        try:
            return repo.default_branch
        except:
            return "main"

    def _should_exclude(self, path):
        """Check if file path matches exclusion patterns"""
        return any(pattern in path for pattern in self.excluded_patterns)

    def _clean_content(self, content, path):
        """Clean and format file contents"""
        # Skip binary files
        if b'\x00' in content[:1024]:
            print(f"🚫 Skipped binary file: {path}")
            return None
            
        # Format C++ files
        if path.endswith(('.cpp', '.h', '.hpp')):
            try:
                return '\n'.join([line.rstrip() for line in content.decode('utf-8').split('\n')])
            except UnicodeDecodeError:
                return None
                
        return content.decode('utf-8', errors='replace')

    def _get_file_content(self, repo, path, ref):
        try:
            content = repo.get_contents(path, ref=ref)
            if content.encoding == "base64":
                decoded = base64.b64decode(content.content)
                return self._clean_content(decoded, path)
            return None
        except Exception as e:
            print(f"⚠️ Skipped {path}: {str(e)}")
            return None

    def _process_repo(self, repo_name, path="", prefix=""):
        try:
            repo = self.g.get_repo(repo_name)
            default_branch = self._get_default_branch(repo)
            files = []
            submodules = []
            
            try:
                contents = repo.get_contents(path, ref=default_branch)
            except UnknownObjectException:
                return {"files": [], "submodules": []}

            for item in contents:
                if self._should_exclude(item.path):
                    print(f"⏩ Skipped excluded pattern: {item.path}")
                    continue

                full_path = os.path.join(prefix, item.path)
                if item.type == "file":
                    content = self._get_file_content(repo, item.path, default_branch)
                    if content:
                        files.append({
                            "file_path": full_path,
                            "content": content
                        })
                elif item.type == "dir":
                    subdir_data = self._process_repo(
                        repo_name,
                        path=item.path,
                        prefix=os.path.join(prefix, item.path)
                    )
                    files.extend(subdir_data["files"])
                    submodules.extend(subdir_data["submodules"])
                elif item.type == "submodule":
                    submodule_data = self._process_submodule(item, prefix)
                    if submodule_data:
                        submodules.append(submodule_data)
            
            return {
                "files": files,
                "submodules": submodules
            }
        except Exception as e:
            print(f"💥 Error in {repo_name}: {str(e)}")
            return {"files": [], "submodules": []}

    def _process_submodule(self, submodule_item, prefix):
        try:
            sub_url = submodule_item.html_url
            repo_path = sub_url.replace("https://github.com/", "")
            sub_repo = self.g.get_repo(repo_path)
            commit_sha = submodule_item.sha or sub_repo.get_branch(
                self._get_default_branch(sub_repo)
            ).commit.sha

            sub_data = self._process_repo(
                repo_path,
                prefix=os.path.join(prefix, submodule_item.path)
            )
            
            return {
                "name": submodule_item.path,
                "url": sub_url,
                "commit": commit_sha,
                "files": sub_data["files"],
                "submodules": sub_data["submodules"]
            }
        except Exception as e:
            print(f"❌ Submodule failed: {str(e)}")
            return None

    def fetch_repo_structure(self, repo_name):
        try:
            result = self._process_repo(repo_name)
            self.output.update({
                "repo_name": repo_name,
                **result
            })
            return self.output
        except Exception as e:
            print(f"💥 Critical error: {str(e)}")
            return None

    def save_as_json(self, data, filename="repo_contents.json"):
        """Save with cleaned structure and sorted entries"""
        cleaned_data = {
            "repo_name": data["repo_name"],
            "files": sorted(data["files"], key=lambda x: x["file_path"]),
            "submodules": sorted(data["submodules"], key=lambda x: x["name"])
        }
        
        with open(filename, "w") as f:
            json.dump(cleaned_data, f, indent=2, ensure_ascii=False)
        print(f"✅ Cleaned structure saved to {filename}")

if __name__ == "__main__":
    fetcher = GitHubRepoFetcher()
    repo_data = fetcher.fetch_repo_structure("RahulSethi070801/Hybrid-Distributed-File-System")
    if repo_data:
        fetcher.save_as_json(repo_data)
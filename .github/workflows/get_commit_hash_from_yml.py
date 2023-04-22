# execute this script and all functions within from the git root folder
import os

def get_ref_from_env():
    with open(".env", "r") as f:
        for line in f:
            if line.startswith("LLVM_COMMIT="):
                ref = line.split("LLVM_COMMIT=")[1].strip()
                return ref

def ensure_executed_in_git_root():
    # make sure it is executed from the root folder
    assert os.path.exists(".git")
    assert os.path.exists(".github")
    assert os.path.exists(".github/workflows")
    assert os.path.exists(".github/workflows/manual_build_this_repo_and_llvm.py")
    assert os.path.exists(".github/workflows/get_commit_hash_from_yml.py")
    assert os.path.exists(".github/workflows/replace_commit_hash_in_yml.py")
    assert os.path.exists(".github/workflows/build-and-test.yml")
    assert os.path.exists(".github/workflows/pull.yml")

if __name__ == "__main__":
    ensure_executed_in_git_root()
    print(get_ref_from_env())
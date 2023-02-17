# execute this script and all functions within from the git root folder
from get_commit_hash_from_yml import ensure_executed_in_git_root
import sys

if __name__=="__main__":
    ensure_executed_in_git_root()
    # for filename in [".github/workflows/build-and-test.yml", ".github/workflows/pull.yml"]:
    #     with open(filename, "r") as f:
    #         lines = f.readlines()
    #     with open(filename, "w") as f:
    #         for line in lines:
    #             if line.startswith("  LLVM_COMMIT:"):
    #                 f.write("  LLVM_COMMIT: " + sys.argv[1] + "\n")
    #             else:
    #                 f.write(line)

    with open(".env", "r") as f:
        lines = f.readlines()
    with open(".env", "w") as f:
        for line in lines:
            if line.startswith("LLVM_COMMIT="):
                f.write("LLVM_COMMIT=" + sys.argv[1] + "\n")
            else:
                f.write(line)
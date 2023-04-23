# execute this script and all functions within from the git root folder
from get_commit_hash_from_yml import ensure_executed_in_git_root
import sys

if __name__=="__main__":
    # usage: python3 .github/workflows/replace_commit_hash_in_yml.py <input_ref> <commit_hash_to_be_pulled>
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
        met_llvm_commit = False
        met_llvm_ref = False
        for line in lines:
            if line.startswith("LLVM_COMMIT="):
                # TODO: always write down commit hash in LLVM_COMMIT and write down sys.argv[1] additionally in LLVM_REF so that when sys.argv[1] is a branch name (tag name is fine now), we can still see the commit hash
                f.write("LLVM_COMMIT=" + sys.argv[2] + "\n")
                met_llvm_commit = True
            elif line.startswith("LLVM_REF="):
                f.write("LLVM_REF=" + sys.argv[1] + "\n")
                met_llvm_ref = True
            else:
                f.write(line)
        if not met_llvm_commit:
            f.write("LLVM_COMMIT=" + sys.argv[2] + "\n")
        if not met_llvm_ref:
            f.write("LLVM_REF=" + sys.argv[1] + "\n")
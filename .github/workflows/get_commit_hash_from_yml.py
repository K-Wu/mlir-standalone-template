
if __name__ == "__main__":
    with open(".github/workflows/build-and-test.yml", "r") as f:
        for line in f:
            if line.startswith("  LLVM_COMMIT:"):
                commit_hash = line.split("LLVM_COMMIT:")[1].strip()
                print(commit_hash)
                break
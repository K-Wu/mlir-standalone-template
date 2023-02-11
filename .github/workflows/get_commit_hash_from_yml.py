
if __name__ == "__main__":
    with open(".env", "r") as f:
        for line in f:
            if line.startswith("LLVM_COMMIT="):
                commit_hash = line.split("LLVM_COMMIT=")[1].strip()
                print(commit_hash)
                break
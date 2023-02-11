import sys

if __name__=="__main__":
    with open(".github/workflows/build-and-test.yml", "r") as f:
        lines = f.readlines()
    with open(".github/workflows/build-and-test.yml", "w") as f:
        for line in lines:
            if line.startswith("  LLVM_COMMIT:"):
                f.write("  LLVM_COMMIT: " + sys.argv[1] + "\n")
            else:
                f.write(line)
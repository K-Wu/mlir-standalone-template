import sys

if __name__=="__main__":
    for filename in [".github/workflows/build-and-test.yml", ".github/workflows/pull.yml"]:
        with open(filename, "r") as f:
            lines = f.readlines()
        with open(filename, "w") as f:
            for line in lines:
                if line.startswith("  LLVM_COMMIT:"):
                    f.write("  LLVM_COMMIT: " + sys.argv[1] + "\n")
                else:
                    f.write(line)
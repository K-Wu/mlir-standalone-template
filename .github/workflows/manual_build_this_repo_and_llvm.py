# execute this script and all functions within from the git root folder

from get_commit_hash_from_yml import get_ref_from_env, ensure_executed_in_git_root
import os

def manual_clone_llvm_project(llvm_dir, git_ref):
    # create a new folder and execute git init
    os.system("mkdir {llvm_dir}".format(llvm_dir=llvm_dir))
    os.chdir("{llvm_dir}".format(llvm_dir=llvm_dir))
    os.system("git init")
    os.system("git remote add origin https://github.com/llvm/llvm-project.git")
    os.system("git fetch --depth 1 origin +" + git_ref)
    os.system("git checkout FETCH_HEAD")
    # go back to the root folder
    os.chdir("..")



def manual_build_llvm_project(git_ref, enable_mlir_python_bindings):
    # TODO: add an option to choose whether to build python bindings
    # To build python bindings, add the two flags specified in the documentation to the cmake command, e.g.:
    # -DMLIR_ENABLE_BINDINGS_PYTHON=ON -DMLIR_INCLUDE_TESTS=ON -DPython3_EXECUTABLE=/home/kwu/anaconda3/envs/dev_mlir/bin/python3
    # Notice that Python3_EXECUTABLE needs to be the same as the one used in run time. Otherwise ImportError (unknown location) will be thrown.
    # https://mlir.llvm.org/docs/Bindings/Python/#building

    os.system("mkdir llvm-project/build")
    os.system("mkdir llvm-project/prefix")
    os.chdir("llvm-project/build")
    cmake_configure_command = "cmake ../llvm -DCMAKE_BUILD_TYPE=Release -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ -DLLVM_ENABLE_ASSERTIONS=ON -DLLVM_BUILD_EXAMPLES=OFF -DLLVM_TARGETS_TO_BUILD=\"host\" -DCMAKE_INSTALL_PREFIX=../prefix -DLLVM_ENABLE_PROJECTS='mlir' -DLLVM_OPTIMIZED_TABLEGEN=ON -DLLVM_ENABLE_OCAMLDOC=OFF -DLLVM_ENABLE_BINDINGS=OFF -DLLVM_INSTALL_UTILS=ON -DLLVM_ENABLE_LLD=ON"
    
    if enable_mlir_python_bindings:
        # get python3 executable path by executing which python3
        python3_executable_path = os.popen("which python3").read().strip()

        cmake_configure_command += " -DMLIR_ENABLE_BINDINGS_PYTHON=ON -DMLIR_INCLUDE_TESTS=ON -DPython3_EXECUTABLE={python3_executable_path}".format(python3_executable_path=python3_executable_path)
    os.system(cmake_configure_command)
    os.system("cmake --build . --target install")
    os.chdir("../..")

MANUAL_CMAKE_FLAGS = '-DCMAKE_LINKER=lld -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ -DMLIR_DIR={github_repo_root}/llvm-project/prefix/lib/cmake/mlir/ -DLLVM_DIR={github_repo_root}/llvm-project/prefix/lib/cmake/llvm/ -DLLVM_EXTERNAL_LIT={github_repo_root}/llvm-project/build/bin/llvm-lit'

def manual_sanitizer_build(): 
    github_repo_root = os.getcwd()   
    os.system("mkdir sanitizer-build")
    os.chdir("sanitizer-build")
    os.system("cmake .. -DCMAKE_BUILD_TYPE=Debug -DUSE_SANITIZER='Address;Undefined' " + MANUAL_CMAKE_FLAGS.format(github_repo_root=github_repo_root))
    os.system("cmake --build . --target check-standalone")
    os.chdir("..")

def manual_release_build():
    github_repo_root = os.getcwd()
    os.system("mkdir build")
    os.chdir("build")
    os.system("cmake .. -DCMAKE_BUILD_TYPE=Release " + MANUAL_CMAKE_FLAGS.format(github_repo_root=github_repo_root))
    os.system("cmake --build . --target check-standalone")
    os.chdir("..")

def get_hash(llvm_dir):
    os.chdir(llvm_dir)
    # read from git rev-parse HEAD
    git_hash = os.popen("git rev-parse HEAD").read().strip()
    os.chdir("..")
    return git_hash

if __name__ == "__main__":
    ensure_executed_in_git_root()

    git_ref = get_ref_from_env()
    # skip if 1) the folder exists and 2) the git_ref is the same
    if os.path.exists("llvm-project"):
        # clone the llvm-project again to check if the two hash match
        manual_clone_llvm_project("llvm-project2",git_ref)
        if get_hash("llvm-project") == get_hash("llvm-project2"):
            print("The git_ref is the same. Skip.")
            os.system("rm -rf llvm-project2")
        else:
            print("The git_ref is different. Re-clone.")
            print("llvm-project git_ref is " + get_hash("llvm-project"))
            print("llvm-project git_ref spec is " + get_hash("llvm-project2"))
            os.system("rm -rf llvm-project")
            os.system("mv llvm-project2 llvm-project")
    else:
        manual_clone_llvm_project("llvm-project", git_ref)
    manual_build_llvm_project(git_ref, enable_mlir_python_bindings=False)
    manual_release_build()
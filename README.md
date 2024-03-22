# FIRO Catkin Workspace
Preconfigured catkin workspace recommended for developing ROS 1 Noetic packages.

## Overview
The goal of this workspace is to assist in developing consistent and high-quality code that conforms to the ROS 1 Noetic coding standards.

In particular, this workspace provides:
- **Clang-Tidy** configuration for C++ static code analysis
- **ClangFormat** configuration for C++ code formatting
- **`cmake-format`** configuration for CMake code formatting
- **Visual Studio Code** recommended settings, extensions, and default tasks

Visual Studio Code will also utilize the following tools:
- **`catkin_lint`** for static analysis of catkin packages
- **Ccache** to speed up compilation
- **Cppcheck** for additional C++ static code analysis
- **YAPF** for Python code formatting

## Usage

The primary assumption is that you will be using Visual Studio Code as your IDE. If you choose a different IDE, you will need to configure most of the tools yourself. Assuming Visual Studio Code is installed, follow the steps in the [Setup](#setup) section to install the required tools and configure your environment.

It is important to note that this workspace uses catkin-tools instead of the default catkin_make. This should be of no concern as long as you use the provided tasks in Visual Studio Code. However, you may want to change the default build settings, such as the number of parallel jobs or setting the build type to `Debug`. You can easily do this with the `catkin config` command, i.e., `catkin config --cmake-args -DCMAKE_BUILD_TYPE=Debug -j4`.

If you decide to run `catkin build` from the terminal, C++ linting will fail, as Clang won't find an up-to-date `compile_commands.json` file. Therefore, it is recommended to use the provided task in Visual Studio Code or at least follow the same steps to generate the `compile_commands.json` file in the build directory.

During development, your C++, Python, and CMake code will be automatically formatted upon saving the file. C++ code will also be analyzed for potential issues with both Clang-Tidy and Cppcheck, which will display any issues in the Problems tab in Visual Studio Code. After adding new includes to your C++ code, you will need to run the default build task to update the Clang Compilation Database.

The default build task will build all packages in the workspace. This will also run `catkin_lint` on all packages, except those placed in the `src/external` directory. All errors and warnings will be displayed at the end of the terminal running the build task.

### Summary
1. Carefully follow the [Setup](#setup) section.
2. Use Visual Studio Code as your IDE.
3. Your code will be automatically formatted after saving.
4. Build all packages in your workspace using the default build task (Ctrl+Shift+B).
5. Pay attention to any squiggly lines in your code and the "Problems" tab in Visual Studio Code, as they report issues in your code.
6. Run the build task after adding new includes to your C++ code.
7. After each build, check the terminal for `catkin_lint` warnings and errors.

## Setup
Assuming you already have ROS 1 Noetic and Visual Studio Code installed, follow these steps to set up your workspace:
1. Clone this repository to your desired location:
    ```bash
    git clone https://github.com/rxsio/firo-catkin-workspace.git
    ```
2. Install Clang-Tidy, ClangFormat, Ccache, and Cppcheck:

    Some tools may already be installed on your system, or Visual Studio Code may prompt you to install them. However, manually installing them is recommended to ensure the use of modern versions. Especially, the default Clang-Tidy version on Ubuntu 20.04 may incorrectly report the usage of ROS Macros.

    The easiest way to install recent versions of these tools is to use the `setup-cpp` script from [this repository](https://github.com/aminya/setup-cpp). Check the repository for the most recent version of the script and installation instructions. To download the script on Ubuntu 20.04, use the following commands:
    ```bash
    wget "https://github.com/aminya/setup-cpp/releases/download/v0.37.0/setup-cpp-x64-linux"
    chmod +x ./setup-cpp-x64-linux
    ```

    After downloading the script, you can install the tools by running the following command:
    ```bash
    sudo ./setup-cpp-x64-linux --cppcheck true --clangtidy true --clangformat true --ccache true
    source ~/.cpprc
    ```
3. Install `cmake-format`, YAPF, Catkin Tools, and `catkin_lint` using pip
    ```bash
    pip install --user cmakelang yapf catkin_tools catkin-lint
    ```
    This assumes your local bin directory is in your PATH. If it is not, the commands for `cmake-format`, `yapf`, `catkin`, and `catkin_lint` will not be found. To fix this, manually add your local bin directory to the PATH variable or run the following command:
    ```bash
    echo -e "\nexport PATH=\"${HOME}/.local/bin:\$PATH\"" >> ~/.bashrc
    source ~/.bashrc
    ```
4. Test that everything is installed correctly by running the following commands:
    ```bash
    clang-tidy --version
    clang-format --version
    cmake-format --version
    ccache --version
    cppcheck --version
    yapf --version
    catkin --version
    catkin_lint --version
    ```
    If something is missing, repeat the installation steps for the missing tools and pay attention to any error messages.
5. It is recommended to change the default build type to `Debug` for more precise debugger information. You can do this by running the following command:
    ```bash
    catkin config --cmake-args -DCMAKE_BUILD_TYPE=Debug
    ```
6. Open the workspace in Visual Studio Code:
    ```bash
    code firo-catkin-workspace
    ```
    You will be prompted to install recommended extensions (Install All). If you don't see the prompt, you can manually install them by clicking on the Extensions icon in the Sidebar and filtering with the `@recommended` keyword. 
7. Clone any packages you want to work on into the `src` directory. If you also need to clone packages that are not under your control, place them in the `src/external` directory. These packages will not be linted by `catkin_lint` during the build process.
8. Verify that everything is set up correctly by running the default build task (Ctrl+Shift+B). You should see the build output in the terminal and any issues reported by `catkin_lint` at the end of the build process. Additionally, if you have any C++ files open, you can intentionally introduce some issues to see if Clang-Tidy and Cppcheck are working correctly. You can use the example provided on the cppcheck [website](https://cppcheck.sourceforge.io/):
    ```c++
    void foo(int x)
    {
        int buf[10];
        buf[x] = 0; // <- ERROR
        if (x == 1000) {}
    }
    ```

## Common Issues
### Clang-Tidy reports errors inside ROS Macros
1. Verify that you have installed Clang-Tidy version 14 or newer.
    ```bash
    clang-tidy --version
    ```
2. Ensure you correctly flag ROS and external ROS packages as system headers in your package's `CMakeLists.txt`, i.e.:
    ```cmake
    include_directories(SYSTEM ${catkin_INCLUDE_DIRS})
    ```
    Missing the `SYSTEM` flag will cause Clang-Tidy to report errors inside ROS Macros and external ROS packages.
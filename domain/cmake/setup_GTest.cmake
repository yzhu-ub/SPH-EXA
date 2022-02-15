#####################################################
# GTest, find system first, download if necessary
#####################################################
find_package(GTest)

if (NOT GTest_FOUND)
    message("-- Configure GTest from github")
    project(googletest-git NONE)

    include(FetchContent)
    FetchContent_Declare(
      googletest
      GIT_REPOSITORY https://github.com/google/googletest.git
      GIT_TAG        release-1.11.0
    )

    # Check if population has already been performed
    FetchContent_GetProperties(googletest)
    if(NOT googletest_POPULATED)
        message("-- Downloading GTest from github")
        # Fetch the content using previously declared details
        FetchContent_Populate(googletest)

        # Prevent overriding the parent project's compiler/linker
        # settings on Windows
        set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)

        # Bring the populated content into the build
        add_subdirectory(${googletest_SOURCE_DIR} ${googletest_BINARY_DIR})
    endif()
endif()

if (NOT TARGET GTest::gtest_main)
    message("Target GTest:: stuff MISSING")
endif()

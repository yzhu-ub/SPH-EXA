#pragma once

#include <tuple>
#include <omp.h>
#include "version.h"

namespace sphexa
{

auto initMpi()
{
    int rank     = 0;
    int numRanks = 0;
    MPI_Init(NULL, NULL);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &numRanks);
    if (rank == 0)
    {
        int mpi_version, mpi_subversion;
        printf("# SPHEXA: %s/%s\n", GIT_BRANCH, GIT_COMMIT_HASH);
        MPI_Get_version(&mpi_version, &mpi_subversion);
#ifdef _OPENMP
        omp_set_num_threads(1);
        printf("# %d MPI-%d.%d process(es) with %d OpenMP-%u thread(s)/process\n", numRanks, mpi_version,
               mpi_subversion, omp_get_num_threads(), _OPENMP);
#else
        printf("# %d MPI-%d.%d process(es) without OpenMP\n", numRanks, mpi_version, mpi_subversion);
#endif
    }
    return std::make_tuple(rank, numRanks);
}

int exitSuccess()
{
    MPI_Finalize();
    return EXIT_SUCCESS;
}

} // namespace sphexa

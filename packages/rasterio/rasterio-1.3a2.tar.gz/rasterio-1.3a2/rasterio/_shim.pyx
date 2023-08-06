# cython: language_level=3, boundscheck=False

"""Rasterio shims for GDAL 3.x"""

include "directives.pxi"

# The baseline GDAL API.
include "gdal.pxi"

# Shim API for GDAL >= 3.0
include "shim_rasterioex.pxi"


# Declarations and implementations specific for GDAL >= 3.x
cdef extern from "gdal.h" nogil:

    cdef CPLErr GDALDeleteRasterNoDataValue(GDALRasterBandH hBand)
    GDALDatasetH GDALOpenEx(const char *filename, int flags, const char **allowed_drivers, const char **options, const char **siblings) # except -1


cdef extern from "ogr_srs_api.h" nogil:

    ctypedef enum OSRAxisMappingStrategy:
        OAMS_TRADITIONAL_GIS_ORDER

    const char* OSRGetName(OGRSpatialReferenceH hSRS)
    void OSRSetAxisMappingStrategy(OGRSpatialReferenceH hSRS, OSRAxisMappingStrategy)
    void OSRSetPROJSearchPaths(const char *const *papszPaths)


from rasterio._err cimport exc_wrap_pointer


cdef GDALDatasetH open_dataset(
        object filename, int flags, object allowed_drivers,
        object open_options, object siblings) except NULL:
    """Open a dataset and return a handle"""


    cdef char **drivers = NULL
    cdef char **options = NULL
    cdef GDALDatasetH hds = NULL
    cdef const char *fname = NULL

    filename = filename.encode('utf-8')
    fname = filename

    # Construct a null terminated C list of driver
    # names for GDALOpenEx.
    if allowed_drivers:
        for name in allowed_drivers:
            name = name.encode('utf-8')
            drivers = CSLAddString(drivers, <const char *>name)

    if open_options:
        for k, v in open_options.items():
            k = k.upper().encode('utf-8')

            # Normalize values consistent with code in _env module.
            if isinstance(v, bool):
                v = ('ON' if v else 'OFF').encode('utf-8')
            else:
                v = str(v).encode('utf-8')

            options = CSLAddNameValue(options, <const char *>k, <const char *>v)

    # Support for sibling files is not yet implemented.
    if siblings:
        raise NotImplementedError(
            "Sibling files are not implemented")

    # Ensure raster flags
    flags = flags | 0x02

    with nogil:
        hds = GDALOpenEx(fname, flags, drivers, options, NULL)
    try:
        return exc_wrap_pointer(hds)
    finally:
        CSLDestroy(drivers)
        CSLDestroy(options)


cdef int delete_nodata_value(GDALRasterBandH hBand) except 3:
    return GDALDeleteRasterNoDataValue(hBand)


cdef const char* osr_get_name(OGRSpatialReferenceH hSrs):
    return OSRGetName(hSrs)


cdef void osr_set_traditional_axis_mapping_strategy(OGRSpatialReferenceH hSrs):
    OSRSetAxisMappingStrategy(hSrs, OAMS_TRADITIONAL_GIS_ORDER)


cdef void set_proj_search_path(object path):
    cdef char **paths = NULL
    cdef const char *path_c = NULL
    path_b = path.encode("utf-8")
    path_c = path_b
    paths = CSLAddString(paths, path_c)
    OSRSetPROJSearchPaths(paths)

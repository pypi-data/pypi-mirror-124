# -*- coding: utf-8 -*-

# py_tools_ds - A collection of geospatial data analysis tools that simplify standard
# operations when handling geospatial raster and vector data as well as projections.
#
# Copyright (C) 2016-2021
# - Daniel Scheffler (GFZ Potsdam, daniel.scheffler@gfz-potsdam.de)
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences Potsdam,
#   Germany (https://www.gfz-potsdam.de/)
#
# This software was developed within the context of the GeoMultiSens project funded
# by the German Federal Ministry of Education and Research
# (project grant code: 01 IS 14 010 A-C).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__author__ = "Daniel Scheffler"

from shapely.wkb import loads
from osgeo import gdal, osr, ogr

from ...io.raster.gdal import get_GDAL_ds_inmem
from ...processing.progress_mon import ProgressBar, Timer
from ..raster.reproject import warp_ndarray
from ..vector.topology import get_bounds_polygon, polyVertices_outside_poly, get_overlap_polygon


def raster2polygon(array, gt, prj, DN2extract=1, exact=True, maxfeatCount=None,
                   timeout=None, progress=True, q=False):
    """Calculate a footprint polygon for the given array.

    :param array:             2D numpy array
    :param gt:                GDAL GeoTransform
    :param prj:               projection as WKT string, 'EPSG:1234' or <EPSG_int>
    :param DN2extract:        <int, float> pixel value to create polygons for
    :param exact:             whether to compute the exact footprint polygon or a simplified one for speed
    :param maxfeatCount:      <int> the maximum expected number of polygons. If more polygons are found, every further
                              processing is cancelled and a RunTimeError is raised.
    :param timeout:           breaks the process after a given time in seconds
    :param progress:          show progress bars (default: True)
    :param q:                 quiet mode (default: False)
    :return:
    """
    assert array.ndim == 2, "Only 2D arrays are supported. Got a %sD array." % array.ndim
    gt_orig = gt
    shape_orig = array.shape

    # downsample input array in case it has more than 1e8 pixels to prevent crash
    if not exact and array.size > 1e8:  # 10000 x 10000 px
        # downsample with nearest neighbour
        zoom_factor = (8000 * 8000 / array.size) ** 0.5
        array, gt, prj = warp_ndarray(array, gt, prj,
                                      out_gsd=(gt[1] / zoom_factor,
                                               gt[5] / zoom_factor),
                                      rspAlg='near',
                                      q=True)

    src_ds = get_GDAL_ds_inmem(array, gt, prj)
    src_band = src_ds.GetRasterBand(1)

    # Create a memory OGR datasource to put results in.
    mem_drv = ogr.GetDriverByName('Memory')
    mem_ds = mem_drv.CreateDataSource('out')

    srs = osr.SpatialReference()
    srs.ImportFromWkt(prj)

    mem_layer = mem_ds.CreateLayer('poly', srs, ogr.wkbPolygon)

    fd = ogr.FieldDefn('DN', ogr.OFTInteger)
    mem_layer.CreateField(fd)

    # set callback
    callback = \
        ProgressBar(prefix='Polygonize progress    ',
                    suffix='Complete',
                    barLength=50,
                    timeout=timeout,
                    use_as_callback=True) \
        if progress and not q else Timer(timeout, use_as_callback=True) if timeout else None

    # run the algorithm
    status = gdal.Polygonize(src_band,
                             src_band.GetMaskBand(),
                             mem_layer,
                             0,
                             ["8CONNECTED=8"] if exact else [],
                             callback=callback)

    # handle exit status other than 0 (fail)
    if status != 0:
        errMsg = gdal.GetLastErrorMsg()

        # Catch the KeyboardInterrupt raised in case of a timeout within the callback. It seems like there is no other
        # way to catch exceptions within callbacks.
        if errMsg == 'User terminated':
            raise TimeoutError('raster2polygon timed out!')

        raise Exception(errMsg)

    # extract polygon
    mem_layer.SetAttributeFilter('DN = %s' % DN2extract)

    from geopandas import GeoDataFrame
    featCount = mem_layer.GetFeatureCount()

    if not featCount:
        raise RuntimeError('No features with DN=%s found in the input image.' % DN2extract)
    if maxfeatCount and featCount > maxfeatCount:
        raise RuntimeError('Found %s features with DN=%s but maximum feature count was set to %s.'
                           % (featCount, DN2extract, maxfeatCount))

    # tmp = np.full((featCount,2), DN, geoArr.dtype)
    # tmp[:,0] = range(featCount)
    # GDF = GeoDataFrame(tmp, columns=['idx','DN'])

    # def get_shplyPoly(GDF_row):
    #    if not is_timed_out(3):
    #        element   = mem_layer.GetNextFeature()
    #        shplyPoly = loads(element.GetGeometryRef().ExportToWkb()).buffer(0)
    #        element   = None
    #        return shplyPoly
    #    else:
    #        raise TimeoutError

    # GDF['geometry'] = GDF.apply(get_shplyPoly, axis=1)

    GDF = GeoDataFrame(columns=['geometry', 'DN'])
    GDF.DN = GDF.DN.astype(float)
    timer = Timer(timeout)
    for i in range(featCount):
        if not timer.timed_out:
            element = mem_layer.GetNextFeature()
            wkb = bytes(element.GetGeometryRef().ExportToWkb())
            GDF.loc[i] = [loads(wkb).buffer(0), DN2extract]
            del element
        else:
            raise TimeoutError('raster2polygon timed out!')

    GDF = GDF.dissolve(by='DN')

    del mem_ds, mem_layer

    shplyPoly = GDF.loc[1, 'geometry']

    # the downsampling in case exact=False may cause vertices of shplyPoly to be outside the input array bounds
    # -> clip shplyPoly with bounds_poly in that case
    if not exact:
        bounds_poly = get_bounds_polygon(gt_orig, *shape_orig)

        if polyVertices_outside_poly(shplyPoly, bounds_poly, 1e-5):
            shplyPoly = get_overlap_polygon(shplyPoly, bounds_poly)['overlap poly']

    return shplyPoly

# -*- coding: utf-8 -*-

__author__ = 'gusbos'
from xml.etree import ElementTree as ET
from shapely.wkt import loads
from shapely.geometry import mapping
import geojson
import sys

sample_sam_file_path = "sami_export_AB5848_2014.xml"

def get_blocks_wkt(sam_file_path):
    r"""
    >>> block_list = get_blocks_wkt("sami_export_AB5848_2014.xml")
    >>> len(block_list)
    16
    >>> get_blocks_wkt()[0]
    ('18894514', 'POLYGON((1647781.623 6609603.909,1647795.089 6609604.778,1647811.595\n                        6609603.909,1647819.414 6609601.303,1647829.839 6609596.09,1647896.48 6609588.93,1647905.082\n                        6609589.383,1647922.796 6609599.565,1647928.443 6609593.918,1647935.827 6609573.502,1647945.818\n                        6609554.39,1647956.678 6609543.096,1647969.37 6609526.905,1647977.972 6609517.398,1647985.669\n                        6609511.512,1647996.64 6609512.255,1648030.49 6609492.045,1648032.753 6609486.612,1648030.037\n                        6609485.254,1648013.738 6609488.423,1648007.853 6609487.97,1647979.783 6609471.219,1647978.425\n                        6609466.692,1647990.196 6609427.756,1647989.043 6609423.172,1647931.74 6609400.755,1647920.208\n                        6609393.921,1647916.28 6609391.945,1647899.956 6609383.728,1647895.415 6609383.161,1647889.577\n                        6609384.222,1647888.88 6609384.484,1647881.226 6609389.404,1647877.731 6609391.628,1647858.523\n                        6609404.161,1647845.332 6609411.692,1647822.229 6609430.464,1647823.134 6609437.504,1647826.917\n                        6609442.547,1647860.261 6609448.129,1647871.944 6609448.311,1647880.59 6609446.69,1647885.614\n                        6609443.149,1647891.5 6609442.697,1647892.405 6609445.866,1647885.614 6609464.881,1647876.318\n                        6609486.192,1647877.012 6609493.403,1647872.485 6609503.816,1647856.455 6609524.318,1647849.43\n                        6609536.025,1647841.686 6609541.969,1647831.239 6609549.534,1647824.948 6609557.239,1647820.873\n                        6609566.746,1647817.371 6609573.669,1647809.806 6609584.115,1647795.067 6609592.099,1647781.623\n                        6609603.909),(1647890.218 6609554.824,1647895.122 6609541.393,1647900.555 6609539.582,1647906.44\n                        6609540.035,1647908.704 6609542.751,1647909.609 6609546.373,1647906.44 6609551.806,1647896.299\n                        6609563.077,1647888.915 6609562.643,1647890.218 6609554.824))\n                    ')
    """
    xml_file = open(sam_file_path,"r", encoding="latin1")
    with xml_file:
        sam_xml =ET.parse(xml_file)
        return [(parcel.find("SDEPARCELID").text,parcel.find("POLYGON").text) for parcel in sam_xml.findall(".//PARCELS/PARCEL")]


def create_shapes_from_wkt_blocks(sam_file_path):
    wkt_blocks = get_blocks_wkt(sam_file_path)
    polygons = []
    for (id,wkt) in wkt_blocks:
        polygons.append(create_polygon(id,wkt))

    return polygons


def create_polygon(id,wkt):
    return (id,loads(wkt))


def add_projection(feature_collection):
    """
    Adds CRS projection specification E g:
    "crs": {
        "type": "name",
        "properties": {
          "name": "EPSG:3847"
        }
      }
    :param feature_collection:
    :return: feature_collection
    """
    feature_collection["crs"] = {"type":"name","properties":{"name":"EPSG:3847"}}
    return feature_collection


def main(sam_file_path):
    polygons = create_shapes_from_wkt_blocks(sam_file_path)
    feature_collection = convert_to_geojson(polygons)
    feature_collection_with_projection = add_projection(feature_collection)
    print(feature_collection_with_projection)


def convert_to_geojson(polygons):
    features = [geojson.Feature(id=id, geometry=mapping(polygon)) for id, polygon in polygons]
    feature_collection = geojson.FeatureCollection(features)
    return feature_collection


if __name__ == '__main__':
    main(sys.argv[1])

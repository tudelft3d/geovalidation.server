
<div class="page-header">
    <h1>about</h1>
</div>

The validator, which uses the open-source project [val3dity](https://github.com/tudelft3d/val3dity) in the background, is maintained by [Hugo Ledoux](https://3d.bk.tudelft.nl/hledoux) and the [3D geoinformation group at TUDelft](https://3d.bk.tudelft.nl).

It allows us to validate 3D primitives according to the international standard ISO19107.

In short, it verifies whether a 3D primitive respects the definition as given in [ISO 19107](http://www.iso.org/iso/catalogue_detail.htm?csnumber=26012) and [GML](https://en.wikipedia.org/wiki/Geography_Markup_Language).

The validation of the following 3D primitives is fully supported:

  - ``MultiSurface``
  - ``CompositeSurface>`` 
  - ``Solid``
  - ``MultiSolid``
  - ``CompositeSolid``

Unlike many other validation tools in 3D GIS, inner rings in polygons/surfaces are supported and so are cavities in solids (also called voids or inner shells).
However, as is the case for many formats used in practice, only planar and linear primitives are allowed: no curves or spheres or other parametrically-modelled primitives are supported. 
There is no plan to support these geometries.

val3dity accepts as input:

  - [GML files](https://en.wikipedia.org/wiki/Geography_Markup_Language) of any flavour
  - [CityJSON](http://www.cityjson.org)
  - [CityGML (v1 & v2 only, v3 will not be supported)](https://www.citygml.org)
  - [IndoorGML](http://indoorgml.net/)
  - [OBJ](https://en.wikipedia.org/wiki/Wavefront_.obj_file)
  - [OFF](https://en.wikipedia.org/wiki/OFF_(file_format))

For the City/JSON/GML and IndoorGML formats, extra validations (specific to the format) are performed, eg the overlap between different parts of a building, or the validation of the navigation graph in IndoorGML.


### Documentation

val3dity has an [extensive documentation](https://val3dity.rtfd.io).

### Bugs?

If you encounter a bug, please report it on the [issue page](https://github.com/tudelft3d/val3dity/issues).


### Source code

The [source code of the validator](https://github.com/tudelft3d/val3dity) is publicly available.
The version used online is always the latest commit in master branch.


### If you use val3dity in a scientific context, please cite these articles:


Ledoux, Hugo (2019). val3dity: validation of 3D GIS primitives according to the international standards. *Open Geospatial Data, Software and Standards*, 3(1), 2018, pp.1 [DOI](http://dx.doi.org/10.1186/s40965-018-0043-x) 

Ledoux, Hugo (2013). On the validation of solids represented with the international standards for geographic information. Computer-Aided Civil and Infrastructure Engineering, 28(9):693-706. [PDF](https://3d.bk.tudelft.nl/hledoux/pdfs/13_cacaie.pdf) [DOI](http://dx.doi.org/10.1111/mice.12043)

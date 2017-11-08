
<div class="page-header">
    <h1>about</h1>
</div>

The validator, which uses the open-source project [val3dity](https://github.com/tudelft3d/val3dity) in the background, is maintained by [Hugo Ledoux](https://3d.bk.tudelft.nl/hledoux) and the [3D geoinformation group at TUDelft](https://3d.bk.tudelft.nl).

It allows us to validate 3D primitives according to the international standard ISO19107.
Think of it as [PostGIS ST_IsValid](http://postgis.net/docs/ST_IsValid.html), but for 3D primitives (PostGIS only validates 2D primitives).

In short, it verifies whether a 3D primitive respects the definition as given in [ISO19107](http://www.iso.org/iso/catalogue_detail.htm?csnumber=26012) and GML/CityGML.
All the 3D primitives of GML are supported:

  - `<gml:MultiSurface>`
  - `<gml:CompositeSurface>` 
  - `<gml:Solid>`
  - `<gml:MultiSolid>`
  - `<gml:CompositeSolid>`

Unlike many other validation tools in 3D GIS, inner rings in polygons/surfaces are supported and so are cavities in solids (also called voids or inner shells).
However, as is the case for CityGML, only planar and linear primitives are allowed: no curves or spheres or other parametrically-modelled primitives are supported. There is no plan to support these geometries, because val3dity is developed with 3D city models in focus.

val3dity accepts as input:

  - [CityGML](https://www.citygml.org)
  - [CityJSON](http://www.cityjson.org)
  - any [GML files](https://en.wikipedia.org/wiki/Geography_Markup_Language) 
  - [OBJ](https://en.wikipedia.org/wiki/Wavefront_.obj_file)
  - [OFF](https://en.wikipedia.org/wiki/OFF_(file_format))


### Documentation

val3dity has a fairly [extensive documentation](http://geovalidation.bk.tudelft.nl/val3dity/docs/).

### Bugs?

If you encounter a bug, please report it on the [issue page](https://github.com/tudelft3d/val3dity/issues).


### Source code

The [source code of the validator](https://github.com/tudelft3d/val3dity) is publicly available.
The version used online is always the latest commit in master branch.

### Acknowledgement

If you use val3dity for research-purposes and publish, please cite that scientific article (which contains all the details):

> Ledoux, Hugo (2013). On the validation of solids represented with the
international standards for geographic information. *Computer-Aided Civil and Infrastructure Engineering*, 28(9):693-706. 
<a href="http://dx.doi.org/10.1111/mice.12043"><i class="fa fa-external-link"></i></a> <a href="https://3d.bk.tudelft.nl/hledoux/pdfs/13_cacaie.pdf"><i class="fa fa-file-pdf-o"></i></a>

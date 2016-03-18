
<div class="page-header">
    <h1>about</h1>
</div>

The validator, which uses the open-source project [val3dity](https://github.com/tudelft3d/val3dity) in the background, checks whether the 3D primitives (__Solids__, __CompositeSurfaces__, or __MultiSurfaces__)  are *geometrically* valid according to the international standard [ISO 19107:2003](http://www.iso.org/iso/catalogue_detail.htm?csnumber=26012). 

If you encounter a bug, please report it on the [issue page](https://github.com/tudelft3d/val3dity/issues) or contact me (<a href="http://www.tudelft.nl/hledoux">Hugo Ledoux</a>) directly.


It accepts as input any GML files (or one of the formats built upon it, such as CityGML), OBJ, OFF, and [POLY](http://wias-berlin.de/software/tetgen/1.5/doc/manual/manual006.html#ff_poly).
It simply scans the file looking for the 3D primitives and validates these according to the rules in ISO19107 (all the rest is ignored). 

<p><img width='500' src="{{ url_for('static', filename='img/workflow.svg') }}" alt="" /></p>

For __Solids__, the validation is performed hierarchically, ie first every polygon (embedded in 3D) is validated (by projecting it to a 2D plane and using [GEOS](http://trac.osgeo.org/geos/)), then every shell is validated (must be watertight, no self-intersections, orientation of the normals must be consistent and pointing outwards, etc), and finally the interactions between the shells are analysed. 
This means that if a polygon of your solid is not valid, the validator will report that error but will *not* continue the validation (to avoid "cascading" errors). 

For __MultiSurfaces__, only the validation of the polygons is performed, ie are they valid according to the 2D rules, and are they planar?

For __CompositeSurfaces__, the surface formed by the polygons must be a 2-manifold.

More details are available in this [blog post about 3D solids in GIS](https://3d.bk.tudelft.nl/hledoux/blog/your-solids-the-same/).

### Error codes

These <a href="{{  url_for("errors")  }}">errors</a> can be reported.

### Source code

The [source code of the validator](https://github.com/tudelft3d/val3dity) is publicly available.
The version used online is always the latest commit in master branch.

### Acknowledgement

If you use val3dity for research-purposes and publish, please cite that scientific article (which contains all the details):

> Ledoux, Hugo (2013). On the validation of solids represented with the
international standards for geographic information. *Computer-Aided Civil and Infrastructure Engineering*, 28(9):693-706. 
<a href="http://dx.doi.org/10.1111/mice.12043"><i class="fa fa-external-link"></i></a> <a href="https://3d.bk.tudelft.nl/hledoux/pdfs/13_cacaie.pdf"><i class="fa fa-file-pdf-o"></i></a>


<div class="page-header">
    <h1>about</h1>
</div>

The validator, which uses the open-source project [val3dity](https://github.com/tudelft-gist/val3dity) in the background, checks whether the 3D primitives (__gml:Solid__ or __gml:MultiSurface__) stored in a GML file are *geometrically* valid according to the international standard [ISO 19107:2003](http://www.iso.org/iso/catalogue_detail.htm?csnumber=26012). Any GML files, or one of the formats built upon it (such as CityGML), can be used as input. The validator simply scans the file looking for the __gml:Solid__ or __gml:MultiSurface__ tags and validates these (all the rest is ignored). It assumes that the input XML is syntactically valid according to the XSD of GML.

<p><img width='500' src="{{ url_for('static', filename='img/workflow.svg') }}" alt="" /></p>

The validation is performed hierarchically, ie first every polygon (embedded in 3D) is validated (by projecting it to a 2D plane and using [GEOS](http://trac.osgeo.org/geos/)), then every shell is validated (must be watertight, no self-intersections, orientation of the normals must be consistent and pointing outwards, etc), and finally the interactions between the shells are analysed. This means that if a polygon of your solid is not valid, the validator will report that error but will *not* continue the validation (to avoid "cascading" errors). For __gml:MultiSurfaces__, only the validation of the polygons is performed.

These <a href="{{  url_for("errors")  }}">errors</a> can be reported.

Most of the details of the implementation are available in this scientific article:

> Ledoux, Hugo (2013). On the validation of solids represented with the
international standards for geographic information. *Computer-Aided Civil and Infrastructure Engineering*, 28(9):693-706. 
<a href="http://dx.doi.org/10.1111/mice.12043"><i class="fa fa-external-link"></i></a> <a href="http://3dgeoinfo.bk.tudelft.nl/hledoux/pdfs/_13cacaie.pdf"><i class="fa fa-file-pdf-o"></i></a>

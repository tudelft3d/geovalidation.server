
## about

The validator, which uses the open-source project [val3dity](https://github.com/tudelft-gist/val3dity) in the background, checks whether the solids stored in a GML file are *geometrically* valid according to the international standard [ISO 19107:2003](http://www.iso.org/iso/catalogue_detail.htm?csnumber=26012). Any GML files, or one of the formats built upon it (such as CityGML), can be used as input. The validator simply scans the file looking for the __gml:Solid__ tags and validates these (all the rest is ignored). It assumes that the input XML is syntactically valid according to the XSD of GML.

![](/img/steps.png)

The validation of a solid is performed hierarchically, ie first every surface (a polygon embedded in 3D) is validated in 2D (with [GEOS](http://trac.osgeo.org/geos/)), then every shell is validated (must be watertight, no self-intersections, orientation of the normals must be consistent and pointing outwards, etc), and finally the interactions between the shells are analysed. This means that if a surface of your solid is not a valid 2D polygon (its projection), then the validator will report that error but will *not* try to further validate the solid (to avoid "cascading" errors). For an overview of all the possible errors, [click here](/errors).

Most of the details of the implementation are available in this scientific article:

> Ledoux, Hugo (2013). On the validation of solids represented with the
international standards for geographic information. *Computer-Aided Civil and Infrastructure Engineering*, 28(9):693-706. [ [PDF] ](http://homepage.tudelft.nl/23t4p/pdfs/_13cacaie.pdf) [ [DOI] ](http://dx.doi.org/10.1111/mice.12043)
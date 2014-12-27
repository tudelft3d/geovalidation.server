
<div class="page-header">
    <h1>about</h1>
</div>

prepair--pronounce 'pee-repair' as in 'polygon repair'--permits us to easily repair 'broken' GIS polygons according to the international standard [ISO19107](http://www.iso.org/iso/catalogue_detail.htm?csnumber=26012) (Geographic information--Spatial schema). Given one input polygon (or a MultiPolygon), it *automatically* repairs it and returns back a valid polygon (actually a MultiPolygon since the input can represent more than one polygon--think of a 'bowtie' for instance).

It is an [open-source project](https://github.com/tudelft-gist/prepair) released under the GPL licence. We offer here a simplified version: only the [WKT](http://en.wikipedia.org/wiki/Well-known_text) of a polygon (or MultiPolygon) can be given as input, and it is repaired with an extension of the [odd-even algorithm](https://en.wikipedia.org/wiki/Even-odd_rule) to handle GIS polygons containing inner rings and degeneracies. Also, only rather small WKT are supported.

For repairing bigger polygons in *shapefiles* for instance, or for more repairing options, download the [code](https://github.com/tudelft-gist/prepair) and compile it. 

Most of the details of the implementation are available in this scientific article:

> Ledoux, H., Arroyo Ohori, K., and Meijers, M. (2014). A triangulation-based approach to automatically repair GIS polygons. *Computers & Geosciences* 66:121-131. <a href="http://dx.doi.org/10.1016/j.cageo.2014.01.009"><i class="fa fa-external-link"></i></a> <a href="http://3dgeoinfo.bk.tudelft.nl/hledoux/pdfs/14cgeo_prepair.pdf"><i class="fa fa-file-pdf-o"></i></a>

If you encounter a bug, please report it on the [issue page](https://github.com/tudelft-gist/prepair/issues). 
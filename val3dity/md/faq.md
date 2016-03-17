
<div class="page-header">
    <h1>faq</h1>
</div>

<!--TOC-->

- - -

### What do you do with my uploaded file?

We delete it right after having validated it, we promise. The report is however available to anyone who knows its ID.

- - -

### How should I interpret the report?

<script src="https://gist.github.com/hugoledoux/11082609.js"></script>

The report lists all the 3D primitives with some statistics about them, and gives if invalid one or more <a href="{{  url_for("errors")  }}">errors</a> for each. 

If your your file is a GML file and the primitives have __gml:id__ (for __gml:Solid__ and __gml:Shell__ and __gml:Polygon__) then these are used to report the errors, if not then the number means the order of the primitives in the file (the first one being 0). 
We offer a <a href="{{  url_for("addgmlids")  }}">small service</a> that adds a __gml:id__ to all the __gml:Solid__ in your file. 
Some examples, referring to the example above. 
The first (ID #0) solid in the file is valid, and some of its properties are shown.
The solid with ID #1 is invalid with error 102.
The solid with ID #5 is invalid because its face ID #c6e90d82 is non-planar; if the tolerance was modified to 0.20m then it would be.
The solid with ID #68 is invalid its exterior shell (ID #0) has holes (2 of them).

- - -

### What is the snap tolerance I need to setup when I upload a file?

Geometries modelled in GML store amazingly very little topological relationships. A cube is for instance represented with 6 surfaces, all stored independently. This means that the coordinates xyz of a single vertex (where 3 surfaces "meet") is stored 3 times. It is possible that these 3 vertices are not exactly at the same location (eg (0.01, 0.5, 1.0), (0.011, 0.49999, 1.00004) and (0.01002, 0.5002, 1.0007)), and that would create problems when validating since there would for example be holes in the cube. The snap tolerance basically gives a threshold that says: "if 2 points are closer then *X*, then we assume that they are the same". It's setup by default to be 1mm. 

If the input file is OBJ or OFF, then this doesn't apply.

- - -

### I don't see all the errors in my solid.

It's normal: as shown in the figure below, a solid is validated *hierarchically*, ie first every surface (a polygon embedded in 3D) is validated in 2D (by projecting it to a plane), then every shell is validated, and finally the interactions between the shells are analysed to verify whether the solid is valid. 
If at one stage there are errors, then the validation stops to avoid "cascading errors". So if you get the error `203 NON_PLANAR_POLYGON_DISTANCE_PLANE`, then fix it and re-run the validator again. 
That does mean that you might have to upload your file and get it validated several times---if that becomes too tedious we strongly suggest you to download the [code](https://github.com/tudelft3d/val3dity), compile it and run it locally (it's open-source and free to use).

<p><img width='500' src="{{ url_for('static', filename='img/workflow.svg') }}" alt="" /></p>

- - -

### I'm sure my solid is valid, but the validator says that something is wrong.

It's possible that there are bugs in [val3dity](https://github.com/tudelft3d/val3dity). Please [report the issue](https://github.com/tudelft3d/val3dity/issues).

- - -

### The validation report says that there are no solids in my file, but I can see the buildings with my viewer!

There are many (or more precisely: [too many](http://erouault.blogspot.nl/2014/04/gml-madness.html)) ways to model a volume/polyhedron in GML (eg a building in CityGML), but usually practitioners do it with either __gml:Solid__ or __gml:MultiSurface__. See the same simple volumetric objects, first modelled with a __gml:Solid__ and then with __gml:MultiSurface__:

<script src="https://gist.github.com/hugoledoux/10551725.js"></script>

<script src="https://gist.github.com/hugoledoux/10551979.js"></script>

If your dataset contains volumes but these are stored as __gml:MultiSurfaces__ (eg the [open dataset of Rotterdam](http://www.rotterdamopendata.nl/dataset/rotterdam-3d-bestanden)), then use our [CityGML Solidifier](https://github.com/tudelft3d/citygml-solidifier).

- - -

### Can my GML file contain more than one gml:Solid or gml:MultiSurface?

Yes, all the 3D primitives in the file will be validated, one by one.

- - -

### Do you validate the topological relationships between the solids?

No we don't. Each solid is validated completely independently from the others.

- - -

### The server says my file is too big, what's the maximum?

50MB. If you need more, download the [code](https://github.com/tudelft3d/val3dity), compile it and run it locally.

- - -

### The IDs for the shells and surfaces in the report, are they 0-based or 1-based?

0-based.

- - -

### I don't have IDs for my __gml:Solid__.

We offer a <a href="{{  url_for("addgmlids")  }}">small service</a> that adds a __gml:id__ to all the __gml:Solid__ in your file

- - -

### Where can I get files containing __gml:Solids__?

We maintain a [repository of unit tests](https://github.com/tudelft3d/CityGML-QIE-3Dvalidation) (file containing one solid that has *one* error) for testing our code. 
Also, on the official [CityGML website](http://www.citygml.org/index.php?id=1539) there are a few files with 3D buildings, and on the [CityGML wiki](http://www.citygmlwiki.org/index.php/Open_Data_Initiatives) there are links to rather large datasets of cities (although they do no always contain __gml:Solids__).


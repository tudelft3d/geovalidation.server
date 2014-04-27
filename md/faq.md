
## FAQ

<!--TOC-->

---

### What do you do with my uploaded file?

We delete it right after having validated it, we promise. The report is however available to everyone (if they know its ID).

---

### I don't understand the report I get.

<script src="https://gist.github.com/hugoledoux/11082609.js"></script>

The report lists only the solids that are *not* valid, and gives one or more [errors](/errors) for each. If your solids have __gml:id__ then these are used to report the errors, if not then the number means the order of the solids in the file (the first one being 1). If a surface is reported invalid, then the ID of the surface is also based on the order of the surfaces in one __gml:Shell__; -1 means that it's not relevant. Some examples, referring to the example above. The 25th solid in the file is invalid because the 14th surface of its first shell is non-planar; the 41st solid is invalid because all the normals of its third shell are the wrong orientation (-1 means that the error is for no specific surface); the 666th solid has 2 shells that are face adjacent, one of them being the 2nd one (its 3rd surface is touching another one). All the other solids in the file are valid.

---

### What is the snap tolerance I need to setup when I upload a file?

Geometries modelled in GML store amazingly very little topological relationships. A cube is for instance represented with 6 surfaces, all stored independently. This means that the coordinates xyz of a single vertex (where 3 surfaces "meet") is stored 3 times. It is possible that these 3 vertices are not exactly at the same location (eg (0.01, 0.5, 1.0), (0.011, 0.49999, 1.00004) and (0.01002, 0.5002, 1.0007)), and that would create problems when validating since there would for example be holes in the cube. The snap tolerance basically gives a threshold that says: "if 2 points are closer then *X*, then we assume that they are the same". It's setup by default to be 1mm. 

---

### I don't see all the errors in my solid.

It's normal: as shown in the figure below, a solid is validated *hierarchically*, ie first every surface (a polygon embedded in 3D) is validated in 2D (by projecting it to a plane), then every shell is validated, and finally the interactions between the shells are analysed to verify whether the solid is valid. If at one stage there are errors, then the validation stops to avoid "cascading errors". So if you get the error "210 NON\_PLANAR\_SURFACE", then fix it and re-run the validator again. That does mean that you might have to upload your file and get it validated several times---if that becomes too tedious we strongly suggest you to download the [code](https://github.com/tudelft-gist/val3dity), compile it and run it locally (it's open-source and free to use).

![](/img/steps.png)

---

### I'm sure that my solid is okay, I've double-checked, and yet the validator says that something is wrong.

It's possible that there are bugs in [val3dity](https://github.com/tudelft-gist/val3dity). Please [report the issue](https://github.com/tudelft-gist/val3dity/issues).

---

### The validation report says that there are no solids in my file, but I can see the buildings with my viewer!

There are many (or more precisely: [too many](http://erouault.blogspot.nl/2014/04/gml-madness.html)) ways to model a volume/polyhedron in GML (eg a building in CityGML), but usually practitioners do it with either __gml:Solid__ or __gml:MultiSurface__. See the same simple volumetric objects, first modelled with a __gml:Solid__ and then with __gml:MultiSurface__:

<script src="https://gist.github.com/hugoledoux/10551725.js"></script>

<script src="https://gist.github.com/hugoledoux/10551979.js"></script>

Our validator only checks the former. The reason is simple: if an object is modelled with __gml:MultiSurface__ and the set of surfaces is not watertight, then it would be wrong to report that the object is not valid... However, if a building is watertight, then in our opinion it is good practice to model it with __gml:Solid__.

---

### The server says my file is too big, what's the maximum?

50MB. If you need more, [get in touch](/contact) or download the [code](https://github.com/tudelft-gist/val3dity), compile it and run val3dity locally.

---

### In the report, the ID for the shells and surfaces, are they 0-based or 1-based?

1-based.





## FAQ

<!--TOC-->

---

### What do you do with my uploaded file?

We delete it right after having validated it, we promise. The report is however available to everyone (if they know its ID).

---

### I don't understand the report I get.

<script src="https://gist.github.com/hugoledoux/11082609.js"></script>

The report lists only the solids that are *not* valid, and gives one or more [errors](/errors) for each. If your solids have *gml:id* then these are used to report the errors, if not then the number means the order of the solids in the file (the first one being 0). If a surface is reported invalid, then the id of the surface is also based on the order of the surfaces in one *gml:Shell*. For instance, in the example above the 15th surface listed in the first shell of the 26th solid is not planar. 

---

### What is the snap tolerance I need to setup when I upload a file?

Geometries modelled in GML store amazingly very little topological relationships. A cube is for instance represented with 6 surfaces, all stored separately. This means that a single vertex (where 3 surfaces "meet") is stored independently 3 times (its coordinates xyz). It is possible that these 3 vertices are not exactly at the same location (eg (0.01, 0.5, 1.0) and (0.01002, 0.5002, 1.0007)), and that would create problems when validating since there would be holes in the cube. The snap tolerance basically gives a threshold that says: "if 2 points are closer then X, then we assume that they are the same". It's setup by default to me 1mm. 

---

### I don't see all the errors in my solid.

It's normal: as shown in the figure below, a solid is validated *hierarchically*, ie first every surface (a polygon embedded in 3D) is validated in 2D, then every shell is validated, and finally the interactions between the shells are analysed. If at one stage there are errors then we don't continue the validation to avoid "cascading errors". So if you get the error "210 NON_PLANAR_SURFACE", then fix it re-run the validator. That does mean that you might have to upload your file and get it validated several times; if that becomes too tedious we strongly suggest you to download the [code](https://github.com/tudelft-gist/val3dity), compile it and run val3dity locally (it's open-source and free to use).

![](/static/steps.png)

---

### I'm sure that my solid is okay, I've double-checked, and yet the validator says that something is wrong.

It's possible that there are bugs in [val3dity](https://github.com/tudelft-gist/val3dity). Please [report the issue](https://github.com/tudelft-gist/val3dity/issues).

---

### The validation report says that there is no solids in my file, but I can see the buildings with my viewer!

There are many (or more precisely: [too many](http://erouault.blogspot.nl/2014/04/gml-madness.html)) ways to model a volume/polyhedron in GML (eg a building in CityGML), but usually practitioners do it with either *gml:Solid* or *gml:MultiSurface*. See the same simple volumetric objects, first modelled with a *gml:Solid* and then with *gml:MultiSurface*:

<script src="https://gist.github.com/hugoledoux/10551725.js"></script>

<script src="https://gist.github.com/hugoledoux/10551979.js"></script>

Our validator only checks the former. The reason is simple: if an object is modelled with *gml:MultiSurface* and the set of surfaces is not watertight, then it would be wrong to report that the object is not valid... However, if a building is watertight, then in our opinion it is good practice to model it with *gml:Solid*.

---

### The server says my file is too big, what's the maximum?

50MB. If you need more, [get in touch](/contact) or download the [code](https://github.com/tudelft-gist/val3dity), compile it and run val3dity locally.





## FAQ

### What do you do with my uploaded file?

We delete it right after having validated it, we promise. The report is however available to everyone (if they know its ID).

---

### I don't understand the report I get.

<script src="https://gist.github.com/hugoledoux/11082609.js"></script>

The report lists only the solids that are *not* valid, and gives one or more [errors](/errors) for each. If your solids have *gml:id* then these are used to report the errors, if not then the number means the order of the solids in the file (the first one being 0). If a surface is reported invalid, then the id of the surface is also based on the order of the surfaces in one *gml:Shell*. For instance, in the example above the face 8th surface listed in the first shell of the 26th solid is not planar. 

---

### I'm sure that my solid is okay, I've double-checked, and yet the validator says that something is wrong.

It's possible that there are bugs in [val3dity](https://github.com/tudelft-gist/val3dity). Please [report the issue](https://github.com/tudelft-gist/val3dity/issues).

---

### The validation report says that there is no solids in my file, but I can see the buildings with my viewer!

There are many (or more precisely: [too many](http://erouault.blogspot.nl/2014/04/gml-madness.html)) ways to model a volume/polyhedron in GML (eg a building in CityGML), but usually practitioners do it with either *gml:Solid* or *gml:MultiSurface*. See the same simple volumetric objects, first modelled with a *gml:Solid* and then with *gml:MultiSurface*:

<script src="https://gist.github.com/hugoledoux/10551725.js"></script>

<script src="https://gist.github.com/hugoledoux/10551979.js"></script>

Our validator only checks the former. The reason is simple: if an object is modelled with *gml:MultiSurface* and the set of surfaces is not watertight, then it would be wrong to report that the object is not valid... However, if a building is watertight, then in our opinion it is good practice to model it with *gml:Solid*.





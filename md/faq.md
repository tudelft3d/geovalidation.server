
## faq


### what do you do with my uploaded file?

We delete it right after having validated it. We promise. The report is however available to everyone.

---

### I'm sure that my solid is okay, I've triple-checked, and yet the validator says that something is wrong.

It's possible that there are bugs in [val3dity](https://github.com/tudelft-gist/val3dity). Please [contact us](/contact) and report the issue.

---

### the validation report says that there is no solids in my file, but I can see the buildings with my viewer!

There are many (too many?) ways to model a volume/polyhedron in GML (eg a building in CityGML), but usually practitioners do it with either *gml:Solid* or *gml:MultiSurface*. See the same simple volumetric objects, first modelled with a *gml:Solid* and then with *gml:MultiSurface*:

<script src="https://gist.github.com/hugoledoux/10551725.js"></script>

<script src="https://gist.github.com/hugoledoux/10551979.js"></script>

The validator only checks the former. The reason is simple: if an object is modelled with *gml:MultiSurface* and the set of surfaces is not watertight, then it would be wrong to report that the object is not valid... However, if a building is watertight, then in our opinion it is good practice to model it with *gml:Solid*.





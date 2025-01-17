# This code is derived from the SOM benchmarks, see AUTHORS.md file.
# This benchmark is based on the minimal-json Java library maintained at:
# https://github.com/ralfstx/minimal-json
#
# Copyright (c) 2015-2021 Stefan Marr <gitself._stefan-marr.de>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the 'Software'), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


def vector_with(elem):
    v = Vector(1)
    v.append(elem)
    return v


# Porting notes:
#  - does not use an explicit array bounds check, because Java already does
#    that. Don't see a point in doing it twice.
class Vector:
    def __init__(self, size=50):
        self._storage = [None] * size
        self._first_idx = 0
        self._last_idx = 0

    def at(self, idx):
        if idx >= len(self._storage):
            return None
        return self._storage[idx]

    def at_put(self, idx, val):
        if idx >= len(self._storage):
            new_length = len(self._storage)
            while new_length <= idx:
                new_length *= 2

            new_storage = [None] * new_length
            for i in range(len(self._storage)):
                new_storage[i] = self._storage[i]
            self._storage = new_storage

        self._storage[idx] = val
        if self._last_idx < idx + 1:
            self._last_idx = idx + 1

    def append(self, elem):
        if self._last_idx >= len(self._storage):
            # Need to expand capacity first
            new_storage = [None] * (2 * len(self._storage))
            for i in range(len(self._storage)):
                new_storage[i] = self._storage[i]
            self._storage = new_storage

        self._storage[self._last_idx] = elem
        self._last_idx += 1

    def is_empty(self):
        return self._last_idx == self._first_idx

    def for_each(self, fn):
        for i in range(self._first_idx, self._last_idx):
            fn(self._storage[i])

    def has_some(self, fn):
        for i in range(self._first_idx, self._last_idx):
            if fn(self._storage[i]):
                return True
        return False

    def get_one(self, fn):
        for i in range(self._first_idx, self._last_idx):
            e = self._storage[i]
            if fn(e):
                return e
        return None

    def first(self):
        if self.is_empty():
            return None
        return self._storage[self._first_idx]

    def remove_first(self):
        if self.is_empty():
            return None
        self._first_idx += 1
        return self._storage[self._first_idx - 1]

    def remove(self, obj):
        new_array = [None] * self.capacity()
        new_last = 0
        found = False

        def each(it):
            nonlocal new_last
            nonlocal found
            if it is obj:
                found = True
            else:
                new_array[new_last] = it
                new_last += 1

        self.for_each(each)

        self._storage = new_array
        self._last_idx = new_last
        self._first_idx = 0
        return found

    def remove_all(self):
        self._first_idx = 0
        self._last_idx = 0
        self._storage = [None] * len(self._storage)

    def size(self):
        return self._last_idx - self._first_idx

    def capacity(self):
        return len(self._storage)

    def sort(self, comparator):
        if self.size() > 0:
            self._sort(self._first_idx, self._last_idx - 1, comparator)

    def _sort(self, i, j, c):
        if c is None:
            self._default_sort(i, j)

        n = j + 1 - i
        if n <= 1:
            return

        di = self._storage[i]
        dj = self._storage[j]

        if c.compare(di, dj) > 0:
            self._swap(self._storage, i, j)
            di, dj = dj, di

        if n > 2:
            ij = (i + j) // 2
            dij = self._storage[ij]

        if c.compare(di, dij) <= 0:
            if c.compare(dij, dj) > 0:
                self._swap(self._storage, j, ij)
                dij = dj
        else:
            self._swap(self._storage, i, ij)
            dij = di

        if n > 3:
            k = i
            l = j - 1

            while True:
                while k <= l and c.compare(dij, self._storage[l]) <= 0:
                    l -= 1

                k += 1
                while k <= l and c.compare(self._storage[k], dij) <= 0:
                    k += 1

                if k > l:
                    break

                self._swap(self._storage, k, l)

            self._sort(i, l, c)
            self._sort(k, j, c)

    def _swap(self, storage, i, j):
        raise NotImplementedError()

    def _default_sort(self, i, j):
        raise NotImplementedError()


_RAP_BENCHMARK_MINIFIED = '{"head":{"requestCounter":4},"operations":[["destroy","w54"],["set","w2",{"activeControl":"w99"}],["set","w21",{"customVariant":"variant_navigation"}],["set","w28",{"customVariant":"variant_selected"}],["set","w53",{"children":["w95"]}],["create","w95","rwt.widgets.Composite",{"parent":"w53","style":["NONE"],"bounds":[0,0,1008,586],"children":["w96","w97"],"tabIndex":-1,"clientArea":[0,0,1008,586]}],["create","w96","rwt.widgets.Label",{"parent":"w95","style":["NONE"],"bounds":[10,30,112,26],"tabIndex":-1,"customVariant":"variant_pageHeadline","text":"TableViewer"}],["create","w97","rwt.widgets.Composite",{"parent":"w95","style":["NONE"],"bounds":[0,61,1008,525],"children":["w98","w99","w226","w228"],"tabIndex":-1,"clientArea":[0,0,1008,525]}],["create","w98","rwt.widgets.Text",{"parent":"w97","style":["LEFT","SINGLE","BORDER"],"bounds":[10,10,988,32],"tabIndex":22,"activeKeys":["#13","#27","#40"]}],["listen","w98",{"KeyDown":true,"Modify":true}],["create","w99","rwt.widgets.Grid",{"parent":"w97","style":["SINGLE","BORDER"],"appearance":"table","indentionWidth":0,"treeColumn":-1,"markupEnabled":false}],["create","w100","rwt.widgets.ScrollBar",{"parent":"w99","style":["HORIZONTAL"]}],["create","w101","rwt.widgets.ScrollBar",{"parent":"w99","style":["VERTICAL"]}],["set","w99",{"bounds":[10,52,988,402],"children":[],"tabIndex":23,"activeKeys":["CTRL+#70","CTRL+#78","CTRL+#82","CTRL+#89","CTRL+#83","CTRL+#71","CTRL+#69"],"cancelKeys":["CTRL+#70","CTRL+#78","CTRL+#82","CTRL+#89","CTRL+#83","CTRL+#71","CTRL+#69"]}],["listen","w99",{"MouseDown":true,"MouseUp":true,"MouseDoubleClick":true,"KeyDown":true}],["set","w99",{"itemCount":118,"itemHeight":28,"itemMetrics":[[0,0,50,3,0,3,44],[1,50,50,53,0,53,44],[2,100,140,103,0,103,134],[3,240,180,243,0,243,174],[4,420,50,423,0,423,44],[5,470,50,473,0,473,44]],"columnCount":6,"headerHeight":35,"headerVisible":true,"linesVisible":true,"focusItem":"w108","selection":["w108"]}],["listen","w99",{"Selection":true,"DefaultSelection":true}],["set","w99",{"enableCellToolTip":true}],["listen","w100",{"Selection":true}],["set","w101",{"visibility":true}],["listen","w101",{"Selection":true}],["create","w102","rwt.widgets.GridColumn",{"parent":"w99","text":"Nr.","width":50,"moveable":true}],["listen","w102",{"Selection":true}],["create","w103","rwt.widgets.GridColumn",{"parent":"w99","text":"Sym.","index":1,"left":50,"width":50,"moveable":true}],["listen","w103",{"Selection":true}],["create","w104","rwt.widgets.GridColumn",{"parent":"w99","text":"Name","index":2,"left":100,"width":140,"moveable":true}],["listen","w104",{"Selection":true}],["create","w105","rwt.widgets.GridColumn",{"parent":"w99","text":"Series","index":3,"left":240,"width":180,"moveable":true}],["listen","w105",{"Selection":true}],["create","w106","rwt.widgets.GridColumn",{"parent":"w99","text":"Group","index":4,"left":420,"width":50,"moveable":true}],["listen","w106",{"Selection":true}],["create","w107","rwt.widgets.GridColumn",{"parent":"w99","text":"Period","index":5,"left":470,"width":50,"moveable":true}],["listen","w107",{"Selection":true}],["create","w108","rwt.widgets.GridItem",{"parent":"w99","index":0,"texts":["1","H","Hydrogen","Nonmetal","1","1"],"cellBackgrounds":[null,null,null,[138,226,52,255],null,null]}],["create","w109","rwt.widgets.GridItem",{"parent":"w99","index":1,"texts":["2","He","Helium","Noble gas","18","1"],"cellBackgrounds":[null,null,null,[114,159,207,255],null,null]}],["create","w110","rwt.widgets.GridItem",{"parent":"w99","index":2,"texts":["3","Li","Lithium","Alkali metal","1","2"],"cellBackgrounds":[null,null,null,[239,41,41,255],null,null]}],["create","w111","rwt.widgets.GridItem",{"parent":"w99","index":3,"texts":["4","Be","Beryllium","Alkaline earth metal","2","2"],"cellBackgrounds":[null,null,null,[233,185,110,255],null,null]}],["create","w112","rwt.widgets.GridItem",{"parent":"w99","index":4,"texts":["5","B","Boron","Metalloid","13","2"],"cellBackgrounds":[null,null,null,[156,159,153,255],null,null]}],["create","w113","rwt.widgets.GridItem",{"parent":"w99","index":5,"texts":["6","C","Carbon","Nonmetal","14","2"],"cellBackgrounds":[null,null,null,[138,226,52,255],null,null]}],["create","w114","rwt.widgets.GridItem",{"parent":"w99","index":6,"texts":["7","N","Nitrogen","Nonmetal","15","2"],"cellBackgrounds":[null,null,null,[138,226,52,255],null,null]}],["create","w115","rwt.widgets.GridItem",{"parent":"w99","index":7,"texts":["8","O","Oxygen","Nonmetal","16","2"],"cellBackgrounds":[null,null,null,[138,226,52,255],null,null]}],["create","w116","rwt.widgets.GridItem",{"parent":"w99","index":8,"texts":["9","F","Fluorine","Halogen","17","2"],"cellBackgrounds":[null,null,null,[252,233,79,255],null,null]}],["create","w117","rwt.widgets.GridItem",{"parent":"w99","index":9,"texts":["10","Ne","Neon","Noble gas","18","2"],"cellBackgrounds":[null,null,null,[114,159,207,255],null,null]}],["create","w118","rwt.widgets.GridItem",{"parent":"w99","index":10,"texts":["11","Na","Sodium","Alkali metal","1","3"],"cellBackgrounds":[null,null,null,[239,41,41,255],null,null]}],["create","w119","rwt.widgets.GridItem",{"parent":"w99","index":11,"texts":["12","Mg","Magnesium","Alkaline earth metal","2","3"],"cellBackgrounds":[null,null,null,[233,185,110,255],null,null]}],["create","w120","rwt.widgets.GridItem",{"parent":"w99","index":12,"texts":["13","Al","Aluminium","Poor metal","13","3"],"cellBackgrounds":[null,null,null,[238,238,236,255],null,null]}],["create","w121","rwt.widgets.GridItem",{"parent":"w99","index":13,"texts":["14","Si","Silicon","Metalloid","14","3"],"cellBackgrounds":[null,null,null,[156,159,153,255],null,null]}],["create","w122","rwt.widgets.GridItem",{"parent":"w99","index":14,"texts":["15","P","Phosphorus","Nonmetal","15","3"],"cellBackgrounds":[null,null,null,[138,226,52,255],null,null]}],["create","w123","rwt.widgets.GridItem",{"parent":"w99","index":15,"texts":["16","S","Sulfur","Nonmetal","16","3"],"cellBackgrounds":[null,null,null,[138,226,52,255],null,null]}],["create","w124","rwt.widgets.GridItem",{"parent":"w99","index":16,"texts":["17","Cl","Chlorine","Halogen","17","3"],"cellBackgrounds":[null,null,null,[252,233,79,255],null,null]}],["create","w125","rwt.widgets.GridItem",{"parent":"w99","index":17,"texts":["18","Ar","Argon","Noble gas","18","3"],"cellBackgrounds":[null,null,null,[114,159,207,255],null,null]}],["create","w126","rwt.widgets.GridItem",{"parent":"w99","index":18,"texts":["19","K","Potassium","Alkali metal","1","4"],"cellBackgrounds":[null,null,null,[239,41,41,255],null,null]}],["create","w127","rwt.widgets.GridItem",{"parent":"w99","index":19,"texts":["20","Ca","Calcium","Alkaline earth metal","2","4"],"cellBackgrounds":[null,null,null,[233,185,110,255],null,null]}],["create","w128","rwt.widgets.GridItem",{"parent":"w99","index":20,"texts":["21","Sc","Scandium","Transition metal","3","4"],"cellBackgrounds":[null,null,null,[252,175,62,255],null,null]}],["create","w129","rwt.widgets.GridItem",{"parent":"w99","index":21,"texts":["22","Ti","Titanium","Transition metal","4","4"],"cellBackgrounds":[null,null,null,[252,175,62,255],null,null]}],["create","w130","rwt.widgets.GridItem",{"parent":"w99","index":22,"texts":["23","V","Vanadium","Transition metal","5","4"],"cellBackgrounds":[null,null,null,[252,175,62,255],null,null]}],["create","w131","rwt.widgets.GridItem",{"parent":"w99","index":23,"texts":["24","Cr","Chromium","Transition metal","6","4"],"cellBackgrounds":[null,null,null,[252,175,62,255],null,null]}],["create","w132","rwt.widgets.GridItem",{"parent":"w99","index":24,"texts":["25","Mn","Manganese","Transition metal","7","4"],"cellBackgrounds":[null,null,null,[252,175,62,255],null,null]}],["create","w133","rwt.widgets.GridItem",{"parent":"w99","index":25,"texts":["26","Fe","Iron","Transition metal","8","4"],"cellBackgrounds":[null,null,null,[252,175,62,255],null,null]}],["create","w134","rwt.widgets.GridItem",{"parent":"w99","index":26,"texts":["27","Co","Cobalt","Transition metal","9","4"],"cellBackgrounds":[null,null,null,[252,175,62,255],null,null]}],["create","w135","rwt.widgets.GridItem",{"parent":"w99","index":27,"texts":["28","Ni","Nickel","Transition metal","10","4"],"cellBackgrounds":[null,null,null,[252,175,62,255],null,null]}],["create","w136","rwt.widgets.GridItem",{"parent":"w99","index":28,"texts":["29","Cu","Copper","Transition metal","11","4"],"cellBackgrounds":[null,null,null,[252,175,62,255],null,null]}],["create","w137","rwt.widgets.GridItem",{"parent":"w99","index":29,"texts":["30","Zn","Zinc","Transition metal","12","4"],"cellBackgrounds":[null,null,null,[252,175,62,255],null,null]}],["create","w138","rwt.widgets.GridItem",{"parent":"w99","index":30,"texts":["31","Ga","Gallium","Poor metal","13","4"],"cellBackgrounds":[null,null,null,[238,238,236,255],null,null]}],["create","w139","rwt.widgets.GridItem",{"parent":"w99","index":31,"texts":["32","Ge","Germanium","Metalloid","14","4"],"cellBackgrounds":[null,null,null,[156,159,153,255],null,null]}],["create","w140","rwt.widgets.GridItem",{"parent":"w99","index":32,"texts":["33","As","Arsenic","Metalloid","15","4"],"cellBackgrounds":[null,null,null,[156,159,153,255],null,null]}],["create","w141","rwt.widgets.GridItem",{"parent":"w99","index":33,"texts":["34","Se","Selenium","Nonmetal","16","4"],"cellBackgrounds":[null,null,null,[138,226,52,255],null,null]}],["create","w142","rwt.widgets.GridItem",{"parent":"w99","index":34,"texts":["35","Br","Bromine","Halogen","17","4"],"cellBackgrounds":[null,null,null,[252,233,79,255],null,null]}],["create","w143","rwt.widgets.GridItem",{"parent":"w99","index":35,"texts":["36","Kr","Krypton","Noble gas","18","4"],"cellBackgrounds":[null,null,null,[114,159,207,255],null,null]}],["create","w144","rwt.widgets.GridItem",{"parent":"w99","index":36,"texts":["37","Rb","Rubidium","Alkali metal","1","5"],"cellBackgrounds":[null,null,null,[239,41,41,255],null,null]}],["create","w145","rwt.widgets.GridItem",{"parent":"w99","index":37,"texts":["38","Sr","Strontium","Alkaline earth metal","2","5"],"cellBackgrounds":[null,null,null,[233,185,110,255],null,null]}],["create","w146","rwt.widgets.GridItem",{"parent":"w99","index":38,"texts":["39","Y","Yttrium","Transition metal","3","5"],"cellBackgrounds":[null,null,null,[252,175,62,255],null,null]}],["create","w147","rwt.widgets.GridItem",{"parent":"w99","index":39,"texts":["40","Zr","Zirconium","Transition metal","4","5"],"cellBackgrounds":[null,null,null,[252,175,62,255],null,null]}],["create","w148","rwt.widgets.GridItem",{"parent":"w99","index":40,"texts":["41","Nb","Niobium","Transition metal","5","5"],"cellBackgrounds":[null,null,null,[252,175,62,255],null,null]}],["create","w149","rwt.widgets.GridItem",{"parent":"w99","index":41,"texts":["42","Mo","Molybdenum","Transition metal","6","5"],"cellBackgrounds":[null,null,null,[252,175,62,255],null,null]}],["create","w150","rwt.widgets.GridItem",{"parent":"w99","index":42,"texts":["43","Tc","Technetium","Transition metal","7","5"],"cellBackgrounds":[null,null,null,[252,175,62,255],null,null]}],["create","w151","rwt.widgets.GridItem",{"parent":"w99","index":43,"texts":["44","Ru","Ruthenium","Transition metal","8","5"],"cellBackgrounds":[null,null,null,[252,175,62,255],null,null]}],["create","w152","rwt.widgets.GridItem",{"parent":"w99","index":44,"texts":["45","Rh","Rhodium","Transition metal","9","5"],"cellBackgrounds":[null,null,null,[252,175,62,255],null,null]}],["create","w153","rwt.widgets.GridItem",{"parent":"w99","index":45,"texts":["46","Pd","Palladium","Transition metal","10","5"],"cellBackgrounds":[null,null,null,[252,175,62,255],null,null]}],["create","w154","rwt.widgets.GridItem",{"parent":"w99","index":46,"texts":["47","Ag","Silver","Transition metal","11","5"],"cellBackgrounds":[null,null,null,[252,175,62,255],null,null]}],["create","w155","rwt.widgets.GridItem",{"parent":"w99","index":47,"texts":["48","Cd","Cadmium","Transition metal","12","5"],"cellBackgrounds":[null,null,null,[252,175,62,255],null,null]}],["create","w156","rwt.widgets.GridItem",{"parent":"w99","index":48,"texts":["49","In","Indium","Poor metal","13","5"],"cellBackgrounds":[null,null,null,[238,238,236,255],null,null]}],["create","w157","rwt.widgets.GridItem",{"parent":"w99","index":49,"texts":["50","Sn","Tin","Poor metal","14","5"],"cellBackgrounds":[null,null,null,[238,238,236,255],null,null]}],["create","w158","rwt.widgets.GridItem",{"parent":"w99","index":50,"texts":["51","Sb","Antimony","Metalloid","15","5"],"cellBackgrounds":[null,null,null,[156,159,153,255],null,null]}],["create","w159","rwt.widgets.GridItem",{"parent":"w99","index":51,"texts":["52","Te","Tellurium","Metalloid","16","5"],"cellBackgrounds":[null,null,null,[156,159,153,255],null,null]}],["create","w160","rwt.widgets.GridItem",{"parent":"w99","index":52,"texts":["53","I","Iodine","Halogen","17","5"],"cellBackgrounds":[null,null,null,[252,233,79,255],null,null]}],["create","w161","rwt.widgets.GridItem",{"parent":"w99","index":53,"texts":["54","Xe","Xenon","Noble gas","18","5"],"cellBackgrounds":[null,null,null,[114,159,207,255],null,null]}],["create","w162","rwt.widgets.GridItem",{"parent":"w99","index":54,"texts":["55","Cs","Caesium","Alkali metal","1","6"],"cellBackgrounds":[null,null,null,[239,41,41,255],null,null]}],["create","w163","rwt.widgets.GridItem",{"parent":"w99","index":55,"texts":["56","Ba","Barium","Alkaline earth metal","2","6"],"cellBackgrounds":[null,null,null,[233,185,110,255],null,null]}],["create","w164","rwt.widgets.GridItem",{"parent":"w99","index":56,"texts":["57","La","Lanthanum","Lanthanide","3","6"],"cellBackgrounds":[null,null,null,[173,127,168,255],null,null]}],["create","w165","rwt.widgets.GridItem",{"parent":"w99","index":57,"texts":["58","Ce","Cerium","Lanthanide","3","6"],"cellBackgrounds":[null,null,null,[173,127,168,255],null,null]}],["create","w166","rwt.widgets.GridItem",{"parent":"w99","index":58,"texts":["59","Pr","Praseodymium","Lanthanide","3","6"],"cellBackgrounds":[null,null,null,[173,127,168,255],null,null]}],["create","w167","rwt.widgets.GridItem",{"parent":"w99","index":59,"texts":["60","Nd","Neodymium","Lanthanide","3","6"],"cellBackgrounds":[null,null,null,[173,127,168,255],null,null]}],["create","w168","rwt.widgets.GridItem",{"parent":"w99","index":60,"texts":["61","Pm","Promethium","Lanthanide","3","6"],"cellBackgrounds":[null,null,null,[173,127,168,255],null,null]}],["create","w169","rwt.widgets.GridItem",{"parent":"w99","index":61,"texts":["62","Sm","Samarium","Lanthanide","3","6"],"cellBackgrounds":[null,null,null,[173,127,168,255],null,null]}],["create","w170","rwt.widgets.GridItem",{"parent":"w99","index":62,"texts":["63","Eu","Europium","Lanthanide","3","6"],"cellBackgrounds":[null,null,null,[173,127,168,255],null,null]}],["create","w171","rwt.widgets.GridItem",{"parent":"w99","index":63,"texts":["64","Gd","Gadolinium","Lanthanide","3","6"],"cellBackgrounds":[null,null,null,[173,127,168,255],null,null]}],["create","w172","rwt.widgets.GridItem",{"parent":"w99","index":64,"texts":["65","Tb","Terbium","Lanthanide","3","6"],"cellBackgrounds":[null,null,null,[173,127,168,255],null,null]}],["create","w173","rwt.widgets.GridItem",{"parent":"w99","index":65,"texts":["66","Dy","Dysprosium","Lanthanide","3","6"],"cellBackgrounds":[null,null,null,[173,127,168,255],null,null]}],["create","w174","rwt.widgets.GridItem",{"parent":"w99","index":66,"texts":["67","Ho","Holmium","Lanthanide","3","6"],"cellBackgrounds":[null,null,null,[173,127,168,255],null,null]}],["create","w175","rwt.widgets.GridItem",{"parent":"w99","index":67,"texts":["68","Er","Erbium","Lanthanide","3","6"],"cellBackgrounds":[null,null,null,[173,127,168,255],null,null]}],["create","w176","rwt.widgets.GridItem",{"parent":"w99","index":68,"texts":["69","Tm","Thulium","Lanthanide","3","6"],"cellBackgrounds":[null,null,null,[173,127,168,255],null,null]}],["create","w177","rwt.widgets.GridItem",{"parent":"w99","index":69,"texts":["70","Yb","Ytterbium","Lanthanide","3","6"],"cellBackgrounds":[null,null,null,[173,127,168,255],null,null]}],["create","w178","rwt.widgets.GridItem",{"parent":"w99","index":70,"texts":["71","Lu","Lutetium","Lanthanide","3","6"],"cellBackgrounds":[null,null,null,[173,127,168,255],null,null]}],["create","w179","rwt.widgets.GridItem",{"parent":"w99","index":71,"texts":["72","Hf","Hafnium","Transition metal","4","6"],"cellBackgrounds":[null,null,null,[252,175,62,255],null,null]}],["create","w180","rwt.widgets.GridItem",{"parent":"w99","index":72,"texts":["73","Ta","Tantalum","Transition metal","5","6"],"cellBackgrounds":[null,null,null,[252,175,62,255],null,null]}],["create","w181","rwt.widgets.GridItem",{"parent":"w99","index":73,"texts":["74","W","Tungsten","Transition metal","6","6"],"cellBackgrounds":[null,null,null,[252,175,62,255],null,null]}],["create","w182","rwt.widgets.GridItem",{"parent":"w99","index":74,"texts":["75","Re","Rhenium","Transition metal","7","6"],"cellBackgrounds":[null,null,null,[252,175,62,255],null,null]}],["create","w183","rwt.widgets.GridItem",{"parent":"w99","index":75,"texts":["76","Os","Osmium","Transition metal","8","6"],"cellBackgrounds":[null,null,null,[252,175,62,255],null,null]}],["create","w184","rwt.widgets.GridItem",{"parent":"w99","index":76,"texts":["77","Ir","Iridium","Transition metal","9","6"],"cellBackgrounds":[null,null,null,[252,175,62,255],null,null]}],["create","w185","rwt.widgets.GridItem",{"parent":"w99","index":77,"texts":["78","Pt","Platinum","Transition metal","10","6"],"cellBackgrounds":[null,null,null,[252,175,62,255],null,null]}],["create","w186","rwt.widgets.GridItem",{"parent":"w99","index":78,"texts":["79","Au","Gold","Transition metal","11","6"],"cellBackgrounds":[null,null,null,[252,175,62,255],null,null]}],["create","w187","rwt.widgets.GridItem",{"parent":"w99","index":79,"texts":["80","Hg","Mercury","Transition metal","12","6"],"cellBackgrounds":[null,null,null,[252,175,62,255],null,null]}],["create","w188","rwt.widgets.GridItem",{"parent":"w99","index":80,"texts":["81","Tl","Thallium","Poor metal","13","6"],"cellBackgrounds":[null,null,null,[238,238,236,255],null,null]}],["create","w189","rwt.widgets.GridItem",{"parent":"w99","index":81,"texts":["82","Pb","Lead","Poor metal","14","6"],"cellBackgrounds":[null,null,null,[238,238,236,255],null,null]}],["create","w190","rwt.widgets.GridItem",{"parent":"w99","index":82,"texts":["83","Bi","Bismuth","Poor metal","15","6"],"cellBackgrounds":[null,null,null,[238,238,236,255],null,null]}],["create","w191","rwt.widgets.GridItem",{"parent":"w99","index":83,"texts":["84","Po","Polonium","Metalloid","16","6"],"cellBackgrounds":[null,null,null,[156,159,153,255],null,null]}],["create","w192","rwt.widgets.GridItem",{"parent":"w99","index":84,"texts":["85","At","Astatine","Halogen","17","6"],"cellBackgrounds":[null,null,null,[252,233,79,255],null,null]}],["create","w193","rwt.widgets.GridItem",{"parent":"w99","index":85,"texts":["86","Rn","Radon","Noble gas","18","6"],"cellBackgrounds":[null,null,null,[114,159,207,255],null,null]}],["create","w194","rwt.widgets.GridItem",{"parent":"w99","index":86,"texts":["87","Fr","Francium","Alkali metal","1","7"],"cellBackgrounds":[null,null,null,[239,41,41,255],null,null]}],["create","w195","rwt.widgets.GridItem",{"parent":"w99","index":87,"texts":["88","Ra","Radium","Alkaline earth metal","2","7"],"cellBackgrounds":[null,null,null,[233,185,110,255],null,null]}],["create","w196","rwt.widgets.GridItem",{"parent":"w99","index":88,"texts":["89","Ac","Actinium","Actinide","3","7"],"cellBackgrounds":[null,null,null,[173,127,168,255],null,null]}],["create","w197","rwt.widgets.GridItem",{"parent":"w99","index":89,"texts":["90","Th","Thorium","Actinide","3","7"],"cellBackgrounds":[null,null,null,[173,127,168,255],null,null]}],["create","w198","rwt.widgets.GridItem",{"parent":"w99","index":90,"texts":["91","Pa","Protactinium","Actinide","3","7"],"cellBackgrounds":[null,null,null,[173,127,168,255],null,null]}],["create","w199","rwt.widgets.GridItem",{"parent":"w99","index":91,"texts":["92","U","Uranium","Actinide","3","7"],"cellBackgrounds":[null,null,null,[173,127,168,255],null,null]}],["create","w200","rwt.widgets.GridItem",{"parent":"w99","index":92,"texts":["93","Np","Neptunium","Actinide","3","7"],"cellBackgrounds":[null,null,null,[173,127,168,255],null,null]}],["create","w201","rwt.widgets.GridItem",{"parent":"w99","index":93,"texts":["94","Pu","Plutonium","Actinide","3","7"],"cellBackgrounds":[null,null,null,[173,127,168,255],null,null]}],["create","w202","rwt.widgets.GridItem",{"parent":"w99","index":94,"texts":["95","Am","Americium","Actinide","3","7"],"cellBackgrounds":[null,null,null,[173,127,168,255],null,null]}],["create","w203","rwt.widgets.GridItem",{"parent":"w99","index":95,"texts":["96","Cm","Curium","Actinide","3","7"],"cellBackgrounds":[null,null,null,[173,127,168,255],null,null]}],["create","w204","rwt.widgets.GridItem",{"parent":"w99","index":96,"texts":["97","Bk","Berkelium","Actinide","3","7"],"cellBackgrounds":[null,null,null,[173,127,168,255],null,null]}],["create","w205","rwt.widgets.GridItem",{"parent":"w99","index":97,"texts":["98","Cf","Californium","Actinide","3","7"],"cellBackgrounds":[null,null,null,[173,127,168,255],null,null]}],["create","w206","rwt.widgets.GridItem",{"parent":"w99","index":98,"texts":["99","Es","Einsteinium","Actinide","3","7"],"cellBackgrounds":[null,null,null,[173,127,168,255],null,null]}],["create","w207","rwt.widgets.GridItem",{"parent":"w99","index":99,"texts":["100","Fm","Fermium","Actinide","3","7"],"cellBackgrounds":[null,null,null,[173,127,168,255],null,null]}],["create","w208","rwt.widgets.GridItem",{"parent":"w99","index":100,"texts":["101","Md","Mendelevium","Actinide","3","7"],"cellBackgrounds":[null,null,null,[173,127,168,255],null,null]}],["create","w209","rwt.widgets.GridItem",{"parent":"w99","index":101,"texts":["102","No","Nobelium","Actinide","3","7"],"cellBackgrounds":[null,null,null,[173,127,168,255],null,null]}],["create","w210","rwt.widgets.GridItem",{"parent":"w99","index":102,"texts":["103","Lr","Lawrencium","Actinide","3","7"],"cellBackgrounds":[null,null,null,[173,127,168,255],null,null]}],["create","w211","rwt.widgets.GridItem",{"parent":"w99","index":103,"texts":["104","Rf","Rutherfordium","Transition metal","4","7"],"cellBackgrounds":[null,null,null,[252,175,62,255],null,null]}],["create","w212","rwt.widgets.GridItem",{"parent":"w99","index":104,"texts":["105","Db","Dubnium","Transition metal","5","7"],"cellBackgrounds":[null,null,null,[252,175,62,255],null,null]}],["create","w213","rwt.widgets.GridItem",{"parent":"w99","index":105,"texts":["106","Sg","Seaborgium","Transition metal","6","7"],"cellBackgrounds":[null,null,null,[252,175,62,255],null,null]}],["create","w214","rwt.widgets.GridItem",{"parent":"w99","index":106,"texts":["107","Bh","Bohrium","Transition metal","7","7"],"cellBackgrounds":[null,null,null,[252,175,62,255],null,null]}],["create","w215","rwt.widgets.GridItem",{"parent":"w99","index":107,"texts":["108","Hs","Hassium","Transition metal","8","7"],"cellBackgrounds":[null,null,null,[252,175,62,255],null,null]}],["create","w216","rwt.widgets.GridItem",{"parent":"w99","index":108,"texts":["109","Mt","Meitnerium","Transition metal","9","7"],"cellBackgrounds":[null,null,null,[252,175,62,255],null,null]}],["create","w217","rwt.widgets.GridItem",{"parent":"w99","index":109,"texts":["110","Ds","Darmstadtium","Transition metal","10","7"],"cellBackgrounds":[null,null,null,[252,175,62,255],null,null]}],["create","w218","rwt.widgets.GridItem",{"parent":"w99","index":110,"texts":["111","Rg","Roentgenium","Transition metal","11","7"],"cellBackgrounds":[null,null,null,[252,175,62,255],null,null]}],["create","w219","rwt.widgets.GridItem",{"parent":"w99","index":111,"texts":["112","Uub","Ununbium","Transition metal","12","7"],"cellBackgrounds":[null,null,null,[252,175,62,255],null,null]}],["create","w220","rwt.widgets.GridItem",{"parent":"w99","index":112,"texts":["113","Uut","Ununtrium","Poor metal","13","7"],"cellBackgrounds":[null,null,null,[238,238,236,255],null,null]}],["create","w221","rwt.widgets.GridItem",{"parent":"w99","index":113,"texts":["114","Uuq","Ununquadium","Poor metal","14","7"],"cellBackgrounds":[null,null,null,[238,238,236,255],null,null]}],["create","w222","rwt.widgets.GridItem",{"parent":"w99","index":114,"texts":["115","Uup","Ununpentium","Poor metal","15","7"],"cellBackgrounds":[null,null,null,[238,238,236,255],null,null]}],["create","w223","rwt.widgets.GridItem",{"parent":"w99","index":115,"texts":["116","Uuh","Ununhexium","Poor metal","16","7"],"cellBackgrounds":[null,null,null,[238,238,236,255],null,null]}],["create","w224","rwt.widgets.GridItem",{"parent":"w99","index":116,"texts":["117","Uus","Ununseptium","Halogen","17","7"],"cellBackgrounds":[null,null,null,[252,233,79,255],null,null]}],["create","w225","rwt.widgets.GridItem",{"parent":"w99","index":117,"texts":["118","Uuo","Ununoctium","Noble gas","18","7"],"cellBackgrounds":[null,null,null,[114,159,207,255],null,null]}],["create","w226","rwt.widgets.Composite",{"parent":"w97","style":["BORDER"],"bounds":[10,464,988,25],"children":["w227"],"tabIndex":-1,"clientArea":[0,0,986,23]}],["create","w227","rwt.widgets.Label",{"parent":"w226","style":["NONE"],"bounds":[10,10,966,3],"tabIndex":-1,"text":"Hydrogen (H)"}],["create","w228","rwt.widgets.Label",{"parent":"w97","style":["WRAP"],"bounds":[10,499,988,16],"tabIndex":-1,"foreground":[150,150,150,255],"font":[["Verdana","Lucida Sans","Arial","Helvetica","sans-serif"],10,false,false],"text":"Shortcuts: [CTRL+F] - Filter | Sort by: [CTRL+R] - Number, [CTRL+Y] - Symbol, [CTRL+N] - Name, [CTRL+S] - Series, [CTRL+G] - Group, [CTRL+E] - Period"}],["set","w1",{"focusControl":"w99"}],["call","rwt.client.BrowserNavigation","addToHistory",{"entries":[["tableviewer","TableViewer"]]}]]}'  # pylint: disable=line-too-long


class Json():
    def benchmark(self):
        return _Parser(_RAP_BENCHMARK_MINIFIED).parse()
    
    def inner_benchmark_loop(self, inner_iterations):
        for _ in range(inner_iterations):
            if not self.verify_result(self.benchmark()):
                return False
        return True

    def verify_result(self, result):
        if not result.is_object():
            return False
        if not result.as_object().get("head").is_object():
            return False
        if not result.as_object().get("operations").is_array():
            return False

        return result.as_object().get("operations").as_array().size() == 156


class _JsonValue:
    def is_object(self):
        return False

    def is_array(self):
        return False

    def is_number(self):
        return False

    def is_string(self):
        return False

    def is_boolean(self):
        return False

    def is_true(self):
        return False

    def is_false(self):
        return False

    def is_null(self):
        return False

    def as_object(self):
        raise Exception("Unsupported operation, not an object: " + str(self))

    def as_array(self):
        raise Exception("Unsupported operation, not an array: " + str(self))


class _JsonLiteral(_JsonValue):
    def __init__(self, value):
        self._value = value
        self._is_null = "null" == value
        self._is_true = "true" == value
        self._is_false = "false" == value

    def is_null(self):
        return self._is_null

    def is_true(self):
        return self._is_true

    def is_false(self):
        return self._is_false

    def as_string(self):
        return self._value

    def is_boolean(self):
        return self._is_true or self._is_false


_LITERAL_NULL = _JsonLiteral("null")
_LITERAL_TRUE = _JsonLiteral("true")
_LITERAL_FALSE = _JsonLiteral("false")


class _Parser:
    def __init__(self, string):
        self._input = string
        self._index = -1
        self._line = 1
        self._capture_start = -1
        self._column = 0
        self._current = None
        self._capture_buffer = ""

    def parse(self):
        self._read()
        self._skip_white_space()
        result = self._read_value()
        self._skip_white_space()
        if not self._is_end_of_text():
            raise self._error("Unexpected character")
        return result

    def _read_value(self):
        if self._current == "n":
            return self._read_null()
        if self._current == "t":
            return self._read_true()
        if self._current == "f":
            return self._read_false()
        if self._current == '"':
            return self._read_string()
        if self._current == "[":
            return self._read_array()
        if self._current == "{":
            return self._read_object()
        if (
            self._current == "-"
            or self._current == "0"
            or self._current == "1"
            or self._current == "2"
            or self._current == "3"
            or self._current == "4"
            or self._current == "5"
            or self._current == "6"
            or self._current == "7"
            or self._current == "8"
            or self._current == "9"
        ):
            return self._read_number()
        raise self._expected("value")

    def _read_array_element(self, array):
        self._skip_white_space()
        array.add(self._read_value())
        self._skip_white_space()

    def _read_array(self):
        self._read()
        array = _JsonArray()
        self._skip_white_space()
        if self._read_char("]"):
            return array

        self._read_array_element(array)
        while self._read_char(","):
            self._read_array_element(array)

        if not self._read_char("]"):
            self._expected("',' or ']'")

        return array

    def _read_object_key_value_pair(self, obj):
        self._skip_white_space()
        name = self._read_name()
        self._skip_white_space()

        if not self._read_char(":"):
            raise self._expected("':'")

        self._skip_white_space()
        obj.add(name, self._read_value())
        self._skip_white_space()

    def _read_object(self):
        self._read()
        obj = _JsonObject()
        self._skip_white_space()
        if self._read_char("}"):
            return obj

        self._read_object_key_value_pair(obj)
        while self._read_char(","):
            self._read_object_key_value_pair(obj)

        if not self._read_char("}"):
            raise self._expected("',' or '}'")

        return obj

    def _read_name(self):
        if self._current != '"':
            raise self._expected("name")
        return self._read_string_internal()

    def _read_null(self):
        self._read()
        self._read_required_char("u")
        self._read_required_char("l")
        self._read_required_char("l")
        return _LITERAL_NULL

    def _read_true(self):
        self._read()
        self._read_required_char("r")
        self._read_required_char("u")
        self._read_required_char("e")
        return _LITERAL_TRUE

    def _read_false(self):
        self._read()
        self._read_required_char("a")
        self._read_required_char("l")
        self._read_required_char("s")
        self._read_required_char("e")
        return _LITERAL_FALSE

    def _read_required_char(self, ch):
        if not self._read_char(ch):
            raise self._expected("'" + ch + "'")

    def _read_string(self):
        return _JsonString(self._read_string_internal())

    def _read_string_internal(self):
        self._read()
        self._start_capture()
        while self._current != '"':
            if self._current == "\\":
                self._pause_capture()
                self._read_escape()
                self._start_capture()
            else:
                self._read()
        string = self._end_capture()
        self._read()
        return string

    def _read_escape_char(self):
        if self._current == '"':
            return '"'
        if self._current == "/":
            return "/"
        if self._current == "\\":
            return "\\"
        if self._current == "b":
            return "\b"
        if self._current == "f":
            return "\f"
        if self._current == "n":
            return "\n"
        if self._current == "r":
            return "\r"
        if self._current == "t":
            return "\t"
        raise self._expected("valid escape sequence")

    def _read_escape(self):
        self._read()
        self._capture_buffer += self._read_escape_char()
        self._read()

    def _read_number(self):
        self._start_capture()
        self._read_char("-")
        first_digit = self._current
        if not self._read_digit():
            raise self._expected("digit")

        if first_digit != "0":
            while self._read_digit():
                pass

        self._read_fraction()
        self._read_exponent()
        return _JsonNumber(self._end_capture())

    def _read_fraction(self):
        if not self._read_char("."):
            return False

        if not self._read_digit():
            raise self._expected("digit")

        while self._read_digit():
            pass

        return True

    def _read_exponent(self):
        if not self._read_char("e") and not self._read_char("E"):
            return False

        if not self._read_char("+"):
            return self._read_char("-")

        if self._read_digit():
            raise self._expected("digit")

        while self._read_digit():
            pass

        return True

    def _read_char(self, ch):
        if self._current != ch:
            return False
        self._read()
        return True

    def _read_digit(self):
        if not self._is_digit():
            return False
        self._read()
        return True

    def _skip_white_space(self):
        while self._is_white_space():
            self._read()

    def _read(self):
        if "\n" == self._current:
            self._line += 1
            self._column = 0

        self._index += 1

        if self._index < len(self._input):
            self._current = self._input[self._index]
        else:
            self._current = None

    def _start_capture(self):
        self._capture_start = self._index

    def _pause_capture(self):
        end = self._index if self._current is None else self._index - 1
        self._capture_buffer += self._input[self._capture_start : end + 1]
        self._capture_start = -1

    def _end_capture(self):
        end = self._index if self._current is None else self._index - 1

        if "" == self._capture_buffer:
            captured = self._input[self._capture_start : end + 1]
        else:
            self._capture_buffer += self._input[self._capture_start : end + 1]
            captured = self._capture_buffer
            self._capture_buffer = ""

        self._capture_start = -1
        return captured

    def _expected(self, expected):
        if self._is_end_of_text():
            return self._error("Unexpected end of input")

        return self._error("Expected " + expected)

    def _error(self, message):
        return _ParseException(message, self._index, self._line, self._column - 1)

    def _is_white_space(self):
        return (
            " " == self._current
            or "\t" == self._current
            or "\n" == self._current
            or "\r" == self._current
        )

    def _is_digit(self):
        return (
            "0" == self._current
            or "1" == self._current
            or "2" == self._current
            or "3" == self._current
            or "4" == self._current
            or "5" == self._current
            or "6" == self._current
            or "7" == self._current
            or "8" == self._current
            or "9" == self._current
        )

    def _is_end_of_text(self):
        return self._current is None


class _HashIndexTable:
    def __init__(self):
        self._hash_table = [0] * 32

    def add(self, name, index):
        slot = self._hash_slot_for(name)
        if index < 0xFF:
            # increment by 1, 0 stands for empty
            self._hash_table[slot] = (index + 1) & 0xFF
        else:
            self._hash_table[slot] = 0

    def get(self, name):
        slot = self._hash_slot_for(name)
        # subtract 1, 0 stands for empty
        return (self._hash_table[slot] & 0xFF) - 1

    @staticmethod
    def _string_hash(s):
        # this is not a proper hash, but sufficient for the benchmark,
        # and very portable!
        return len(s) * 1_402_589

    def _hash_slot_for(self, element):
        return self._string_hash(element) & len(self._hash_table) - 1


class _ParseException(Exception):
    def __init__(self, message, offset, line, column):
        super().__init__()
        self._message = message
        self._offset = offset
        self._line = line
        self._column = column

    def get_message(self):
        return self._message

    def get_offset(self):
        return self._offset

    def get_line(self):
        return self._line

    def get_column(self):
        return self._column


class _JsonArray(_JsonValue):
    def __init__(self):
        self._values = Vector()

    def add(self, value):
        if value is None:
            raise Exception("value is null")
        self._values.append(value)
        return self

    def size(self):
        return self._values.size()

    def get(self, index):
        return self._values.at(index)

    def is_array(self):
        return True

    def as_array(self):
        return self


class _JsonNumber(_JsonValue):
    def __init__(self, string):
        self._string = string
        if string is None:
            raise Exception("string is null")

    def as_string(self):
        return self._string

    def is_number(self):
        return True


class _JsonObject(_JsonValue):
    def __init__(self):
        self._names = Vector()
        self._values = Vector()
        self._table = _HashIndexTable()

    def add(self, name, value):
        if name is None:
            raise Exception("name is null")
        if value is None:
            raise Exception("value is null")

        self._table.add(name, self._names.size())
        self._names.append(name)
        self._values.append(value)
        return self

    def get(self, name):
        if name is None:
            raise Exception("name is null")

        index = self.index_of(name)
        return None if index == -1 else self._values.at(index)

    def size(self):
        return self._names.size()

    def is_empty(self):
        return self._names.is_empty()

    def is_object(self):
        return True

    def as_object(self):
        return self

    def index_of(self, name):
        index = self._table.get(name)
        if index != -1 and name == self._names.at(index):
            return index
        raise Exception("NotImplemented")  # Not needed for benchmark


class _JsonString(_JsonValue):
    def __init__(self, string):
        self._string = string

    def is_string(self):
        return True

import utime
class Run:
    def __init__(self, name):
        self._name = name
        self._benchmark_suite = Json
        self._total = 0
        self._num_iterations = 15
        self._inner_iterations = 1

    def run_benchmark(self):
        print("Starting " + self._name + " benchmark ...")

        self._do_runs(self._benchmark_suite())
        self._report_benchmark()
        print()

    def measure(self, bench):
        start_time = utime.ticks_ms()
        if not bench.inner_benchmark_loop(self._inner_iterations):
            raise Exception("Benchmark failed with incorrect result")

        end_time = utime.ticks_ms()
        run_time = utime.ticks_diff(end_time, start_time)
        

        #self._print_result(run_time)

        self._total += run_time

    def _do_runs(self, bench):
        for _ in range(self._num_iterations):
            self.measure(bench)

    def _report_benchmark(self):
        print(
            self._name
            + ": iterations="
            + str(self._num_iterations)
            + " average: "
            + str(round(self._total / self._num_iterations))
            + "ms total: "
            + str(self._total)
            + "ms\n"
        )

    def _print_result(self, run_time):
        print(self._name + ": iterations=1 runtime: " + str(run_time) + "ms")

    #def print_total(self):
        #print("Total Runtime: " + str(self._total) + "ms")

    def set_num_iterations(self, num_iterations):
        self._num_iterations = num_iterations

    def set_inner_iterations(self, inner_iterations):
        self._inner_iterations = inner_iterations

#Stacksize 1024*4096*20
test = Run("Json")
test.run_benchmark()
# VoxyPy    
 A data structure for Voxel operations.     
    
- Uses [NumPy](https://pypi.org/project/numpy/) for speed and efficiency.     
- Uses a modified version of [numpy-vox-io](https://github.com/alexhunsley/numpy-vox-io) for IO operations.    
    
## Quickstart 
```python  
from voxypy.models.models import Entity, Voxel
dense = np.zeros((10, 10, 10), dtype=int) 
entity = Entity(data=dense) 

entity.set(x=1, y=2, z=3, 42)   
voxel = entity.get(1, 2, 3) # Voxel object with value 42 

voxel.add(1) # Voxel object with value 43   
new_voxel = Voxel(255) 
new_voxel.add(1) # Returns Voxel object with value 1  
entity.set(5, 5, 5, new_voxel)
entity.set(5, 5, 5, 69)
  
entity = Entity().from_file('old_entity.vox')
entity.save('new_entity.vox')  
```    
 ## Voxel 
Voxel is a small class representing one cell in an Entity.    
  
Voxel colors are represented as indices from 0 to 255, where 0 means blank. These indices refer to actual RGB colors in a 1x255 `.png` file. So, for example, if the 10th pixel in the texture is red, then a voxel with value 10 will render as red.  
    
| Method     | Input                     | Output                                                                                                                                             |  
| ---------- | ------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |  
| `__init__` | `color` 0-255 (default 0) | Voxel object with color `color`. 0 is blank.                                                                                                       |  
| `get`      |                           | int value of voxel's `color`.                                                                                                                                                   |     |  
| `set`      | `color` 0-255             | Voxel object with color `color`                                                                                                                    |  
| `add`      | `amount` (default 1) | Adds `amount` to voxel's `color`. Adding 1 to 255 causes the color to wrap to 1 instead of 0. See preceding paragraph for info about voxel colors. |
| `subtract` | `amount` (default 1) | Subtracts `amount` from voxel's `color`. Just a wrapper for `add`. |
  
The Voxel equality operator works with ints and Voxels. Voxels can also be cast to ints.  
```python  
v1 = Voxel(1)  
v2 = Voxel(1)  
  
v1 == v2      # True  
v1 == 1       # True  
int(v1) == 1  # True  
v1 != 0       # True  
```  
  
## Entity  
An Entity is (conceptually) a 3d array of Voxels.  
  
Under the hood, an Entity is actually a 3d [NumPy ndarray](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html). Values are converted to Voxels during `get` and `set` methods. Voxels and ints can be used interchangeably in every case.

Entity can be initialized with 
- ints `x, y, z` which will create an Entity with those dimensions and filled with only zeros.
- or `data` which can only be a 3d ndarray. The contents will be copied into the new Entity.

Providing mismatched dimensions for `x, y, z` and `data` will throw an error. 


| Method       | Input                                 | Output                                                                      |
| ------------ | ------------------------------------- | --------------------------------------------------------------------------- |
| `get`        | `x, y, z`                             | A Voxel object from Entity at `[x, y, z]`                                   |
| `set`        | `x, y, z, color` where color is 0-255 | Sets Entity at `[x, y, z]` to `color` and returns self.                     |
| `get_dense`  |                                       | NumPy ndarray of ints, where each int is a valid voxel color.               |
| `from_dense` | 3d NumPy ndarray with dtype=int       | Overwrites Entity with new data                                             |
| `write`      | File name                             | Writes entity to a .vox file using py-vox-io                                |
| `save`       | File name                             | Same as `write`                                                             |
| `from_file`  | File name                             | Reads `.vox` file into an Entity, replacing existing data.                                                                            |
| `layers`     |                                       | Iterable list of z-layers.                                                  |
| `set_layer`  | `z`, ndarray `layer` with dtype=int   | Sets layer `z` of Entity to the contents of `layer`. Dimensions must match. |
| `flip`       |                                       | Flips the entity along the Z axis. |
  
The methods `get_dense` and `from_dense` can be combined to allow invocation of any [NumPy ndarray method](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html)  

```python  
entity = (x=10, y=10, z=10) # 10x10x10 Entity full of zeros.  
ones = entity.get_dense().fill(1)  # 10x10x10 ndarray full of ones.  
entity.from_dense(ones)  # 10x10x10 Entity full of ones.  
# one liner  
entity.from_dense(entity.get_dense().fill(1))  
```

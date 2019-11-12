# image-to-pointCloud

At times I need very simple textured based pointclouds to do stuff like denoising, segmentation etc. This simple project aims 
to convert simple textured based images to 3d point clouds with some distortion.


# Results

> Here see that how I converted the lena image into 3d point-cloud.

![result](./data/lena.png)

![result](./result.png)

> And a simple gimp-texture is converted to a point-cloud which shall be used later to segment the two textures.

![result](./data/gimp_texture.png)


![result](./result2.png)

# Usage

```bash
python image_To_pcd.py -i ./data/wood.png -d 1
```
> This should generate the .ply file in the working directory. The `-d` flag other than 1 means the image will not be distored.

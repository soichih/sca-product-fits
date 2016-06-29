## Installation

For png > dzi conversion, you need to install depzoom.py on the resource that you are running this service
> https://github.com/openzoom/deepzoom.py.git

## conversion script

fits2img.py analyzes input fits image and convert to png using the optimal scaling.

```
../mef2fits.py m67.single.fits m67.mef.fits
../fits2img.py -t png -o m67 m67.single.fits
```

## Notes

gm(GraphicsMagick) can also convert fits(including multi extension) to png

```
gm convert 20121009T153329.0.fits 20121009T153329.0.png
```

Converting image to DZI (compatible with openseadragon) could be done with tools like https://github.com/vikbez/img2dzi

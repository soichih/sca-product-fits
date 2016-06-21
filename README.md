## conversion script

fits2img.py analyzes input fits image and convert to png using the optimal scaling.

```
../fits2img.py -t png -o m67 m67.fits  
```

## Notes

fits2img.py doesn't work on some ODI detrended images.

```
$ ./fits2img.py -t png -o 20121009T153329.0 ~/workflows/570d14e266a1e2fc1ef5a843/57684fa567c3f50d4b214cb2/output/20121009T153329.0.fits
Traceback (most recent call last):
 File "./fits2img.py", line 71, in <module>
   data[(data<options.mingood)|(data>options.maxgood)] = numpy.NaN
TypeError: 'NoneType' object does not support item assignment
```

gm(GraphicsMagick) convert works, on the other hand..

```
gm convert 20121009T153329.0.fits 20121009T153329.0.png
```

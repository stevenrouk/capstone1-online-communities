Here are the rough steps you can use to create a .gif from images.

1. Make sure you have your images in the same folder. For the sake of this example, we'll assume they're all named "my_image_01.png", with numbers indicating the order.
2. Make duplicate copies of your image to slow down the speed at which the images progress. 10 or 20 copies of each image seems to be a nice speed (at least when I tested it). You can use a variation of this script to make copies. (Make sure not to overwrite your other images—name these copies something slightly different. In this case, I'll have my original images saved with two digits, and my copies will all have three digits. Ex: my_image_01.png for the original, my_image_001.png for the copy.)

```bash
for i in {1..9}; do cp my_image_01.png "my_image_00$i.png"; done
for i in {10..19}; do cp my_image_02.png "my_image_0$i.png"; done
```

3. Now, you can combine the images you just created into a gif using the ffmpeg utility. (`brew install ffmpeg` if you don't already have it.) This gives the gif a white background rather than the default of black. If you don't need the white background, you can just use `ffmpeg -i my_image_%03d.png myimage.gif`.

```bash
ffmpeg -f lavfi -i color=white -i my_image_%03d.png -filter_complex "[0][1]scale2ref[bg][gif];[bg]setsar=1[bg];[bg][gif]overlay=shortest=1" myimage.gif
```


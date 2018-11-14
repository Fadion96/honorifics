#AV1 codec

###Aomenc installation
#####Windows installation: 
https://nwgat.ninja/compile-av1-using-msys2-mingw/
#####Linux installation:
https://nwgat.ninja/compiling-aomedia-av1-on-ubuntu/

https://aomedia.googlesource.com/aom/#building-the-library-and-applications

###Video encoding
`ffmpeg -i [input] -pix_fmt yuv420p [file].y4m`

`./aomenc.exe -p 2 --pass=1 -t 3 --cpu-used=4 --tile-columns=6 --frame-parallel=1 -w 1280 -h 720 --auto-alt-ref=1 --lag-in-frames=25 --profile=0 --target-bitrate=2000 --fpf=[output].log -o [output].mkv [file].y4m`

`./aomenc.exe -p 2 --pass=2 -t 3 --cpu-used=4 --tile-columns=6 --frame-parallel=1 -w 1280 -h 720 --auto-alt-ref=1 --lag-in-frames=25 --profile=0 --target-bitrate=2000 --fpf=[output].log -o [output].mkv [file].y4m`
###Video players which supports AV1:
#####VLC:
https://www.videolan.org/vlc/ - stable release, works on Linux only

https://nightlies.videolan.org/ - unstable builds 
#####MPC-HC (unofficial)
https://github.com/clsid2/mpc-hc/releases
#####MPV
https://mpv.io/
#####MPC-BE
https://sourceforge.net/projects/mpcbe/files/MPC-BE/Release%20builds/


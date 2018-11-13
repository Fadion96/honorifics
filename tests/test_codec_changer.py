import unittest

from honorifics.codec_changer import CodecChanger


class TestCodecChanger(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.codec_changer = CodecChanger(".\Aruku.mp4", "negated.mp4", False,
                                         timestamps=[[149.451, 162.751],
                                                     [219.222, 235.777],
                                                     [259.444, 276.674]])
        cls.second_codec_changer = CodecChanger(".\syake.mp4", "output.mkv", True, timestamps=[[10.0, 20.0]],
                                                subtitles=".\subs.ass", start=5.0, end=80.0)

    def test_make_command(self):
        first_command = "ffmpeg -y -i .\Aruku.mp4 -filter_complex \"" \
                        "[0:0]trim=start=0:end=149.451[a];" \
                        "[0:0]trim=start=149.451:end=162.751,setpts=PTS-STARTPTS[trimmed0];" \
                        "[trimmed0]negate[negation0];[a][negation0]concat[negated0];" \
                        "[0:0]trim=start=162.751:end=219.222,setpts=PTS-STARTPTS[nor0];" \
                        "[negated0][nor0]concat[normal0];" \
                        "[0:0]trim=start=219.222:end=235.777,setpts=PTS-STARTPTS[trimmed1];" \
                        "[trimmed1]negate[negation1];" \
                        "[normal0][negation1]concat[negated1];" \
                        "[0:0]trim=start=235.777:end=259.444,setpts=PTS-STARTPTS[nor1];" \
                        "[negated1][nor1]concat[normal1];" \
                        "[0:0]trim=start=259.444:end=276.674,setpts=PTS-STARTPTS[trimmed2];" \
                        "[trimmed2]negate[negation2];" \
                        "[normal1][negation2]concat[negated2];" \
                        "[0:0]trim=start=276.674,setpts=PTS-STARTPTS[ending];" \
                        "[negated2][ending]concat[out1];[out1]scale=-1:360[out2]\" " \
                        "-map [out2] -c:v libx264 -preset ultrafast negated.mp4"
        self.assertEqual(first_command, self.codec_changer.make_command())
        second_command = "ffmpeg -y -i .\syake.mp4 -filter_complex \"" \
                         "[0:0]trim=start=5.0:end=10.0[a];" \
                         "[0:0]trim=start=10.0:end=20.0,setpts=PTS-STARTPTS[trimmed0];" \
                         "[trimmed0]deband[debanded0];" \
                         "[debanded0]noise=alls=6:allf=t[noise0];" \
                         "[a][noise0]concat[debnoise0];" \
                         "[0:0]trim=start=20.0:end=80.0,setpts=PTS-STARTPTS[ending];" \
                         "[debnoise0][ending]concat[subs];" \
                         "[subs]ass=.\subs.ass[out1]\" " \
                         "-map [out1] -c:v libvpx-vp9 -pass 1 -pix_fmt yuv420p -crf 21 -threads 3 -speed 4 -tile-columns 6 -frame-parallel 1 -b:v 0 -an -f matroska /dev/null " \
                         "&& ffmpeg -y -i .\syake.mp4 -filter_complex \"" \
                         "[0:0]trim=start=5.0:end=10.0[a];" \
                         "[0:0]trim=start=10.0:end=20.0,setpts=PTS-STARTPTS[trimmed0];" \
                         "[trimmed0]deband[debanded0];" \
                         "[debanded0]noise=alls=6:allf=t[noise0];" \
                         "[a][noise0]concat[debnoise0];" \
                         "[0:0]trim=start=20.0:end=80.0,setpts=PTS-STARTPTS[ending];" \
                         "[debnoise0][ending]concat[subs];" \
                         "[subs]ass=.\subs.ass[out1]\" " \
                         "-map [out1] -c:v libvpx-vp9 -pass 2 -pix_fmt yuv420p -crf 21 -threads 3 -speed 1 -tile-columns 6 -frame-parallel 1 -b:v 0 -auto-alt-ref 1 -lag-in-frames 25 -an -f matroska output.mkv"
        self.assertEqual(second_command, self.second_codec_changer.make_command())

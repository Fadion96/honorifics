from typing import Dict, List, Tuple


class CodecChanger(object):
    def __init__(self, input_file: str, output_file: str, debanding: bool, subtitles: str = None,
                 timestamps: List[float] = None, durations: List[float] = None):
        self.input = input_file
        self.output = output_file
        self.debanding = debanding
        self.subtitles = subtitles if timestamps is not None else ""
        self.timestamps = timestamps if timestamps is not None else []
        self.durations = durations if durations is not None else []

    def __start_of_video(self):
        return "\"[0:0]trim=start=0:duration=" + str(self.timestamps[0]) + "[a];", "[a]"

    def __negation_part(self, last_part: str, number: int) -> Tuple[str, str]:
        result = "[0:0]trim=start=" + str(self.timestamps[number]) + ":duration=" + str(
            self.durations[number]) + ",setpts=PTS-STARTPTS[trimmed" + str(
            number) + "];"
        result += "[trimmed" + str(number) + "]negate[negation" + str(number) + "];"
        result += last_part + "[negation" + str(number) + "]concat[negated" + str(number) + "];"
        return result, "[negated" + str(number) + "]"

    def __deband_noise_part(self, last_part: str, number: int) -> Tuple[str, str]:
        result = "[0:0]trim=start=" + str(self.timestamps[number]) + ":duration=" \
                 + str(self.durations[number]) + ",setpts=PTS-STARTPTS[trimmed" + str(number) + "];"
        result += "[trimmed" + str(number) + "]deband[debanded" + str(number) + "];"
        result += "[debanded" + str(number) + "]noise=alls=6:allf=t[noise" + str(number) + "];"
        result += last_part + "[noise" + str(number) + "]concat[debnoise" + str(number) + "];"
        return result, "[debnoise" + str(number) + "]"

    def __normal_part(self, last_part: str, number: int) -> Tuple[str, str]:
        normal_timestamp = round(self.timestamps[number] + self.durations[number], 3)
        normal_duration = round(self.timestamps[number + 1] - normal_timestamp, 3)
        result = "[0:0]trim=start=" + str(normal_timestamp) + ":duration=" + str(
            normal_duration) + ",setpts=PTS-STARTPTS[nor" + str(
            number) + "];"
        result += last_part + "[nor" + str(number) + "]concat[normal" + str(number) + "];"
        return result, "[normal" + str(number) + "]"

    def __end_of_video(self, last_part: str) -> str:
        last_index = len(self.timestamps) - 1
        last_timestamp = round(self.timestamps[last_index] + self.durations[last_index], 3)
        result = "[0:0]trim=start=" + str(last_timestamp) + ",setpts=PTS-STARTPTS[ending];"
        if self.subtitles:
            result += last_part + "[ending]concat[subs];"
            result += "[subs]ass=" + self.subtitles.replace(".\\", "") + "[out1]\" "
        else:
            result += last_part + "[ending]concat[out1]\" "
        return result

    def __make_deband_command(self) -> str:
        first_pass = "ffmpeg -y -i " + self.input
        second_pass = " && ffmpeg -y -i " + self.input
        if self.timestamps:
            filter_complex = " -filter_complex "
            start, last_part = self.__start_of_video()
            filter_complex += start
            for i in range(len(self.timestamps) - 1):
                debanded, last_part = self.__deband_noise_part(last_part, i)
                filter_complex += debanded
                normal, last_part = self.__normal_part(last_part, i)
                filter_complex += normal
            last_debanded, last_part = self.__deband_noise_part(last_part, len(self.timestamps) - 1)
            filter_complex += last_debanded
            ending = self.__end_of_video(last_part)
            filter_complex += ending + "-map [out1]"
            first_pass += filter_complex
            second_pass += filter_complex
        else:
            if self.subtitles:
                first_pass += " -vf \"ass=" + self.subtitles.replace(".\\", "") + "\" "
                second_pass += " -vf \"ass=" + self.subtitles.replace(".\\", "") + "\" "
        first_pass += " -c:v libvpx-vp9 -pass 1 -pix_fmt yuv420p -crf 21 -threads 3 -speed 4 -tile-columns 6 -frame-parallel 1 -b:v 0 -an -f matroska /dev/null"
        second_pass += " -c:v libvpx-vp9 -pass 2 -pix_fmt yuv420p -crf 21 -threads 3 -speed 1 -tile-columns 6 -frame-parallel 1 -b:v 0 -auto-alt-ref 1 -lag-in-frames 25 -an -f matroska " + self.output
        command = first_pass + second_pass
        return command

    def __make_negation_command(self) -> str:
        command = "ffmpeg -y -i " + self.input
        if self.timestamps:
            filter_complex = " -filter_complex "
            start, last_part = self.__start_of_video()
            filter_complex += start
            for i in range(len(self.timestamps) - 1):
                negated, last_part = self.__negation_part(last_part, i)
                filter_complex += negated
                normal, last_part = self.__normal_part(last_part, i)
                filter_complex += normal
            last_negated, last_part = self.__negation_part(last_part, len(self.timestamps) - 1)
            filter_complex += last_negated
            ending = self.__end_of_video(last_part)
            filter_complex += ending[:-2] + ";[out1]scale=-1:360[out2]\" -map [out2]"
            command += filter_complex
        command += " -c:v libx264 -preset ultrafast " + self.output
        return command

    def make_command(self) -> str:
        if self.debanding:
            command = self.__make_deband_command()
        else:
            command = self.__make_negation_command()
        return command

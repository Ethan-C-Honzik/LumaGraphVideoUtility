# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import ffmpeg
from PIL import Image
import binascii
import os


def generateByteArray(colorStr: str):
    return binascii.unhexlify(colorStr)


def ffmpegVideoGen(name: str, images: list, durations: list):
    # Create a list of png files and their durations
    # png_files = ["images/Test2333.png", "images/Test2335.png", "images/Test2349.png"]
    # durations = [3, 10, 3]

    # Create a text file with the concat filter format
    with open("frametimes.txt", "w") as f:
        for png_file, duration in zip(images, durations):
            f.write(f"file {png_file}\n")
            f.write(f"duration {duration}\n")

    # Use ffmpeg-python to convert the text file into a video
    stream = ffmpeg.input("frametimes.txt", format="concat")
    stream = ffmpeg.output(stream, f"{name}.mp4", r='24', vcodec="libx264")
    ffmpeg.run(stream)


def genVid(lines: list):
    sequence_name = lines[0]
    images = []
    times = []
    for index, line in enumerate(lines):
        if index == 0:
            continue
        if line == '':
            break
        data = line.split(',')
        times.append(float(data[0])/1000)
        color_str = data[1]
        res = len(color_str) // 6
        image = Image.frombytes('RGB', (res, 1), generateByteArray(color_str))
        image = image.resize((512, 256))
        if not os.path.exists(f'images/{sequence_name}_images'):
            os.mkdir(f'images/{sequence_name}_images')
        path = f'images/{sequence_name}_images/frame_{index}.png'
        images.append(path)
        image.save(path)
    images = images[:len(images) - 1]
    durations = [times[i + 1] - times[i] for i in range(len(times) - 1)]
    ffmpegVideoGen(sequence_name, images, durations)


def parseFile(file_dir: str):
    file = open(file_dir)
    lines = file.read().replace(' ', '_')
    sequences = lines.split('-')
    for sequence in sequences:
        if sequence == '':
            continue
        lines = sequence.splitlines()
        genVid(lines)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parseFile('borealis.txt')
    # ffmpegTest()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

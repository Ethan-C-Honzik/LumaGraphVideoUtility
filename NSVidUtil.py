# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sys
from Options import Options
import json
from PIL import Image
import binascii
import os
import ffmpeg


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
    stream = ffmpeg.output(stream, f"{name}.mp4", r=f'{options.frameRate}', vcodec="libx264")
    ffmpeg.run(stream)


def genVid(lines: list):
    sequence_name = lines[0]
    images = []
    times = []
    if not os.path.exists('NSVidUtilImages'):
        os.mkdir('NSVidUtilImages')
    for index, line in enumerate(lines):
        if index == 0:
            continue
        if line == '':
            break
        data = line.split(',')
        times.append(float(data[0]) / 1000)
        color_str = data[1]
        res = len(color_str) // 6
        image = Image.frombytes('RGB', (res, 1), generateByteArray(color_str))
        image = image.resize((options.width, options.height))
        path = f'NSVidUtilImages/{sequence_name}_images'
        if not os.path.exists(path):
            os.mkdir(path)
        path = path + f'/frame_{index}.png'
        images.append(path)
        image.save(path, compress_level=9)
    images = images[:len(images) - 1]
    durations = [times[i + 1] - times[i] for i in range(len(times) - 1)]
    ffmpegVideoGen(sequence_name, images, durations)


def parse_text(rawData: str):
    lines = rawData.replace(' ', '_')
    sequences = lines.split('-')
    for sequence in sequences:
        if sequence == '':
            continue
        lines = sequence.splitlines()
        genVid(lines)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    options = Options()
    file_name = 'options.json'
    settings_path = os.path.join(os.getcwd(), file_name)
    if not os.path.exists(settings_path):
        print("no settings file detected in directory, creating a new file. Hit enter when settings are finalized")
        # Save the instance to a JSON file
        with open(file_name, 'w') as json_file:
            json_file.write(options.to_json())
        input()
        print("continuing...")
    # Load the instance from the JSON file
    with open(file_name, 'r') as json_file:
        data = json.load(json_file)
    options = options.from_dict(data)
    parse_text(open(sys.argv[1]).read())
    print("Press enter to continue . . .")
    input()
    # ffmpegTest()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

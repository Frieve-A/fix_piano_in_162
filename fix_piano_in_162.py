import soundfile as sf
import numpy as np
import argparse
import glob
import os
from tqdm import tqdm

def func(args):
    files = glob.glob(os.path.join(args.input_dir, '**\*.flac'))
    print(f'{len(files)} flac files are found.')
    for file in files:
        try:
            data, freq = sf.read(file)
        except:
            continue
        pos = np.where(data > 0.001)[0][0]
        if pos > 0:
            zcpos = np.where(data[0:pos] <= 0.0)[0]
            if len(zcpos):
                zcpos = zcpos[-1] + 1
                data = data[zcpos:]
                sf.write(file, data, freq, format='FLAC', subtype='PCM_24')
                print(f'{zcpos}\t{file[-70:]}')

def main():
    parser = argparse.ArgumentParser(
        description='Fix FLAC files of Piano in 162.',
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        '-i',
        '--input-dir',
        help='path where FLAC files are placed',
        required=True)
    parser.set_defaults(func=func)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()


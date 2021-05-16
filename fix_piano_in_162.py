import soundfile as sf
import numpy as np
import argparse
import glob
import os
import traceback
from tqdm import tqdm

def func(args):
    flac_pattern = '**\*.flac' if os.name == "nt" else '**/*.flac'
    files = glob.glob(os.path.join(args.input_dir, flac_pattern), recursive=True)
    print(f'{len(files)} flac files are found.')

    exceps = {}
    for file in files:
        try:
            data, freq = sf.read(file)
            body_idxs = np.where(data > 0.001)

            if len(body_idxs[0]) == 0:
                print(f'skip {file}')
                continue

            pos = body_idxs[0][0]
            if pos > 0:
                zcpos = np.where(data[0:pos] <= 0.0)[0]
                if len(zcpos):
                    zcpos = zcpos[-1] + 1
                    data = data[zcpos:]
                    sf.write(file, data, freq, format='FLAC', subtype='PCM_24')
                    print(f'{zcpos}\t{file[-70:]}')
        except Exception as e:
            exceps[file] = traceback.format_exc()
            print(f'file: {file}\n{exceps[file]}')
            continue
    return exceps

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
    exceps = args.func(args)
    exit(len(exceps))

if __name__ == '__main__':
    main()


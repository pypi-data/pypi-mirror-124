import pprint
import argparse
import sys
sys.path.insert(0, '.')
import tempfile

from tl2.tl2_utils import get_filelist_recursive
from tl2.proj.logger.logger_utils import get_file_logger


def main():

  file_list = get_filelist_recursive(directory=args.source_dir, ext=args.ext, sort=True)
  print("")

  if not args.outfile:
    fd, path = tempfile.mkstemp()
    args.outfile = path

  out_f = get_file_logger(args.outfile, stream=True)
  for path in file_list:
    out_f.info_msg(path)

  print(f"\noutfile: {args.outfile}")
  print(f"number of items: {len(file_list)}\n")
  pass

if __name__ == '__main__':
  """
  python3 -m tl2.tools.get_data_list \
    --source_dir  \
    --outfile  \
    --ext *.png
  """
  parser = argparse.ArgumentParser()
  parser.add_argument('--source_dir', type=str, default="")
  parser.add_argument('--outfile', type=str, default="")
  parser.add_argument('--ext', type=str, nargs='+', default=["*.png", "*.jpg", "*.jfif", "*.jpeg"])

  args = parser.parse_args()
  pprint.pprint(vars(args))
  main()


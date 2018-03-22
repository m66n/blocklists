#!/usr/bin/env python3

import argparse
import sys


def parse_file(filename):
  comments = []
  entries = []
  with open(filename) as f:
    for line in f:
      line = line.strip()
      if line.startswith('#') and len(entries) == 0:
        comments.append(line)
      else:
        segments = line.split()
        if len(segments) != 2:
          continue
        units = segments[1].split('.')
        if len(units) < 2:
          continue
        entries.append((line,
            (units[-2], units[-1], ' '.join(units[:-2]))))
  return comments, entries


def main():
  parser = argparse.ArgumentParser(description='Sort hosts file.')
  parser.add_argument('input', help='hosts file to sort',
      metavar='<input-file>')
  parser.add_argument('-o', '--out', help='output file',
      metavar='<output-file>', dest='output')

  args = parser.parse_args()

  if not args.output:
    args.output = args.input

  comments, entries = parse_file(args.input)

  # dedupe entries
  entries = list(dict.fromkeys(entries))

  entries.sort(key=lambda x: (x[1][0], x[1][1], x[1][2]))

  with open(args.output, 'w') as f:
    for item in comments:
      f.write('{}\n'.format(item))
    if len(comments) > 0:
      f.write('\n')
    for item in entries:
      f.write('{}\n'.format(item[0]))

  return 0


if __name__ == '__main__':
  sys.exit(main())

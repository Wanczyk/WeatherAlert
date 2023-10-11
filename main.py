import asyncio
from argparse import ArgumentParser

from src.app import app

parser = ArgumentParser()

parser.add_argument("-t", required=True, type=float, help="Temp threshold")
parser.add_argument("-r", required=True, type=float, help="Rain threshold")

args = parser.parse_args()

asyncio.run(app(args.t, args.r))

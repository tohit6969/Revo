# Revo/src/inference/run_inference.py
import argparse
from core.model import generate_mesh  # your PIFuHD wrapper
import os

def main(input_image: str, output_dir: str):
    mesh_path = generate_mesh(input_image, output_dir)
    print(mesh_path)  # subprocess stdout

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input",  required=True, help="Path to input image")
    parser.add_argument("--output", required=True, help="Directory to write .obj file")
    args = parser.parse_args()
    main(args.input, args.output)

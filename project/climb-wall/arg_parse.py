import argparse

def parser():
    parser = argparse.ArgumentParser(
        description=("Select Object")
    )
    # parser.add_argument("--img", type=str, required=True)
    parser.add_argument("--checkpoint", type=str, default="/Users/tiankonguse-m3/project/github/segment-anything/checkpoint/sam_vit_h_4b8939.pth")
    parser.add_argument("--device", type=str, default="cpu")
    parser.add_argument("--model_type", type=str, default="vit_h")
    parser.add_argument(
        "--output",
        type=str,
        default=None, 
        help=(
            "Path to the directory where masks will be output. Output will be either a folder "
            "of PNGs per image or a single json with COCO-style masks."
        ),
    )
    return parser
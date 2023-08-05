from videdit.commands import cut_video
from videdit.parse import parse_args


def main():
    args = parse_args()
    
    if args.command == "cut":
        cut_video(
            file=args.file,
            output=args.file if args.inplace else args.output,
            intervals=args.intervals
        )


if __name__ == "__main__":
    main()

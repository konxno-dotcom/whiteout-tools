print("app imported")

from whiteout_tools.data import PACKS  # noqa: E402


def main() -> None:
    print(f"{len(PACKS)} packs loaded")

    for pack in PACKS:
        print(pack)


if __name__ == "__main__":
    print("__name__ =", __name__)
    main()
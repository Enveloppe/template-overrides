import argparse
import os
from git import Repo


def create_tag(tag_name: str):
    repo = Repo(os.path.dirname(os.path.realpath(__file__)))
    repo.create_tag(tag_name, message=f"chore(bump): v{tag_name}")
    print(f"Tag {tag_name} created")
    # commit changelog
    repo.git.add("CHANGELOG.md")
    repo.git.add("version.txt")
    repo.index.commit("chore(version): update version")
    print("Changelog updated | Version file updated")
    # push tag
    try:
        origin = repo.remote(name="origin")
        origin.push()
        origin.push(tag_name)
        print("Tag pushed to origin")
    except OSError:
        os.system(f"git push --atomic origin main {tag_name}")


def generate_changelog(version: str):
    print(f"Generating changelog for version {version}")
    os.system(f"git-chglog --next-tag v{version} --output CHANGELOG.md")

def generate_version_file(version: str):
    print(f"Generating version file for version {version}")
    with open("version.txt", "w") as f:
        f.write(version)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("version", help="Version to create tag for")
    args = parser.parse_args()
    generate_changelog(args.version)
    generate_version_file(args.version)
    create_tag(args.version)

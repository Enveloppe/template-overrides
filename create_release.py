import argparse
import os
from git import Repo


def create_tag(tag_name: str):
    repo = Repo(os.path.dirname(os.path.realpath(__file__)))
    tag = repo.create_tag(tag_name, message=f"chore(bump): v{tag_name}")
    print(f"Tag {tag_name} created")
    # commit
    repo.git.add(update=True)
    repo.index.commit(f"chore(bump): v{tag_name}")
    repo.remotes.origin.push(tag.path)

def generate_changelog(version: str):
    print(f"Generating changelog for version {version}")
    os.system(f"git-chglog --next-tag v{version} --output CHANGELOG.md")



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("version", help="Version to create tag for")
    args = parser.parse_args()
    generate_changelog(args.version)
    create_tag(args.version)

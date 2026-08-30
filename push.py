import subprocess
import sys


def run_command(command, error_message):
    """Helper function to run shell commands and handle errors."""
    try:
        result = subprocess.run(
            command,
            check=True,
            shell=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if result.stdout:
            print(result.stdout.strip())
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] {error_message}")
        if e.stderr:
            print(e.stderr.strip())
        sys.exit(1)


def main():
    print("=== GCK Site Git Automation Tool ===\n")

    # 1. Check git status to see if there are changes
    status_result = subprocess.run(
        "git status --porcelain",
        shell=True,
        text=True,
        stdout=subprocess.PIPE,
    )
    if not status_result.stdout.strip():
        print("[INFO] Working directory clean. No changes to push.")
        sys.exit(0)

    print("[1/4] Staging all changes...")
    run_command("git add .", "Failed to stage files using 'git add .'")

    # 2. Get commit message from user
    print("\n[2/4] Enter your commit message:")
    commit_msg = input(" > ").strip()

    if not commit_msg:
        print(
            "[WARNING] Commit message cannot be empty. Aborting operation."
        )
        sys.exit(1)

    print("\n[3/4] Committing changes...")
    run_command(
        f'git commit -m "{commit_msg}"', "Failed to commit changes."
    )

    # 4. Push to remote repository
    print("\n[4/4] Pushing changes to remote repository...")
    run_command("git push", "Failed to push to remote repository.")

    print("\nSUCCESS: All changes successfully pushed to Git! 🚀")


if __name__ == "__main__":
    main()
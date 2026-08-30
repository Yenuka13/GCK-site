import os
import subprocess
import sys


def run_command(command, error_message, allow_failure=False):
    """Helper function to run shell commands and handle errors."""
    print(f"Running: {command}")
    result = subprocess.run(
        command,
        shell=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if result.stdout:
        print(result.stdout.strip())

    if result.returncode != 0:
        if allow_failure:
            print(f"[WARNING] Command failed, but continuing: {error_message}")
            if result.stderr:
                print(result.stderr.strip())
            return False
        else:
            print(f"\n[ERROR] {error_message}")
            if result.stderr:
                print(result.stderr.strip())
            sys.exit(1)
    return True


def main():
    print("=== GCK Site PythonAnywhere Smart Update Tool ===\n")

    # 1. Stash any accidental local modifications just in case
    print("[1/5] Staging/stashing local state...")
    run_command("git stash", "Failed to stash local changes.",
                allow_failure=True)

    # 2. Pull latest changes from remote Git repository using rebase to prevent divergence errors
    print("\n[2/5] Pulling latest code from GitHub (with rebase)...")
    run_command(
        "git pull origin main --rebase",
        "Failed to pull from Git repository. Check for code/settings merge conflicts."
    )

    # 3. Run database migrations (handles new app structures and field alterations)
    print("\n[3/5] Applying database migrations...")
    run_command(
        "python manage.py migrate",
        "Failed to apply database migrations."
    )

    # 4. Collect static files cleanly (clearing old cache first)
    print("\n[4/5] Collecting static files...")
    run_command(
        "python manage.py collectstatic --noinput --clear",
        "Failed to collect static files.",
        allow_failure=True
    )

    print("\n[5/5] SUCCESS: Repository successfully synchronized and updated! 🚀")
    print("-" * 65)
    print("IMPORTANT REMINDER:")
    print("Go to your PythonAnywhere **Web** tab and click the green **Reload**")
    print("button to apply the new code changes to your live web server!")
    print("-" * 65)


if __name__ == "__main__":
    main()

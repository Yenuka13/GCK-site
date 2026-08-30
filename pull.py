import os
import subprocess
import sys


def run_command(command, error_message):
    """Helper function to run shell commands and handle errors."""
    try:
        print(f"Running: {command}")
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
    print("=== GCK Site PythonAnywhere Update Tool ===\n")

    # 1. Pull latest changes from remote Git repository
    print("[1/3] Pulling latest code from Git...")
    run_command("git pull", "Failed to pull from Git repository.")

    # 2. Run database migrations
    print("\n[2/3] Applying database migrations...")
    run_command(
        "python manage.py migrate",
        "Failed to apply database migrations.",
    )

    # 3. Collect static files for production
    print("\n[3/3] Collecting static files...")
    run_command(
        "python manage.py collectstatic --noinput",
        "Failed to collect static files.",
    )

    print("\nSUCCESS: Site successfully updated and synchronized! 🚀")
    print(
        "[REMOTE NOTE]: Don't forget to go to your PythonAnywhere Web tab and click **Reload** to apply the new code."
    )


if __name__ == "__main__":
    main()

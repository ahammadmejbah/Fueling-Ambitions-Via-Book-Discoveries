import os
import subprocess

# ==========================================
# CONFIGURATION
# ==========================================

TARGET_DATE = "2026-05-18"

# ==========================================
# START
# ==========================================

print(f"Cleaning all README.md files...")
print(f"Creating commits for {TARGET_DATE}...\n")

commit_counter = 0

# ==========================================
# WALK THROUGH ALL DIRECTORIES
# ==========================================

for root, dirs, files in os.walk("."):

    # Skip .git directory
    if ".git" in dirs:
        dirs.remove(".git")

    folder_name = os.path.basename(root)

    if folder_name in ["", "."]:
        folder_name = "Root"

    readme_path = os.path.join(root, "README.md")

    try:

        # ==========================================
        # ENSURE README EXISTS
        # ==========================================

        if not os.path.exists(readme_path):

            with open(readme_path, "w", encoding="utf-8") as f:
                pass

        # ==========================================
        # TEMPORARY CONTENT FOR COMMIT
        # ==========================================

        with open(readme_path, "a", encoding="utf-8") as f:
            f.write(f"Verified on: {TARGET_DATE}\n")

        # ==========================================
        # STAGE FILE
        # ==========================================

        subprocess.run(
            ["git", "add", readme_path],
            check=True
        )

        # ==========================================
        # UNIQUE TIMESTAMP
        # ==========================================

        minutes = (commit_counter // 60) % 60
        seconds = commit_counter % 60

        timestamp = f"12:{minutes:02d}:{seconds:02d}"
        full_date = f"{TARGET_DATE} {timestamp}"

        env = os.environ.copy()
        env["GIT_AUTHOR_DATE"] = full_date
        env["GIT_COMMITTER_DATE"] = full_date

        # ==========================================
        # COMMIT
        # ==========================================

        subprocess.run(
            [
                "git",
                "commit",
                "-m",
                f"Docs: updated {folder_name}"
            ],
            env=env,
            check=True
        )

        print(f"✅ Commit created for: {folder_name}")

        commit_counter += 1

    except Exception as e:

        print(f"❌ Failed in: {folder_name}")
        print(e)

# ==========================================
# CLEAN ALL README FILES
# ==========================================

print("\nCleaning all README.md files...\n")

for root, dirs, files in os.walk("."):

    if ".git" in dirs:
        dirs.remove(".git")

    readme_path = os.path.join(root, "README.md")

    try:

        if os.path.exists(readme_path):

            # EMPTY THE FILE COMPLETELY
            with open(readme_path, "w", encoding="utf-8") as f:
                pass

    except Exception as e:

        print(f"❌ Could not clean: {readme_path}")
        print(e)

# ==========================================
# FINAL CLEANUP COMMIT
# ==========================================

subprocess.run(["git", "add", "."], check=True)

cleanup_env = os.environ.copy()
cleanup_env["GIT_AUTHOR_DATE"] = f"{TARGET_DATE} 23:59:59"
cleanup_env["GIT_COMMITTER_DATE"] = f"{TARGET_DATE} 23:59:59"

subprocess.run(
    [
        "git",
        "commit",
        "-m",
        "Cleanup: emptied all README files"
    ],
    env=cleanup_env,
    check=True
)

# ==========================================
# PUSH TO GITHUB
# ==========================================

print(f"\nPushing {commit_counter + 1} commits...\n")

subprocess.run(
    ["git", "push", "origin", "main"],
    check=True
)

print("\n✅ DONE!")
print("All README.md files are now completely empty.")
#!/usr/bin/env python3
"""Publish daily game market report to skillworks-site.

Run after data collection pipeline completes.
1. Regenerates dashboard.html from latest data
2. Copies files to skillworks-site/public/game-market-daily/
3. Commits and pushes to GitHub

Usage: python3 publish_daily.py [--skip-collect] [--dry-run]
"""

import subprocess
import shutil
import sys
from pathlib import Path
from datetime import datetime

GAME_MONITOR = Path.home() / "projects/game-monitor"
AD_MONITOR = Path.home() / "projects/ad-monitor"
SITEWORKS = Path.home() / "projects/skillworks-site"

PUBLIC_DIR = SITEWORKS / "public" / "game-market-daily"


def run(cmd, cwd=None, check=True):
    """Run shell command, return output."""
    result = subprocess.run(
        cmd, shell=True, cwd=cwd,
        capture_output=True, text=True
    )
    if check and result.returncode != 0:
        print(f"  FAILED: {cmd}")
        print(f"  stderr: {result.stderr[-300:]}")
        sys.exit(1)
    return result


def main():
    dry = "--dry-run" in sys.argv
    skip_collect = "--skip-collect" in sys.argv

    print(f"[{datetime.now():%Y-%m-%d %H:%M}] publish_daily start")
    if dry:
        print("  DRY RUN — no git push")

    # 1. Regenerate dashboard
    print("1. Regenerating dashboard...")
    run("python3 html_report.py", cwd=GAME_MONITOR)
    print("   done")

    # 2. Copy files to skillworks-site
    print("2. Copying files...")
    PUBLIC_DIR.mkdir(parents=True, exist_ok=True)

    # Dashboard
    src_dashboard = GAME_MONITOR / "data" / "dashboard.html"
    dst_dashboard = PUBLIC_DIR / "dashboard.html"
    shutil.copy2(src_dashboard, dst_dashboard)
    print(f"   {src_dashboard} → {dst_dashboard}")

    # Storyboard (from whichever source is more recent)
    src_storyboard_a = AD_MONITOR / "data" / "storyboard.html"
    src_storyboard_g = GAME_MONITOR / "data" / "storyboard.html"
    src_storyboard = None
    if src_storyboard_a.exists() and src_storyboard_g.exists():
        src_storyboard = (src_storyboard_a
            if src_storyboard_a.stat().st_mtime > src_storyboard_g.stat().st_mtime
            else src_storyboard_g)
    elif src_storyboard_a.exists():
        src_storyboard = src_storyboard_a
    elif src_storyboard_g.exists():
        src_storyboard = src_storyboard_g

    if src_storyboard:
        dst_storyboard = PUBLIC_DIR / "storyboard.html"
        shutil.copy2(src_storyboard, dst_storyboard)
        # Fix any leftover file:// links
        content = dst_storyboard.read_text()
        if "file://" in content:
            content = content.replace(
                'href="file:///Users/wan/projects/game-monitor/data/dashboard.html"',
                'href="dashboard.html"'
            )
            dst_storyboard.write_text(content)
            print(f"   fixed file:// link in storyboard.html")
        print(f"   {src_storyboard} → {dst_storyboard}")
    else:
        print("   storyboard.html not found, skipping")

    # 3. Ensure index.html exists (meta-refresh redirect)
    index_file = PUBLIC_DIR / "index.html"
    if not index_file.exists():
        index_file.write_text(
            '<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta http-equiv="refresh" content="0;url=dashboard.html">'
            '<title>Game Market Daily</title></head>'
            '<body><p><a href="dashboard.html">🎮 游戏市场日报</a></p></body></html>\n'
        )
        print("   created index.html")

    # 4. Git commit and push
    if dry:
        run("git status --short", cwd=SITEWORKS)
        run("git diff --stat", cwd=SITEWORKS)
        print("   DRY RUN — skipping commit+push")
        return

    print("3. Git commit + push...")
    today = datetime.now().strftime("%Y-%m-%d")
    run(f"git add public/game-market-daily/", cwd=SITEWORKS)

    # Only commit if there are changes
    status = run("git status --porcelain -- public/game-market-daily/",
                 cwd=SITEWORKS, check=False)
    if not status.stdout.strip():
        print("   no changes, skipping commit")
        return

    run(
        f'git commit -m "Update game market daily {today}"',
        cwd=SITEWORKS
    )
    run("git push origin main", cwd=SITEWORKS)
    print("   pushed ✓")

    print(f"[{datetime.now():%Y-%m-%d %H:%M}] publish_daily done")


if __name__ == "__main__":
    main()

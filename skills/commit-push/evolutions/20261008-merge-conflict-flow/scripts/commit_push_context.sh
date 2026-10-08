#!/usr/bin/env bash
# Read-only git context summarizer for the commit-push skill.
# It never runs add/commit/push/reset or any other write operation.
set -euo pipefail

mode="summary"
max_lines=40
full=0

usage() {
  cat <<'EOF'
Usage: commit_push_context.sh [--summary|--push|--stat|--conflicts] [--max-lines N] [--full]

Modes:
  --summary    Compact repository, branch, operation and change summary (default).
  --push       Summary plus commits on HEAD that are not on the upstream.
  --stat       Summary plus `git diff HEAD --stat` for large changes.
  --conflicts  Summary plus unmerged files and conflict-hunk summaries.

Options:
  --max-lines N  Max lines printed from each side of a conflict (default: 40).
  --full         Do not truncate conflict sides.
  --help         Show this help.

The script only reads git state. It does not stage, commit, push, reset or edit files.
EOF
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --summary) mode="summary" ;;
    --push) mode="push" ;;
    --stat) mode="stat" ;;
    --conflicts) mode="conflicts" ;;
    --max-lines)
      shift
      if [ "$#" -eq 0 ] || ! printf '%s' "$1" | grep -Eq '^[0-9]+$'; then
        echo "error: --max-lines requires a non-negative integer" >&2
        exit 2
      fi
      max_lines="$1"
      ;;
    --full) full=1 ;;
    --help|-h) usage; exit 0 ;;
    *)
      echo "error: unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
  shift
done

if ! git rev-parse --show-toplevel >/dev/null 2>&1; then
  echo "error: not inside a git repository" >&2
  exit 1
fi

repo="$(git rev-parse --show-toplevel)"
cd "$repo"

branch="$(git branch --show-current 2>/dev/null || true)"
[ -n "$branch" ] || branch="(detached HEAD)"
upstream="$(git rev-parse --abbrev-ref --symbolic-full-name '@{u}' 2>/dev/null || true)"
ahead=0
behind=0
if [ -n "$upstream" ]; then
  counts="$(git rev-list --left-right --count HEAD...@{u} 2>/dev/null || true)"
  if [ -n "$counts" ]; then
    ahead="${counts%%[[:space:]]*}"
    behind="${counts##*[[:space:]]}"
  fi
fi

operation="none"
if git rev-parse -q --verify MERGE_HEAD >/dev/null 2>&1; then
  operation="merge"
elif [ -d "$(git rev-parse --git-path rebase-merge)" ] || [ -d "$(git rev-parse --git-path rebase-apply)" ]; then
  operation="rebase"
elif git rev-parse -q --verify CHERRY_PICK_HEAD >/dev/null 2>&1; then
  operation="cherry-pick"
elif git rev-parse -q --verify REVERT_HEAD >/dev/null 2>&1; then
  operation="revert"
fi

staged=0
unstaged=0
untracked=0
unmerged=0
while IFS= read -r line; do
  case "$line" in
    '1 '*|'2 '*)
      xy="${line:2:2}"
      [ "${xy:0:1}" != "." ] && staged=$((staged + 1))
      [ "${xy:1:1}" != "." ] && unstaged=$((unstaged + 1))
      ;;
    'u '*) unmerged=$((unmerged + 1)) ;;
    '? '*) untracked=$((untracked + 1)) ;;
  esac
done < <(git status --porcelain=v2)

unmerged_paths="$(git diff --name-only --diff-filter=U)"
untracked_paths="$(git ls-files --others --exclude-standard)"

print_paths() {
  title="$1"
  data="$2"
  limit=50
  if [ -z "$data" ]; then
    echo "$title: 0"
    return
  fi
  total="$(printf '%s\n' "$data" | wc -l | tr -d ' ')"
  echo "$title: $total"
  i=0
  printf '%s\n' "$data" | while IFS= read -r path; do
    [ -n "$path" ] || continue
    i=$((i + 1))
    if [ "$i" -le "$limit" ]; then
      echo "  $path"
    fi
  done
  if [ "$total" -gt "$limit" ]; then
    echo "  ... +$((total - limit)) more"
  fi
}

echo "== git context =="
echo "repo: $repo"
echo "branch: $branch"
echo "upstream: ${upstream:-<none>}"
echo "ahead: $ahead behind: $behind"
echo "operation: $operation"
echo "changes: staged=$staged unstaged=$unstaged untracked=$untracked conflicts=$unmerged"
print_paths "unmerged" "$unmerged_paths"

case "$mode" in
  summary)
    ;;
  push)
    echo "== unpushed commits =="
    if [ -n "$upstream" ]; then
      git log --oneline --decorate "$upstream..HEAD" || true
    else
      echo "(no upstream; cannot compute unpushed commits)"
    fi
    ;;
  stat)
    echo "== diffstat (HEAD) =="
    if git diff --quiet HEAD -- 2>/dev/null; then
      echo "(no tracked changes)"
    else
      git diff HEAD --stat
    fi
    ;;
  conflicts)
    echo "== conflicts =="
    if [ -z "$unmerged_paths" ]; then
      echo "(none)"
      exit 0
    fi
    if [ "$full" -eq 1 ]; then
      max_lines=0
    fi
    printf '%s\n' "$unmerged_paths" | while IFS= read -r file; do
      [ -n "$file" ] || continue
      count="$(grep -c '^<<<<<<<' "$file" 2>/dev/null || true)"
      echo "file: $file"
      echo "  conflicts: ${count:-0}"
      awk -v max="$max_lines" '
        function flush() {
          if (inblock && truncated) {
            print "    ... (truncated; use --full)"
          }
          inblock = 0
          ours = 0
          theirs = 0
          truncated = 0
        }
        /^<<<<<<< / {
          flush()
          inblock = 1
          side = "ours"
          n++
          print "  conflict " n " @ line " NR
          next
        }
        /^=======$/ { side = "theirs"; next }
        /^>>>>>>> / { flush(); next }
        inblock && side == "ours" {
          ours++
          if (max == 0 || ours <= max) print "    - " $0
          else truncated = 1
          next
        }
        inblock && side == "theirs" {
          theirs++
          if (max == 0 || theirs <= max) print "    + " $0
          else truncated = 1
          next
        }
        END { flush() }
      ' "$file"
    done
    ;;
esac

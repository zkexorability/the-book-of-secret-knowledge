# 🔧 Git Cheatsheet

Essential Git commands every developer should know.

## 📋 Basic Commands

### Repository Setup
```bash
# Initialize a new repository
git init

# Clone a repository
git clone <url>

# Add remote origin
git remote add origin <url>

# View remotes
git remote -v
```

### Basic Workflow
```bash
# Check status
git status

# Add files to staging
git add <file>
git add .                    # Add all files
git add -A                   # Add all files including deleted

# Commit changes
git commit -m "message"
git commit -am "message"     # Add and commit in one step

# Push changes
git push
git push origin <branch>
git push -u origin <branch>  # Set upstream and push
```

## 🌿 Branching

### Branch Management
```bash
# List branches
git branch                   # Local branches
git branch -r               # Remote branches
git branch -a               # All branches

# Create and switch to new branch
git checkout -b <branch-name>
git switch -c <branch-name>  # Modern alternative

# Switch branches
git checkout <branch-name>
git switch <branch-name>     # Modern alternative

# Delete branch
git branch -d <branch-name>  # Safe delete (merged only)
git branch -D <branch-name>  # Force delete

# Delete remote branch
git push origin --delete <branch-name>
```

### Branch Operations
```bash
# Merge branch
git checkout main
git merge <branch-name>

# Rebase branch
git checkout <feature-branch>
git rebase main

# Cherry-pick commit
git cherry-pick <commit-hash>
```

## 📝 Commit History

### Viewing History
```bash
# View commit history
git log
git log --oneline           # Compact view
git log --graph            # Visual graph
git log --stat             # Show file changes
git log -p                 # Show diff

# View specific file history
git log <file>
git log --follow <file>    # Follow renames

# Search commits
git log --grep="<pattern>"
git log -S"<string>"       # Search for string in diff
```

### Commit Information
```bash
# Show commit details
git show <commit-hash>

# Show files changed in commit
git show --name-only <commit-hash>

# Compare commits
git diff <commit1>..<commit2>
```

## 🔄 Undoing Changes

### Working Directory
```bash
# Discard changes in working directory
git checkout -- <file>
git restore <file>          # Modern alternative

# Discard all changes
git checkout -- .
git restore .
```

### Staging Area
```bash
# Unstage file
git reset HEAD <file>
git restore --staged <file> # Modern alternative

# Unstage all files
git reset HEAD
```

### Commits
```bash
# Amend last commit
git commit --amend
git commit --amend -m "new message"

# Reset to previous commit (keep changes)
git reset --soft HEAD~1

# Reset to previous commit (discard changes)
git reset --hard HEAD~1

# Revert commit (create new commit)
git revert <commit-hash>
```

## 🔍 Inspection & Comparison

### File Status
```bash
# Show changes in working directory
git diff

# Show staged changes
git diff --staged
git diff --cached

# Show changes between branches
git diff <branch1>..<branch2>

# Show changes for specific file
git diff <file>
```

### Blame & History
```bash
# Show who changed each line
git blame <file>

# Show file at specific commit
git show <commit>:<file>

# Find when bug was introduced
git bisect start
git bisect bad <commit>
git bisect good <commit>
```

## 🏷️ Tags

### Tag Management
```bash
# List tags
git tag

# Create tag
git tag <tag-name>
git tag -a <tag-name> -m "message"  # Annotated tag

# Push tags
git push origin <tag-name>
git push origin --tags              # Push all tags

# Delete tag
git tag -d <tag-name>               # Local
git push origin --delete <tag-name> # Remote
```

## 🔧 Configuration

### User Settings
```bash
# Set user info
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# View configuration
git config --list
git config user.name

# Set default branch
git config --global init.defaultBranch main
```

### Aliases
```bash
# Create aliases
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.unstage 'reset HEAD --'
git config --global alias.last 'log -1 HEAD'
git config --global alias.visual '!gitk'
```

## 🚀 Advanced Commands

### Stashing
```bash
# Stash changes
git stash
git stash push -m "message"

# List stashes
git stash list

# Apply stash
git stash apply
git stash apply stash@{0}

# Pop stash (apply and remove)
git stash pop

# Drop stash
git stash drop stash@{0}

# Clear all stashes
git stash clear
```

### Submodules
```bash
# Add submodule
git submodule add <url> <path>

# Initialize submodules
git submodule init
git submodule update

# Update submodules
git submodule update --remote

# Clone with submodules
git clone --recursive <url>
```

### Worktrees
```bash
# Create worktree
git worktree add <path> <branch>

# List worktrees
git worktree list

# Remove worktree
git worktree remove <path>
```

## 🛠️ Useful One-Liners

```bash
# Delete all merged branches
git branch --merged | grep -v "\*\|master\|main" | xargs -n 1 git branch -d

# Update all branches
git branch -r | grep -v '\->' | while read remote; do git branch --track "${remote#origin/}" "$remote"; done
git fetch --all
git pull --all

# Find large files in history
git rev-list --objects --all | git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' | sed -n 's/^blob //p' | sort --numeric-sort --key=2 | tail -10

# Remove file from history
git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch <file>' --prune-empty --tag-name-filter cat -- --all

# Count commits by author
git shortlog -sn

# Show commits in date range
git log --since="2023-01-01" --until="2023-12-31" --oneline

# Find commits that changed a specific line
git log -L <start>,<end>:<file>

# Show branches that contain a commit
git branch --contains <commit-hash>
```

## 🚨 Emergency Commands

```bash
# Recover deleted branch
git reflog
git checkout -b <branch-name> <commit-hash>

# Recover lost commits
git fsck --lost-found

# Abort merge
git merge --abort

# Abort rebase
git rebase --abort

# Force push (use with caution!)
git push --force-with-lease

# Clean untracked files
git clean -fd              # Remove files and directories
git clean -fX              # Remove only ignored files
```

## 📚 Best Practices

1. **Commit Messages**: Use clear, descriptive commit messages
2. **Branch Naming**: Use descriptive branch names (feature/user-auth, bugfix/login-error)
3. **Small Commits**: Make small, focused commits
4. **Pull Before Push**: Always pull before pushing to avoid conflicts
5. **Review Changes**: Use `git diff` before committing
6. **Backup**: Push regularly to avoid losing work
7. **Clean History**: Use interactive rebase to clean up commit history before merging

## 🔗 Useful Resources

- [Git Documentation](https://git-scm.com/doc)
- [Pro Git Book](https://git-scm.com/book)
- [Git Cheat Sheet (PDF)](https://education.github.com/git-cheat-sheet-education.pdf)
- [Interactive Git Tutorial](https://learngitbranching.js.org/)
- [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/)

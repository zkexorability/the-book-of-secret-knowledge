#!/usr/bin/env python3
"""
🚀 Developer Productivity Utilities
A collection of useful Python utilities for developers
"""

import os
import sys
import json
import subprocess
import argparse
import requests
from pathlib import Path
from datetime import datetime
import hashlib
import re


class Colors:
    """ANSI color codes for terminal output"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def print_colored(text, color=Colors.WHITE):
    """Print colored text to terminal"""
    print(f"{color}{text}{Colors.END}")


def print_header(text):
    """Print a formatted header"""
    print_colored(f"\n{'='*50}", Colors.CYAN)
    print_colored(f"{text.center(50)}", Colors.BOLD + Colors.CYAN)
    print_colored(f"{'='*50}", Colors.CYAN)


class ProjectAnalyzer:
    """Analyze project structure and provide insights"""
    
    def __init__(self, path="."):
        self.path = Path(path)
        self.stats = {}
    
    def analyze(self):
        """Analyze the project directory"""
        print_header("PROJECT ANALYSIS")
        
        # Count files by extension
        file_counts = {}
        total_files = 0
        total_size = 0
        
        for file_path in self.path.rglob("*"):
            if file_path.is_file() and not self._should_ignore(file_path):
                ext = file_path.suffix.lower() or "no_extension"
                file_counts[ext] = file_counts.get(ext, 0) + 1
                total_files += 1
                total_size += file_path.stat().st_size
        
        # Display results
        print_colored(f"📁 Project Path: {self.path.absolute()}", Colors.BLUE)
        print_colored(f"📊 Total Files: {total_files}", Colors.GREEN)
        print_colored(f"💾 Total Size: {self._format_size(total_size)}", Colors.GREEN)
        
        print_colored("\n📋 File Types:", Colors.YELLOW)
        for ext, count in sorted(file_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
            percentage = (count / total_files) * 100
            print(f"  {ext:15} {count:6} files ({percentage:5.1f}%)")
        
        # Detect project type
        self._detect_project_type()
        
        return {
            "total_files": total_files,
            "total_size": total_size,
            "file_counts": file_counts
        }
    
    def _should_ignore(self, path):
        """Check if path should be ignored"""
        ignore_patterns = [
            ".git", "node_modules", "__pycache__", ".venv", "venv",
            ".DS_Store", "*.pyc", "*.pyo", "*.pyd", ".pytest_cache"
        ]
        
        path_str = str(path)
        for pattern in ignore_patterns:
            if pattern in path_str:
                return True
        return False
    
    def _format_size(self, size_bytes):
        """Format file size in human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"
    
    def _detect_project_type(self):
        """Detect the type of project"""
        print_colored("\n🔍 Project Type Detection:", Colors.PURPLE)
        
        detections = []
        
        # Check for common project files
        project_indicators = {
            "package.json": "Node.js/JavaScript",
            "requirements.txt": "Python",
            "Pipfile": "Python (Pipenv)",
            "pyproject.toml": "Python (Poetry/Modern)",
            "Cargo.toml": "Rust",
            "go.mod": "Go",
            "pom.xml": "Java (Maven)",
            "build.gradle": "Java/Kotlin (Gradle)",
            "composer.json": "PHP",
            "Gemfile": "Ruby",
            "Dockerfile": "Docker",
            "docker-compose.yml": "Docker Compose",
            ".gitignore": "Git Repository"
        }
        
        for file_name, project_type in project_indicators.items():
            if (self.path / file_name).exists():
                detections.append(project_type)
        
        if detections:
            for detection in detections:
                print(f"  ✅ {detection}")
        else:
            print("  ❓ Unknown project type")


class GitHelper:
    """Git repository helper utilities"""
    
    @staticmethod
    def get_repo_info():
        """Get current repository information"""
        try:
            # Get current branch
            branch = subprocess.check_output(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                stderr=subprocess.DEVNULL
            ).decode().strip()
            
            # Get remote URL
            remote_url = subprocess.check_output(
                ["git", "config", "--get", "remote.origin.url"],
                stderr=subprocess.DEVNULL
            ).decode().strip()
            
            # Get last commit
            last_commit = subprocess.check_output(
                ["git", "log", "-1", "--pretty=format:%h - %s (%cr)"],
                stderr=subprocess.DEVNULL
            ).decode().strip()
            
            return {
                "branch": branch,
                "remote_url": remote_url,
                "last_commit": last_commit
            }
        except subprocess.CalledProcessError:
            return None
    
    @staticmethod
    def clean_branches():
        """Clean up merged branches"""
        print_header("GIT BRANCH CLEANUP")
        
        try:
            # Get merged branches
            merged_branches = subprocess.check_output(
                ["git", "branch", "--merged"],
                stderr=subprocess.DEVNULL
            ).decode().strip().split('\n')
            
            # Filter out current branch and main/master
            branches_to_delete = []
            for branch in merged_branches:
                branch = branch.strip().replace('*', '').strip()
                if branch and branch not in ['main', 'master', 'develop']:
                    branches_to_delete.append(branch)
            
            if branches_to_delete:
                print_colored(f"Found {len(branches_to_delete)} merged branches to clean up:", Colors.YELLOW)
                for branch in branches_to_delete:
                    print(f"  - {branch}")
                
                confirm = input("\nDelete these branches? (y/N): ")
                if confirm.lower() == 'y':
                    for branch in branches_to_delete:
                        subprocess.run(["git", "branch", "-d", branch])
                    print_colored("✅ Branches cleaned up!", Colors.GREEN)
                else:
                    print_colored("❌ Cleanup cancelled", Colors.YELLOW)
            else:
                print_colored("✅ No merged branches to clean up", Colors.GREEN)
                
        except subprocess.CalledProcessError:
            print_colored("❌ Not a git repository or git not available", Colors.RED)


class CodeFormatter:
    """Code formatting utilities"""
    
    @staticmethod
    def format_json_file(file_path):
        """Format a JSON file"""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2, sort_keys=True)
            
            print_colored(f"✅ Formatted {file_path}", Colors.GREEN)
            return True
        except Exception as e:
            print_colored(f"❌ Error formatting {file_path}: {e}", Colors.RED)
            return False
    
    @staticmethod
    def format_all_json():
        """Format all JSON files in current directory"""
        print_header("JSON FORMATTER")
        
        json_files = list(Path(".").rglob("*.json"))
        if not json_files:
            print_colored("No JSON files found", Colors.YELLOW)
            return
        
        print_colored(f"Found {len(json_files)} JSON files", Colors.BLUE)
        
        success_count = 0
        for json_file in json_files:
            if CodeFormatter.format_json_file(json_file):
                success_count += 1
        
        print_colored(f"\n✅ Successfully formatted {success_count}/{len(json_files)} files", Colors.GREEN)


class SecurityScanner:
    """Basic security scanning utilities"""
    
    @staticmethod
    def scan_for_secrets():
        """Scan for potential secrets in code"""
        print_header("SECURITY SCAN")
        
        # Common secret patterns
        patterns = {
            "API Key": r"api[_-]?key['\"\s]*[:=]['\"\s]*[a-zA-Z0-9]{20,}",
            "Password": r"password['\"\s]*[:=]['\"\s]*['\"][^'\"]{8,}['\"]",
            "Token": r"token['\"\s]*[:=]['\"\s]*[a-zA-Z0-9]{20,}",
            "Secret": r"secret['\"\s]*[:=]['\"\s]*[a-zA-Z0-9]{20,}",
            "Private Key": r"-----BEGIN [A-Z ]+PRIVATE KEY-----"
        }
        
        findings = []
        
        for file_path in Path(".").rglob("*"):
            if file_path.is_file() and file_path.suffix in ['.py', '.js', '.ts', '.json', '.yaml', '.yml', '.env']:
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        
                    for secret_type, pattern in patterns.items():
                        matches = re.finditer(pattern, content, re.IGNORECASE)
                        for match in matches:
                            line_num = content[:match.start()].count('\n') + 1
                            findings.append({
                                "file": str(file_path),
                                "line": line_num,
                                "type": secret_type,
                                "match": match.group()[:50] + "..." if len(match.group()) > 50 else match.group()
                            })
                except Exception:
                    continue
        
        if findings:
            print_colored(f"⚠️  Found {len(findings)} potential security issues:", Colors.RED)
            for finding in findings:
                print(f"  {finding['file']}:{finding['line']} - {finding['type']}")
                print(f"    {finding['match']}")
        else:
            print_colored("✅ No obvious security issues found", Colors.GREEN)


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Developer Productivity Utilities")
    parser.add_argument("command", choices=[
        "analyze", "git-info", "git-clean", "format-json", "security-scan", "all"
    ], help="Command to run")
    parser.add_argument("--path", default=".", help="Path to analyze (default: current directory)")
    
    args = parser.parse_args()
    
    print_colored("🚀 Developer Productivity Utilities", Colors.BOLD + Colors.CYAN)
    print_colored(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", Colors.BLUE)
    
    if args.command == "analyze" or args.command == "all":
        analyzer = ProjectAnalyzer(args.path)
        analyzer.analyze()
    
    if args.command == "git-info" or args.command == "all":
        print_header("GIT REPOSITORY INFO")
        repo_info = GitHelper.get_repo_info()
        if repo_info:
            print_colored(f"🌿 Branch: {repo_info['branch']}", Colors.GREEN)
            print_colored(f"🔗 Remote: {repo_info['remote_url']}", Colors.BLUE)
            print_colored(f"📝 Last Commit: {repo_info['last_commit']}", Colors.YELLOW)
        else:
            print_colored("❌ Not a git repository", Colors.RED)
    
    if args.command == "git-clean":
        GitHelper.clean_branches()
    
    if args.command == "format-json":
        CodeFormatter.format_all_json()
    
    if args.command == "security-scan" or args.command == "all":
        SecurityScanner.scan_for_secrets()
    
    print_colored("\n✨ Done!", Colors.GREEN)


if __name__ == "__main__":
    main()

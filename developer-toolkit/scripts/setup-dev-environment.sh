#!/bin/bash

# 🚀 Ultimate Developer Environment Setup Script
# This script sets up a complete development environment with essential tools

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Install package managers
install_package_managers() {
    log_info "Installing package managers..."
    
    # Homebrew (macOS/Linux)
    if [[ "$OSTYPE" == "darwin"* ]] || [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if ! command_exists brew; then
            log_info "Installing Homebrew..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            log_success "Homebrew installed"
        else
            log_success "Homebrew already installed"
        fi
    fi
    
    # Node Version Manager
    if ! command_exists nvm; then
        log_info "Installing NVM..."
        curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
        export NVM_DIR="$HOME/.nvm"
        [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
        log_success "NVM installed"
    else
        log_success "NVM already installed"
    fi
    
    # Python Version Manager
    if ! command_exists pyenv; then
        log_info "Installing pyenv..."
        curl https://pyenv.run | bash
        log_success "pyenv installed"
    else
        log_success "pyenv already installed"
    fi
}

# Install development tools
install_dev_tools() {
    log_info "Installing development tools..."
    
    # Git
    if ! command_exists git; then
        if [[ "$OSTYPE" == "darwin"* ]]; then
            brew install git
        elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
            sudo apt-get update && sudo apt-get install -y git
        fi
        log_success "Git installed"
    else
        log_success "Git already installed"
    fi
    
    # GitHub CLI
    if ! command_exists gh; then
        if [[ "$OSTYPE" == "darwin"* ]]; then
            brew install gh
        elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
            curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
            echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
            sudo apt update && sudo apt install gh
        fi
        log_success "GitHub CLI installed"
    else
        log_success "GitHub CLI already installed"
    fi
    
    # Docker
    if ! command_exists docker; then
        log_info "Installing Docker..."
        if [[ "$OSTYPE" == "darwin"* ]]; then
            brew install --cask docker
        elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
            curl -fsSL https://get.docker.com -o get-docker.sh
            sudo sh get-docker.sh
            sudo usermod -aG docker $USER
            rm get-docker.sh
        fi
        log_success "Docker installed"
    else
        log_success "Docker already installed"
    fi
}

# Install programming languages
install_languages() {
    log_info "Installing programming languages..."
    
    # Node.js
    if command_exists nvm; then
        log_info "Installing Node.js LTS..."
        nvm install --lts
        nvm use --lts
        log_success "Node.js LTS installed"
        
        # Install global npm packages
        npm install -g yarn pnpm typescript eslint prettier
        log_success "Global npm packages installed"
    fi
    
    # Python
    if command_exists pyenv; then
        log_info "Installing Python 3.11..."
        pyenv install 3.11.0
        pyenv global 3.11.0
        log_success "Python 3.11 installed"
        
        # Install Python package managers
        pip install --upgrade pip pipenv poetry
        log_success "Python package managers installed"
    fi
    
    # Rust
    if ! command_exists rustc; then
        log_info "Installing Rust..."
        curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
        source $HOME/.cargo/env
        log_success "Rust installed"
    else
        log_success "Rust already installed"
    fi
    
    # Go
    if ! command_exists go; then
        if [[ "$OSTYPE" == "darwin"* ]]; then
            brew install go
        elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
            wget https://go.dev/dl/go1.21.0.linux-amd64.tar.gz
            sudo rm -rf /usr/local/go && sudo tar -C /usr/local -xzf go1.21.0.linux-amd64.tar.gz
            echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc
            rm go1.21.0.linux-amd64.tar.gz
        fi
        log_success "Go installed"
    else
        log_success "Go already installed"
    fi
}

# Install terminal tools
install_terminal_tools() {
    log_info "Installing terminal tools..."
    
    # Oh My Zsh
    if [ ! -d "$HOME/.oh-my-zsh" ]; then
        log_info "Installing Oh My Zsh..."
        sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended
        log_success "Oh My Zsh installed"
    else
        log_success "Oh My Zsh already installed"
    fi
    
    # Starship prompt
    if ! command_exists starship; then
        log_info "Installing Starship..."
        curl -sS https://starship.rs/install.sh | sh -s -- -y
        echo 'eval "$(starship init zsh)"' >> ~/.zshrc
        log_success "Starship installed"
    else
        log_success "Starship already installed"
    fi
    
    # Modern CLI tools
    if [[ "$OSTYPE" == "darwin"* ]]; then
        brew install bat exa fd ripgrep fzf htop
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt-get install -y bat exa fd-find ripgrep fzf htop
    fi
    log_success "Modern CLI tools installed"
}

# Install VS Code extensions
install_vscode_extensions() {
    if command_exists code; then
        log_info "Installing VS Code extensions..."
        
        extensions=(
            "ms-python.python"
            "ms-vscode.vscode-typescript-next"
            "bradlc.vscode-tailwindcss"
            "esbenp.prettier-vscode"
            "ms-vscode.vscode-eslint"
            "ms-vscode.vscode-json"
            "redhat.vscode-yaml"
            "ms-vscode.vscode-docker"
            "GitLab.gitlab-workflow"
            "ms-vscode.vscode-git-graph"
            "formulahendry.auto-rename-tag"
            "christian-kohler.path-intellisense"
            "ms-vscode.vscode-thunder-client"
        )
        
        for extension in "${extensions[@]}"; do
            code --install-extension "$extension" --force
        done
        
        log_success "VS Code extensions installed"
    else
        log_warning "VS Code not found, skipping extensions"
    fi
}

# Configure Git
configure_git() {
    log_info "Configuring Git..."
    
    read -p "Enter your Git username: " git_username
    read -p "Enter your Git email: " git_email
    
    git config --global user.name "$git_username"
    git config --global user.email "$git_email"
    git config --global init.defaultBranch main
    git config --global pull.rebase false
    
    log_success "Git configured"
}

# Main installation function
main() {
    log_info "🚀 Starting Ultimate Developer Environment Setup"
    log_info "This script will install essential development tools and configure your environment"
    
    # Check OS
    log_info "Detected OS: $OSTYPE"
    
    # Install components
    install_package_managers
    install_dev_tools
    install_languages
    install_terminal_tools
    install_vscode_extensions
    configure_git
    
    log_success "🎉 Developer environment setup complete!"
    log_info "Please restart your terminal or run 'source ~/.zshrc' to apply changes"
    log_info "You may need to log out and back in for some changes to take effect"
}

# Run main function
main "$@"

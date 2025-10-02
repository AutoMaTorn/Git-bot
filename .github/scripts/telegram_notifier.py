name: Daily Auto Commit

on:
  schedule:
    - cron: '0 12 * * *'
  workflow_dispatch:

jobs:
  auto-commit:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    
    steps:
    - name: Checkout repository
      uses: actions/checkout@v4
      with:
        token: ${{ secrets.GITHUB_TOKEN }}
        fetch-depth: 0
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install requests
    
    - name: Run commit bot
      run: |
        python .github/scripts/commit_bot.py
    
    - name: Commit and push changes
      run: |
        git config --local user.email "github-actions[bot]@users.noreply.github.com"
        git config --local user.name "github-actions[bot]"
        
        git add .
        
        # Коммитим только если есть изменения
        if git diff --staged --quiet; then
          echo "✅ No changes to commit"
        else
          git commit -m "🤖 Auto-commit: $(date -u +'%Y-%m-%d %H:%M:%S UTC')"
          git push
          echo "✅ Changes committed and pushed"
        fi
    
    - name: Simple success message
      run: echo "🎉 Workflow completed successfully!"
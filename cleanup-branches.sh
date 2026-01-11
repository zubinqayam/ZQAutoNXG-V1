#!/bin/bash
# ZQAutoNXG-V1 Branch Cleanup Script
# Generated: 2026-01-11
# Purpose: Delete outdated and destructive branches from remote

set -e

echo "🧹 ZQAutoNXG-V1 Branch Cleanup Script"
echo "========================================"
echo ""
echo "This script will delete 25 branches from the remote repository."
echo "The following branches will be KEPT:"
echo "  1. main (protected)"
echo "  2. copilot/review-and-merge-branches (current PR)"
echo "  3. copilot/add-feature-from-repo (frontend addition)"
echo "  4. fix-cors-whitespace (has fixes)"
echo "  5. vercel/enable-vercel-speed-insights-i-re8ops (analytics)"
echo ""
echo "⚠️  WARNING: This action cannot be undone!"
echo ""

read -p "Do you want to proceed? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "❌ Cleanup cancelled."
    exit 0
fi

echo ""
echo "🗑️  Deleting branches..."
echo ""

# Counter
deleted=0
failed=0

# Function to delete a branch
delete_branch() {
    local branch=$1
    echo -n "Deleting $branch... "
    if git push origin --delete "$branch" 2>/dev/null; then
        echo "✅ Deleted"
        ((deleted++))
    else
        echo "❌ Failed (may not exist or no permission)"
        ((failed++))
    fi
}

# Category 1: Already Merged (3 branches)
echo "📦 Category 1: Already Merged Branches"
delete_branch "copilot/add-new-feature-implementation"
delete_branch "copilot/fix-github-actions-cache-error"
delete_branch "copilot/update-checks-status-response"
echo ""

# Category 2: Destructive "Bolt" Branches (14 branches)
echo "⚠️  Category 2: Destructive 'Bolt' Branches"
delete_branch "bolt/async-endpoints-optimization-3832087936365419913"
delete_branch "bolt-async-endpoints-1604690059097381405"
delete_branch "bolt-async-endpoints-3059472604653003645"
delete_branch "bolt-async-endpoints-4530341808122708846"
delete_branch "bolt-async-endpoints-8913473747712539192"
delete_branch "bolt-gzip-compression-8783984052347987712"
delete_branch "bolt-optimize-endpoints-3851131301620202090"
delete_branch "bolt-optimize-root-endpoint-12549690232185960117"
delete_branch "bolt-optimize-root-endpoint-9250567379554527185"
delete_branch "bolt-optimize-status-endpoint-13714227936700589219"
delete_branch "bolt-perf-opt-root-10327503609263953491"
delete_branch "bolt-perf-root-optimization-9195975302337934528"
delete_branch "bolt-response-optimization-4027168571882894165"
delete_branch "bolt-root-endpoint-optimization-4312827992691060435"
echo ""

# Category 3: Destructive/Outdated Copilot Branches (4 branches)
echo "🔄 Category 3: Outdated Copilot Branches"
delete_branch "copilot/sub-pr-8"
delete_branch "copilot/fix-issue-with-login-module"
delete_branch "copilot/fix-issue-with-user-login"
delete_branch "copilot/fixworkflow-lowercase-image"
echo ""

# Category 4: Experimental/Duplicate Branches (4 branches)
echo "🧪 Category 4: Experimental/Duplicate Branches"
delete_branch "evolve-product-architecture-8549057981400434527"
delete_branch "vercel/enable-vercel-speed-insights-o-z8wtny"
delete_branch "vercel/set-up-vercel-web-analytics-in-k1nso1"
echo ""

# Summary
echo "========================================"
echo "✨ Cleanup Complete!"
echo ""
echo "📊 Summary:"
echo "  ✅ Successfully deleted: $deleted branches"
echo "  ❌ Failed to delete: $failed branches"
echo ""
echo "🎯 Remaining branches (5 total):"
git branch -r | grep -E "(main|copilot/review-and-merge-branches|copilot/add-feature-from-repo|fix-cors-whitespace|vercel/enable-vercel-speed-insights-i-re8ops)" | sed 's/origin\///' | sed 's/^/  - /'
echo ""
echo "✅ Repository cleaned up successfully!"
echo ""
echo "Next steps:"
echo "  1. Verify the remaining branches are correct"
echo "  2. Merge 'copilot/review-and-merge-branches' to main"
echo "  3. Review 'copilot/add-feature-from-repo' for frontend addition"
echo "  4. Consider final branch organization"
echo ""

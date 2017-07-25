#!/bin/sh

cd $(dirname "$0")

#if [[ $(git status -s) ]]
#then
#    echo "The working directory is dirty. Please commit any pending changes."
#    exit 1;
#fi

echo "Deleting old publication"
rm -rf public
mkdir public
git worktree prune
rm -rf .git/worktrees/public/

echo "Checking out gh-pages branch into public"
git worktree add -B gh-pages public hugo/gh-pages

echo "Removing existing files"
rm -rf public/*

echo "Generating site"
hugo

echo "Updating gh-pages branch and pushing"
cd public
git add --all
git commit -m "Publishing to gh-pages (publish.sh)"
git push

echo "Pushing any remaining commits to the master branch"
#cd ..
#git push
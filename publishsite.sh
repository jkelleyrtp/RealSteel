cd blog
hugo -d ../docs
cd ..
git add docs

msg="rebuilding site `date`"
if [ $# -eq 1 ]
  then msg="$1"
fi
git commit -m "$msg"

git push origin master
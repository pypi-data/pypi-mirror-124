#!/bin/sh
# This file is in the public domain.
# See README.
for fn in $REPO/philosophy/*.html $REPO/gnu/*.html
do

echo "Working on $fn"
bn=`basename $fn`
IFS=. read name lang ext <<EOF
${bn}
EOF
if test -z "$ext"
then
  ext="${lang}"
  lang="en"
fi
mkdir -p "${lang}"
cp "${fn}" ${lang}/${name}.${ext}

done

mkdir -p br zh
mv pt-br/* br/
mv zh-cn/* zh/
mv zh-tw/* zh/
rmdir pt-br zh-cn zh-tw

# remove menus
rm ??/*-menu.html
rm ??/latest-articles.html

# remove non-articles
rm ??/gnu-user-groups.html
rm ??/fs-translations.html

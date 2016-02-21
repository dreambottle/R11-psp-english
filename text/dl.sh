#!/bin/bash
TEXTDIR=www
mkdir -p $TEXTDIR

LIST=`wget 'http://tlwiki.org/index.php?title=Remember11_-_the_age_of_infinity' -O - |\
      perl -lne '/<b><a href="[^" ]+title=R11:((?:PR|CO|SA)[A-Z0-9_]+\.txt)/ and print $1'`
download_list () {
for i in $1 ; do
    wget 'http://tlwiki.org/index.php?title=R11:'$i -O - |\
    perl -p0e 'm#<pre>(.*)</pre>#s or die; $_=$1; %h=(nbsp=>" ", 160=>" ", quot=>"\"", lt=>"<", gt=>">"); s/\&#?([\d\w]+);/defined($h{$1})||die$&; $h{$1}/ge;' > $TEXTDIR/$i
done
}
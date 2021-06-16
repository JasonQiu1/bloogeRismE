#!/bin/bash
out=""
for f in $@ ;do
  out="$out\n$(cat $f | grep -Po "class='(.*?)'" \
  | grep -o "[^' ][-a-zA-Z0-9]*[^' ]" \
  | grep -v "class=")"
done
classSet=$(echo -e "${out:2}" | sort -u)
pattern=$(echo "$classSet" | awk '{ print "(?s)^\\." $1 " {.*?}" }')
cat ${@:(-2):1} > strippedBS.css
stripped=$(echo "$pattern" | pcre2grep -Mf /dev/fd/0 ${@:(-1)})
echo "$stripped" >> strippedBS.css


#!/bin/bash
./stripBSclasses.sh /home/jason/BlogSite/blog/templates/blog/*.html bshead.css bsbody.css
cat extra.css >> strippedBS.css
curl -X POST -s --data-urlencode 'input@strippedBS.css' https://cssminifier.com/raw > strippedBS.min.css

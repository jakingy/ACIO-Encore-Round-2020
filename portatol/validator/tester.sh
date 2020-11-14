for f in ../data/*.in; do
if ! ./sub3 < $f; then
break
else
	echo "$f pass"
fi
done

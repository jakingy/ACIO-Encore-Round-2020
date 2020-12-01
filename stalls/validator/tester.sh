for f in ../data/*.in; do
if ! ./sub5 < $f; then
break
else
	echo "$f pass"
fi
done

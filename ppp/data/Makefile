.PHONY: all clean input output check

all: input output check zip

input:
	# Put any data generation commands here
	python3 gen/gen-sub1.py
	python3 gen/gen-sub2.py
	python3 gen/gen-sub3.py
	python3 gen/gen-sub4.py
	python3 gen/gen-sub5.py
	python3 gen/maxcase.py
	cp handmade/* .

output: input
	bash ./make-output-py.sh

check: input

zip: input output check
	zip data.zip *.in *.out

clean:
	-rm *.in *.out
	-rm data.zip

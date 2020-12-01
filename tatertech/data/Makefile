.PHONY: all clean input output check

all: input output check zip

input:
	# Put any data generation commands here
	python3 gen/gen.py
	cp handmade/* .

output: input
	bash ./make-output-py.sh

check: input

zip: input output check
	zip data.zip *.in *.out

clean:
	-rm *.in *.out
	-rm data.zip

all: locations_resolved.gpx

locations_resolved.gpx: locations_resolved.csv
	python gengpx.py < $< > $@ || { rm -f $@; exit 1; }

locations_resolved.csv: locations_orig.csv
	python resolve_w3w.py < $< > $@ || { rm -f $@; exit 1; }

clean:
	rm -f locations_resolved.gpx locations_resolved.csv

P4C = p4c
CORE = pot-polka-core.p4
CORE-S1 = pot-polka-core-s1.p4
CORE-S2 = pot-polka-core-s2.p4
CORE-S3 = pot-polka-core-s3.p4
EDGE = pot-polka-edge.p4

all: build

build: edge
	${P4C} ${CORE}

edge:
	${P4C} ${EDGE}

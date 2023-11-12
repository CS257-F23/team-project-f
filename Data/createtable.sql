DROP TABLE IF EXISTS caseinfo;
CREATE TABLE caseinfo (
	usCite VARCHAR,
	sctCite VARCHAR,
	ledCite VARCHAR,
	lexisCite VARCHAR,
	caseName VARCHAR,
	dateDecision DATE,
	caseDisposition VARCHAR
);

DROP TABLE IF EXISTS voteinfo;
CREATE TABLE voteinfo (
	lexisCite VARCHAR,
	justiceName VARCHAR,
	vote CHAR
);
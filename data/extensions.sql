CREATE TABLE IF NOT EXISTS merged_districts AS
  SELECT
    l.identifier identifier,
    l.bwk bwk,
    l.geom geom,
    l.bezname bezname,
    l.spd + sum(u.spd) spd,
    l.cdu + sum(u.cdu) cdu,
    l.gruene + sum(u.gruene) gruene,
    l.fdp + sum(u.fdp) fdp,
    l.die_linke + sum(u.die_linke) die_linke,
    l.afd + sum(u.afd) afd
  FROM
    letter_districts l
  INNER JOIN
    urn_districts u
  ON
    ST_Contains(l.geom, u.geom)
    OR
      (l.identifier = '024B' and u.identifier in ('02403', '02402'))
    OR
      (l.identifier = '038D' and u.identifier = '03807')
    OR
      (l.identifier = '039I' and u.identifier = '03919')
    OR
      (l.identifier = '114H' and u.identifier = '11422')
  GROUP BY
    l.identifier;


CREATE TABLE IF NOT EXISTS diffs (
  identifier varchar(20) primary key,
  bwk varchar(20)
);

DROP VIEW IF EXISTS counties_diff;
DROP VIEW IF EXISTS merged_districts_diff;

CREATE VIEW merged_districts_diff AS
  SELECT
    m.identifier identifier,
    CASE WHEN d.bwk is NULL THEN m.bwk ELSE d.bwk END bwk,
    m.geom geom,
    m.bezname bezname,
    m.spd spd,
    m.cdu cdu,
    m.gruene gruene,
    m.fdp fdp,
    m.die_linke die_linke,
    m.afd afd
  FROM
    merged_districts m
  LEFT OUTER JOIN
    diffs d
  ON
    m.identifier = d.identifier;

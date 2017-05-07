drop table if exists parsedPdfs;
create table parsedPdfs (
  Heading text null,
  Body text null,
  FileName text null,
  Commodity text null,
  Continent text null,
  Date date,
  DateFetched datetime
);
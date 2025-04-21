CREATE TABLE IF NOT EXISTS "fact_air_quality" (
  "parameter_id" integer,
  "location_id" integer,
  "sensor_id" integer,
  "value" float,
  "created_at" timestamp,
  PRIMARY KEY ("parameter_id", "location_id", "sensor_id", "created_at")
);

CREATE TABLE IF NOT EXISTS "dim_parameter" (
  "id" integer PRIMARY KEY,
  "name" varchar UNIQUE,
  "unit" varchar,
  "display_name" varchar,
  "description" varchar
);

CREATE TABLE IF NOT EXISTS "dim_location" (
  "id" integer PRIMARY KEY,
  "name" varchar,
  "city" varchar,
  "country_id" integer,
  "latitude" float,
  "longitude" float,
  "timezone" varchar
);

CREATE TABLE IF NOT EXISTS "dim_country" (
  "id" integer PRIMARY KEY,
  "code" varchar UNIQUE,
  "name" varchar
);

CREATE TABLE IF NOT EXISTS "dim_sensor" (
  "id" integer PRIMARY KEY,
  "name" varchar,
  "parameter_id" integer,
  "location_id" integer
);

ALTER TABLE "fact_air_quality" ADD FOREIGN KEY ("parameter_id") REFERENCES "dim_parameter" ("id");

ALTER TABLE "fact_air_quality" ADD FOREIGN KEY ("location_id") REFERENCES "dim_location" ("id");

ALTER TABLE "fact_air_quality" ADD FOREIGN KEY ("sensor_id") REFERENCES "dim_sensor" ("id");

ALTER TABLE "dim_location" ADD FOREIGN KEY ("country_id") REFERENCES "dim_country" ("id");

ALTER TABLE "dim_sensor" ADD FOREIGN KEY ("parameter_id") REFERENCES "dim_parameter" ("id");

ALTER TABLE "dim_sensor" ADD FOREIGN KEY ("location_id") REFERENCES "dim_location" ("id");

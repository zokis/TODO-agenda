BEGIN;
CREATE TABLE "agenda_calendarioevento_participantes" (
    "id" serial NOT NULL PRIMARY KEY,
    "calendarioevento_id" integer NOT NULL,
    "user_id" integer NOT NULL REFERENCES "core_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("calendarioevento_id", "user_id")
)
;
CREATE TABLE "agenda_calendarioevento" (
    "id" serial NOT NULL PRIMARY KEY,
    "nome" varchar(255) NOT NULL,
    "tipo" varchar(15) NOT NULL,
    "descricao" text NOT NULL,
    "inicio" timestamp with time zone NOT NULL,
    "fim" timestamp with time zone,
    "owner_id" integer REFERENCES "core_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "publico" boolean NOT NULL
)
;
ALTER TABLE "agenda_calendarioevento_participantes" ADD CONSTRAINT "calendarioevento_id_refs_id_887fbb1e" FOREIGN KEY ("calendarioevento_id") REFERENCES "agenda_calendarioevento" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE TABLE "agenda_departamento_funcionarios" (
    "id" serial NOT NULL PRIMARY KEY,
    "departamento_id" integer NOT NULL,
    "user_id" integer NOT NULL REFERENCES "core_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("departamento_id", "user_id")
)
;
CREATE TABLE "agenda_departamento" (
    "id" serial NOT NULL PRIMARY KEY,
    "nome" varchar(255) NOT NULL
)
;
ALTER TABLE "agenda_departamento_funcionarios" ADD CONSTRAINT "departamento_id_refs_id_f807a67f" FOREIGN KEY ("departamento_id") REFERENCES "agenda_departamento" ("id") DEFERRABLE INITIALLY DEFERRED;

COMMIT;


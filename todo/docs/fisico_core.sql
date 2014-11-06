BEGIN;
CREATE TABLE "core_user_groups" (
    "id" serial NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL,
    "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("user_id", "group_id")
)
;
CREATE TABLE "core_user_user_permissions" (
    "id" serial NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL,
    "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("user_id", "permission_id")
)
;
CREATE TABLE "core_user" (
    "id" serial NOT NULL PRIMARY KEY,
    "password" varchar(128) NOT NULL,
    "last_login" timestamp with time zone NOT NULL,
    "is_superuser" boolean NOT NULL,
    "email" varchar(75) NOT NULL UNIQUE,
    "nome" varchar(100) NOT NULL,
    "is_active" boolean NOT NULL,
    "is_staff" boolean NOT NULL,
    "date_joined" timestamp with time zone NOT NULL
)
;
ALTER TABLE "core_user_groups" ADD CONSTRAINT "user_id_refs_id_b61eb0a1" FOREIGN KEY ("user_id") REFERENCES "core_user" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "core_user_user_permissions" ADD CONSTRAINT "user_id_refs_id_6d90fe92" FOREIGN KEY ("user_id") REFERENCES "core_user" ("id") DEFERRABLE INITIALLY DEFERRED;

COMMIT;


-- A user of the application
CREATE TABLE "user" (
    "id" INTEGER PRIMARY KEY ASC,
    "username" TEXT NOT NULL,
    "hashed_password" TEXT NOT NULL,
    "can_su" INT DEFAULT 0,
    "can_manage_works" INT NOT NULL DEFAULT 0,
    "can_manage_techniques" INT NOT NULL DEFAULT 0
);

-- A technique that can be learned
CREATE TABLE "technique" (
    "id" INTEGER PRIMARY KEY ASC,
    "name" TEXT NOT NULL,
    "short_description" TEXT
);

-- Prerequisites for learning a technique
CREATE TABLE "technique_prereq" (
    "id" INTEGER PRIMARY KEY ASC,
    "technique_base_id" INTEGER NOT NULL,
    "technique_to_learn_id" INTEGER NOT NULL,
    FOREIGN KEY ("technique_base_id") REFERENCES "technique"("technique_id")
    FOREIGN KEY ("technique_to_learn_id") REFERENCES "technique"("technique_to_learn_id")
    -- Todo: Add uniquess constraint. Maybe remove primary key too.
);

-- A work that somebody might learn
CREATE TABLE "work" (
    "id" INTEGER PRIMARY KEY ASC,
    "name" TEXT NOT NULL
);

-- A link attached to a work
CREATE TABLE "work_link" (
    "id" INTEGER PRIMARY KEY ASC,
    -- For now - 1 for Affiliate, 2 for Stream
    "link_type" INTEGER NOT NULL,
    "href" TEXT NOT NULL,
    "work_id" INTEGER NOT NULL,
    FOREIGN KEY ("work_id") REFERENCES "work"("work_id")
    -- Todo: Add uniquess constraint. Maybe remove primary key too.
);

-- A required technique to perform a work
CREATE TABLE "work_technique" (
    "id" INTEGER PRIMARY KEY ASC,
    "work_id" INTEGER NOT NULL,
    "technique_id" INTEGER NOT NULL,
    FOREIGN KEY ("technique_id") REFERENCES "technique"("technique_id")
    FOREIGN KEY ("work_id") REFERENCES "work"("work_id")
    -- Todo: Add uniquess constraint. Maybe remove primary key too.
)

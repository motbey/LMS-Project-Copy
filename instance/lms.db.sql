BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "alembic_version" (
	"version_num"	VARCHAR(32) NOT NULL,
	CONSTRAINT "alembic_version_pkc" PRIMARY KEY("version_num")
);
CREATE TABLE IF NOT EXISTS "company" (
	"id"	INTEGER NOT NULL,
	"name"	VARCHAR(100) NOT NULL,
	PRIMARY KEY("id"),
	UNIQUE("name")
);
CREATE TABLE IF NOT EXISTS "forms" (
	"id"	INTEGER,
	"title"	TEXT NOT NULL,
	"description"	TEXT,
	"created_at"	TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	"fields"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "group_module" (
	"group_id"	INTEGER NOT NULL,
	"module_id"	INTEGER NOT NULL,
	"assigned_date"	TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	"required_completion_date"	DATE,
	"status"	TEXT DEFAULT 'Active',
	PRIMARY KEY("group_id","module_id"),
	FOREIGN KEY("group_id") REFERENCES "user_group"("id") ON DELETE CASCADE,
	FOREIGN KEY("module_id") REFERENCES "module"("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "group_qualification" (
	"group_id"	INTEGER NOT NULL,
	"qualification_id"	INTEGER NOT NULL,
	"assigned_date"	TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	"expiry_date"	DATE,
	"status"	TEXT DEFAULT 'Active',
	PRIMARY KEY("group_id","qualification_id"),
	FOREIGN KEY("group_id") REFERENCES "user_group"("id") ON DELETE CASCADE,
	FOREIGN KEY("qualification_id") REFERENCES "qualification"("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "job_title" (
	"id"	INTEGER,
	"name"	VARCHAR(100) NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "location" (
	"id"	INTEGER NOT NULL,
	"name"	VARCHAR(100) NOT NULL,
	PRIMARY KEY("id"),
	UNIQUE("name")
);
CREATE TABLE IF NOT EXISTS "module" (
	"id"	INTEGER NOT NULL,
	"name"	VARCHAR(150) NOT NULL,
	"file_name"	VARCHAR(150) NOT NULL,
	"created_at"	DATETIME,
	"status"	TEXT DEFAULT 'Active',
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "qualification" (
	"id"	INTEGER NOT NULL,
	"name"	VARCHAR(100) NOT NULL,
	"description"	TEXT,
	"valid_days"	INTEGER,
	PRIMARY KEY("id"),
	UNIQUE("name")
);
CREATE TABLE IF NOT EXISTS "user" (
	"id"	INTEGER,
	"first_name"	TEXT NOT NULL,
	"last_name"	TEXT NOT NULL,
	"email"	TEXT NOT NULL,
	"code"	TEXT,
	"password"	TEXT,
	"role"	TEXT,
	"status"	TEXT,
	"company_id"	INTEGER,
	"job_title_id"	INTEGER,
	PRIMARY KEY("id"),
	FOREIGN KEY("job_title_id") REFERENCES "job_title"("id")
);
CREATE TABLE IF NOT EXISTS "user_group" (
	"id"	INTEGER NOT NULL,
	"name"	VARCHAR(100) NOT NULL,
	"description"	TEXT,
	"created_at"	TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY("id" AUTOINCREMENT),
	UNIQUE("name")
);
CREATE TABLE IF NOT EXISTS "user_group_association" (
	"user_id"	INTEGER NOT NULL,
	"group_id"	INTEGER NOT NULL,
	PRIMARY KEY("user_id","group_id"),
	FOREIGN KEY("group_id") REFERENCES "user_group"("id") ON DELETE CASCADE,
	FOREIGN KEY("user_id") REFERENCES "user"("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "user_group_criteria" (
	"id"	INTEGER NOT NULL,
	"group_id"	INTEGER NOT NULL,
	"criteria_type"	TEXT NOT NULL CHECK("criteria_type" IN ('role', 'company', 'location', 'job_title', 'code')),
	"criteria_value"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("group_id") REFERENCES "user_group"("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "user_group_member" (
	"user_id"	INTEGER NOT NULL,
	"group_id"	INTEGER NOT NULL,
	PRIMARY KEY("user_id","group_id"),
	FOREIGN KEY("group_id") REFERENCES "user_group"("id") ON DELETE CASCADE,
	FOREIGN KEY("user_id") REFERENCES "user"("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "user_group_members" (
	"user_id"	INTEGER NOT NULL,
	"group_id"	INTEGER NOT NULL,
	PRIMARY KEY("user_id","group_id"),
	FOREIGN KEY("group_id") REFERENCES "user_groups"("id"),
	FOREIGN KEY("user_id") REFERENCES "user"("id")
);
CREATE TABLE IF NOT EXISTS "user_groups" (
	"id"	INTEGER,
	"name"	VARCHAR(100) NOT NULL,
	"description"	TEXT,
	"created_at"	DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "user_locations" (
	"user_id"	INTEGER NOT NULL,
	"location_id"	INTEGER NOT NULL,
	PRIMARY KEY("user_id","location_id"),
	FOREIGN KEY("location_id") REFERENCES "location"("id"),
	FOREIGN KEY("user_id") REFERENCES "user_old"("id")
);
INSERT INTO "alembic_version" VALUES ('ca7d279654fe');
INSERT INTO "company" VALUES (1,'ISS');
INSERT INTO "company" VALUES (2,'BGC');
INSERT INTO "forms" VALUES (1,'Sample Form','This is a sample form description','2025-01-13 05:28:00',NULL);
INSERT INTO "forms" VALUES (2,'Test 2 form','this is test 2','2025-01-13 05:38:02',NULL);
INSERT INTO "forms" VALUES (3,'test 3','this is test 3','2025-01-13 06:13:05',NULL);
INSERT INTO "forms" VALUES (4,'test 3','test 3','2025-01-13 06:18:21',NULL);
INSERT INTO "forms" VALUES (5,'Generated Form','["<p>Drag fields here to build your form.</p>", "<div class=\"\" data-type=\"text\" draggable=\"false\" style=\"\"><label>Text Field:</label> <input type=\"text\" name=\"text\"></div>", "<div class=\"\" data-type=\"file\" draggable=\"false\" style=\"\"><label>File Upload:</label> <input type=\"file\" name=\"file\"></div>"]','2025-01-13 06:19:16',NULL);
INSERT INTO "forms" VALUES (6,'Generated Form','["<p>Drag fields here to build your form.</p>", "<div class=\"\" data-type=\"text\" draggable=\"false\" style=\"\"><label>Text Field:</label> <input type=\"text\" name=\"text\"></div>", "<div class=\"\" data-type=\"file\" draggable=\"false\" style=\"\"><label>File Upload:</label> <input type=\"file\" name=\"file\"></div>"]','2025-01-13 06:19:58',NULL);
INSERT INTO "forms" VALUES (7,'test 3','test 3','2025-01-13 06:22:50',NULL);
INSERT INTO "forms" VALUES (8,'test 3','test 3','2025-01-13 06:28:04',NULL);
INSERT INTO "forms" VALUES (9,'test 3','test 3','2025-01-13 06:32:05',NULL);
INSERT INTO "forms" VALUES (10,'test 3','test 3','2025-01-13 06:34:00',NULL);
INSERT INTO "forms" VALUES (11,'test 3','test 3','2025-01-13 06:36:17',NULL);
INSERT INTO "forms" VALUES (12,'Test 6','this is test 6','2025-01-13 06:49:17',NULL);
INSERT INTO "forms" VALUES (13,'Generated Form','["<p class=\"placeholder\" style=\"display: none;\">Drag fields here to build your form.</p>", "<div class=\"form-element\" draggable=\"false\"><label>Text Field:</label> <input type=\"text\" name=\"text\"><button class=\"remove-btn\" onclick=\"removeElement(this)\">Remove</button></div>", "<div class=\"form-element\" draggable=\"false\"><label>Long Answer:</label> <textarea name=\"textarea\"></textarea><button class=\"remove-btn\" onclick=\"removeElement(this)\">Remove</button></div>", "<div class=\"form-element\" draggable=\"false\"><label>Date Picker:</label> <input type=\"date\" name=\"date\"><button class=\"remove-btn\" onclick=\"removeElement(this)\">Remove</button></div>", "<div class=\"form-element\" draggable=\"false\"><label>Checkbox:</label> <input type=\"checkbox\"><button class=\"remove-btn\" onclick=\"removeElement(this)\">Remove</button></div>"]','2025-01-13 06:50:08',NULL);
INSERT INTO "forms" VALUES (14,'Test 10','this is test 10','2025-01-13 07:04:28',NULL);
INSERT INTO "forms" VALUES (15,'test 10','','2025-01-13 07:05:13','["<p class=\"placeholder\" style=\"display: none;\">Drag fields here to build your form.</p>", "<div class=\"form-element\" draggable=\"false\"><label>Text Field:</label> <input type=\"text\" name=\"text\"><button class=\"remove-btn\" onclick=\"removeElement(this)\">Remove</button></div>", "<div class=\"form-element\" draggable=\"false\"><label>Long Answer:</label> <textarea name=\"textarea\"></textarea><button class=\"remove-btn\" onclick=\"removeElement(this)\">Remove</button></div>"]');
INSERT INTO "forms" VALUES (16,'test 10','','2025-01-13 07:26:40',NULL);
INSERT INTO "forms" VALUES (17,'test 10','','2025-01-13 07:41:20',NULL);
INSERT INTO "forms" VALUES (18,'test 11','','2025-01-13 08:01:07',NULL);
INSERT INTO "forms" VALUES (19,'test 11','','2025-01-13 08:11:30',NULL);
INSERT INTO "forms" VALUES (20,'test 11','','2025-01-13 08:16:30',NULL);
INSERT INTO "forms" VALUES (21,'test 11','','2025-01-13 08:17:04',NULL);
INSERT INTO "forms" VALUES (22,'test 11','','2025-01-13 08:32:10',NULL);
INSERT INTO "forms" VALUES (23,'test 11','','2025-01-13 08:34:07',NULL);
INSERT INTO "group_module" VALUES (2,2,'2025-01-14 06:53:38','2025-02-13','Active');
INSERT INTO "group_module" VALUES (1,2,'2025-01-16 10:36:12.109138',NULL,'Active');
INSERT INTO "group_qualification" VALUES (1,2,'2025-01-16 10:25:35.180331',NULL,'Active');
INSERT INTO "group_qualification" VALUES (1,1,'2025-01-16 10:36:40.244677',NULL,'Active');
INSERT INTO "job_title" VALUES (1,'Software Engineer');
INSERT INTO "job_title" VALUES (2,'Data Analyst');
INSERT INTO "job_title" VALUES (3,'Project Manager');
INSERT INTO "job_title" VALUES (4,'Cleaner');
INSERT INTO "job_title" VALUES (5,'Plummer');
INSERT INTO "job_title" VALUES (6,'Chef');
INSERT INTO "job_title" VALUES (7,'Kitchen Hand');
INSERT INTO "job_title" VALUES (8,'Driver');
INSERT INTO "location" VALUES (1,'Head Office');
INSERT INTO "location" VALUES (2,'Branch A');
INSERT INTO "location" VALUES (3,'Branch B');
INSERT INTO "location" VALUES (4,'Perth Office');
INSERT INTO "location" VALUES (5,'Sydney Office');
INSERT INTO "location" VALUES (6,'Darwin Office');
INSERT INTO "module" VALUES (2,'Fatigue Management','Test upload (2)','2025-01-10 09:57:32.088260','Active');
INSERT INTO "qualification" VALUES (1,'Forklift Licence ','',365);
INSERT INTO "qualification" VALUES (2,'C Class Driver''s Licence','This is to drive a car',730);
INSERT INTO "user" VALUES (1,'John','Doe','john.doe@example.com','CODE123','scrypt:32768:8:1$cnwXVf27ld78uau2$9b92eb842d04660bc43a06c4412161a6f8a1fb0dc2050948c8a0b26548f5fbfb75fa91eeb8ddd0fe6cba14f2bd14b55ef453ad06361876af8da7def4ec8e7f07','User','Active',1,2);
INSERT INTO "user" VALUES (2,'Alice','Johnson','alice.johnson@example.com','CODE123','scrypt:32768:8:1$tRw45QxIHzmTrGHf$78c7c15e3272cbe627a9d3e472d2a37f8a30fcc90d9ad6e987a3d12809477482e5fa9962cc0ce87d007295d218e592a4b944f366114d3883a9b7ccda9351b1af','User','Active',1,1);
INSERT INTO "user" VALUES (3,'Adam','Motbey','mail@mail.com','CODE123','scrypt:32768:8:1$Y8G4imYziisgUliC$732e2b2d009202a0fbe625bdeed3592acba85c1f446b2995c338cf2199085d4c23b3b6a6db992aefb9ac1f89a5de5846c79f9c3f274021edc3bdf4f7e8039a20','Admin','Active',1,5);
INSERT INTO "user" VALUES (4,'Billy','Bob','newuser@example.com','CODE123','scrypt:32768:8:1$mmxZznQYFSmZfCnN$450fedaa3eb35723ce20caaa3f7bc0003e35d89b215f7e129ead499ee577f075212767926916fb32847556745432c8725fe66319104875cb4381c521cdf7fad2','Security','Active',2,1);
INSERT INTO "user" VALUES (5,'Test1','User1','test1@example.com','123','pass123','User','Active',2,NULL);
INSERT INTO "user" VALUES (6,'Test2','User2','test2@example.com','123','pass123','User','Active',1,8);
INSERT INTO "user" VALUES (7,'Adam','Motbey','my@mail.com','test001','scrypt:32768:8:1$hmhYU7ZaV3U09Heq$46e35958c5521b2405d70b7e0bc80acea61479f72fcac690fd506bd4ff2bdac8e706444cbb89d7f2e99238e58ef15e3d546b7dfce10111227160f3d5c0bf4d81','User','Active',2,2);
INSERT INTO "user_group" VALUES (1,'Test Group','This is our first test group','2025-01-14 06:40:52');
INSERT INTO "user_group" VALUES (2,'Safety Team','Group for safety-related training and qualifications','2025-01-14 06:53:38');
INSERT INTO "user_group" VALUES (3,' test 1 new','words','2025-01-15 02:30:46.125692');
INSERT INTO "user_group" VALUES (5,'Test Admin Group','Group for testing admin role rules','2025-01-15 06:57:10.452701');
INSERT INTO "user_group" VALUES (6,'Test Company Location Group','Testing multiple rule types','2025-01-15 07:03:48.636507');
INSERT INTO "user_group" VALUES (7,'Drivers','All Drivers','2025-01-15 23:16:32.526894');
INSERT INTO "user_group_criteria" VALUES (37,6,'company','2');
INSERT INTO "user_group_criteria" VALUES (38,6,'location','2');
INSERT INTO "user_group_criteria" VALUES (43,7,'job_title','8');
INSERT INTO "user_group_criteria" VALUES (44,1,'role','User');
INSERT INTO "user_group_criteria" VALUES (45,1,'company','1');
INSERT INTO "user_group_criteria" VALUES (46,1,'job_title','2');
INSERT INTO "user_group_member" VALUES (6,7);
INSERT INTO "user_group_member" VALUES (1,1);
INSERT INTO "user_groups" VALUES (1,'Test Group','This is a test group created via debug route','2025-01-14 07:54:26.227768');
INSERT INTO "user_groups" VALUES (2,'Test group 5','this is a test user group','2025-01-14 08:17:07.447999');
INSERT INTO "user_locations" VALUES (5,4);
INSERT INTO "user_locations" VALUES (5,5);
INSERT INTO "user_locations" VALUES (1,4);
INSERT INTO "user_locations" VALUES (2,1);
INSERT INTO "user_locations" VALUES (2,2);
INSERT INTO "user_locations" VALUES (2,3);
INSERT INTO "user_locations" VALUES (4,1);
INSERT INTO "user_locations" VALUES (4,3);
INSERT INTO "user_locations" VALUES (7,4);
INSERT INTO "user_locations" VALUES (7,1);
CREATE INDEX IF NOT EXISTS "idx_group_module_group_id" ON "group_module" (
	"group_id"
);
CREATE INDEX IF NOT EXISTS "idx_group_module_module_id" ON "group_module" (
	"module_id"
);
CREATE INDEX IF NOT EXISTS "idx_group_qualification_group_id" ON "group_qualification" (
	"group_id"
);
CREATE INDEX IF NOT EXISTS "idx_group_qualification_qualification_id" ON "group_qualification" (
	"qualification_id"
);
CREATE INDEX IF NOT EXISTS "idx_user_group_association_group_id" ON "user_group_association" (
	"group_id"
);
CREATE INDEX IF NOT EXISTS "idx_user_group_association_user_id" ON "user_group_association" (
	"user_id"
);
COMMIT;

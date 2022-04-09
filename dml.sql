INSERT INTO "mainframe_machine"("uuid", "name")
VALUES (
    'd89647bf-ebdb-53c5-ae26-99d5256439c5',
    'Ground floor of A5'
  ),
  (
    '1a3de312-0360-577e-a316-3de66c157beb',
    'Dormitory'
  ),
  (
    'bc1bdab1-cf1c-554d-bcf3-f9ec16d00577',
    'Gate 1 machine 3'
  ),
  (
    '42020346-f4ab-51bc-b53c-b06791aef99d',
    'Gate 3 machine 2'
  );
INSERT INTO "mainframe_customuser"(
    "password",
    "rem_credit",
    "last_login",
    "is_superuser",
    "first_name",
    "last_name",
    "is_staff",
    "is_active",
    "uuid",
    "email",
    "phone",
    "date_joined",
    "date_updated"
  )
VALUES (
    'pbkdf2_sha256$260000$fdSBoXLCOb2v7yIK9eIKCD$bWbpj6GaYGiSnmtEYCzm6eYyA9TLmhnHKLBEu1cIoZM=',
    3000,
    null,
    False,
    'Hilda',
    'Ramirez',
    False,
    True,
    'b0343384-0152-4671-a7d6-c2122a65eab1',
    'hig@emovaw.za',
    '41276641',
    '2021-12-08 08:08:14.987748+00',
    '2021-12-08 08:08:14.987763+00'
  ),
  (
    'pbkdf2_sha256$320000$9dv7D43Jh7IwSDc9nhKFlk$5LGMNT46U66IPRuAJnDjv9N5/L1O/O6Kpd2uS6spfwE=',
    3000,
    null,
    False,
    'Ruth',
    'Curtis',
    False,
    True,
    'cfb11fd9-80a2-58c4-a669-ce7359b098cb',
    'metmir@uwedobi.tr',
    '43715432',
    '2022-02-08 08:08:14.987748+00',
    '2022-02-08 08:08:14.987763+00'
  );
INSERT INTO "mainframe_product"(
    "uuid",
    "image",
    "name",
    "unit",
    "price",
    "desc"
  )
VALUES (
    '6d9349b0-7877-5f44-a863-888e273c3ab0',
    '/products/coca.png',
    'Coca Cola',
    '330mL',
    60,
    'forty four tribe century situation degree pour husband party break particular next growth construction happen metal figure which vowel basic twice frequently globe concerned'
  ),
  (
    'ce602c59-de2e-5dfb-8841-02e1d719b1d4',
    '/products/cocalight.png',
    'Coca Light',
    '330mL',
    40,
    'born pole settlers case serve bill learn easily cold colony alone read building recall face love there dark fallen level relationship to book nodded'
  ),
  (
    'baf9c355-a040-5f07-a669-a92e6245bf3e',
    '/products/nutriboost.png',
    'NutriBoost',
    '297mL',
    30,
    'specific fat judge eye every spread forth concerned teeth electricity growth composed one caught price youth difference quarter locate tall gasoline slightly recall have'
  ),
  (
    '072c8269-eda2-5085-8d5f-4811e5adb80d',
    '/products/sting.png',
    'Sting',
    '330mL',
    35,
    'dot such additional want species butter corner soon middle heat contrast cover sign pig stuck include planning baby value trip running space valley exciting'
  ),
  (
    'ba50b773-0580-5da1-b4fa-56f01696a1cb',
    '/products/blackcoffee.png',
    'Black Coffee',
    '185mL',
    70,
    'race nest noun produce orange finally wrapped oldest fly vast report job wagon design possible equator without pick rest soap till closely science rhyme'
  ),
  (
    'e5fb8ff4-9520-5118-8195-290803e57460',
    '/products/dasani.png',
    'Dasani',
    '350mL',
    25,
    'factory coach indeed greatly past however evidence pitch slowly chapter off evening cannot wheat memory kill gas general arm health brother themselves environment catch'
  );
INSERT INTO "mainframe_order"(
    "uuid",
    "quantity",
    "order_id",
    "machine_id",
    "item_id",
    "user_id"
  )
VALUES (
    '761262f5-6deb-5aba-9599-01c67cf84d56',
    1,
    '2',
    null,
    (
      SELECT id
      FROM "mainframe_product"
      WHERE name = 'Dasani'
    ),
    (
      SELECT id
      FROM "mainframe_customuser"
      WHERE email = 'hig@emovaw.za'
    )
  ),
  (
    '50807864-db73-548e-b703-6a229d2f565f',
    1,
    '2',
    null,
    (
      SELECT id
      FROM "mainframe_product"
      WHERE name = 'Black Coffee'
    ),
    (
      SELECT id
      FROM "mainframe_customuser"
      WHERE email = 'hig@emovaw.za'
    )
  ),
  (
    '616b29d4-37b6-599a-b870-9c9be185b5a2',
    2,
    '2',
    null,
    (
      SELECT id
      FROM "mainframe_product"
      WHERE name = 'Sting'
    ),
    (
      SELECT id
      FROM "mainframe_customuser"
      WHERE email = 'hig@emovaw.za'
    )
  ),
  (
    '5d4b141d-ee40-54b1-89f8-203dbfa7b2d9',
    1,
    '420',
    null,
    (
      SELECT id
      FROM "mainframe_product"
      WHERE name = 'NutriBoost'
    ),
    (
      SELECT id
      FROM "mainframe_customuser"
      WHERE email = 'metmir@uwedobi.tr'
    )
  );
INSERT INTO "mainframe_producthistory" ("uuid", "quantity", "time_recorded")
VALUES (),
  ();

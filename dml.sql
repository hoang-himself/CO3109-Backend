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
    "credit",
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
    'pbkdf2_sha256$320000$sGt1oRWD5wh6c6gCnpIOzs$KRbBjBGH8BVNJKvw8uwLXddETf8ad8R2jIuUpyQKCAQ=',
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
    'pbkdf2_sha256$320000$tOKJn3HPYY36ymrp4VQdly$Gb9SqwAZ/NusiWPRxZ9nxxKu3wSZej6UzND01P+7lgA=',
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
INSERT INTO "mainframe_order"("uuid", "name", "user_id")
VALUES (
    '761262f5-6deb-5aba-9599-01c67cf84d56',
    'My order 1',
    (
      SELECT id
      FROM "mainframe_customuser"
      WHERE email = 'hig@emovaw.za'
    )
  ),
  (
    '50807864-db73-548e-b703-6a229d2f565f',
    'Not your order',
    (
      SELECT id
      FROM "mainframe_customuser"
      WHERE email = 'hig@emovaw.za'
    )
  ),
  (
    '616b29d4-37b6-599a-b870-9c9be185b5a2',
    'Unused order 69',
    (
      SELECT id
      FROM "mainframe_customuser"
      WHERE email = 'hig@emovaw.za'
    )
  ),
  (
    '5d4b141d-ee40-54b1-89f8-203dbfa7b2d9',
    'My future order',
    (
      SELECT id
      FROM "mainframe_customuser"
      WHERE email = 'metmir@uwedobi.tr'
    )
  );
INSERT INTO "mainframe_orderitem"(
    "uuid",
    "order_id",
    "item_id",
    "quantity"
  )
VALUES (
    'ef134134-f732-56d0-9dcc-5c38e7449269',
    (
      SELECT id
      FROM "mainframe_order"
      WHERE "uuid" = '761262f5-6deb-5aba-9599-01c67cf84d56'
    ),
    (
      SELECT id
      FROM "mainframe_product"
      WHERE "name" = 'Coca Cola'
    ),
    1
  ),
  (
    '0df24184-7272-5f4e-b83a-d2179475dbd6',
    (
      SELECT id
      FROM "mainframe_order"
      WHERE "uuid" = '761262f5-6deb-5aba-9599-01c67cf84d56'
    ),
    (
      SELECT id
      FROM "mainframe_product"
      WHERE "name" = 'Coca Light'
    ),
    3
  ),
  (
    '925ef48d-4c1a-5a72-afd3-8a123e11172f',
    (
      SELECT id
      FROM "mainframe_order"
      WHERE "uuid" = '50807864-db73-548e-b703-6a229d2f565f'
    ),
    (
      SELECT id
      FROM "mainframe_product"
      WHERE "name" = 'NutriBoost'
    ),
    4
  ),
  (
    'eb2d28f6-4ace-5b7a-ae6b-c81f167ff9e0',
    (
      SELECT id
      FROM "mainframe_order"
      WHERE "uuid" = '50807864-db73-548e-b703-6a229d2f565f'
    ),
    (
      SELECT id
      FROM "mainframe_product"
      WHERE "name" = 'Sting'
    ),
    2
  ),
  (
    '681187ba-5871-50f3-8f25-82546af3784a',
    (
      SELECT id
      FROM "mainframe_order"
      WHERE "uuid" = '616b29d4-37b6-599a-b870-9c9be185b5a2'
    ),
    (
      SELECT id
      FROM "mainframe_product"
      WHERE "name" = 'Black Coffee'
    ),
    7
  ),
  (
    '970e9007-6c35-5fc9-acc0-f0e6a6765048',
    (
      SELECT id
      FROM "mainframe_order"
      WHERE "uuid" = '616b29d4-37b6-599a-b870-9c9be185b5a2'
    ),
    (
      SELECT id
      FROM "mainframe_product"
      WHERE "name" = 'Dasani'
    ),
    6
  );
INSERT INTO "mainframe_orderqueue"("uuid", "machine_id", "order_id")
VALUES (
    'baaa78dd-dbd4-4a2a-b0bd-7a071178d76c',
    (
      SELECT id
      FROM "mainframe_machine"
      WHERE "name" = 'Ground floor of A5'
    ),
    (
      SELECT id
      FROM "mainframe_order"
      WHERE "uuid" = '761262f5-6deb-5aba-9599-01c67cf84d56'
    )
  ),
  (
    '8ae9cf49-d8f4-4948-9c1d-a2ad2f26d0e5',
    (
      SELECT id
      FROM "mainframe_machine"
      WHERE "name" = 'Ground floor of A5'
    ),
    (
      SELECT id
      FROM "mainframe_order"
      WHERE "uuid" = '50807864-db73-548e-b703-6a229d2f565f'
    )
  ),
  (
    '3de91ea0-7581-4fbd-b724-4d3459a90df3',
    (
      SELECT id
      FROM "mainframe_machine"
      WHERE "name" = 'Ground floor of A5'
    ),
    (
      SELECT id
      FROM "mainframe_order"
      WHERE "uuid" = '616b29d4-37b6-599a-b870-9c9be185b5a2'
    )
  );
INSERT INTO "mainframe_itemhistory"(
    "uuid",
    "user_id",
    "item_id",
    "quantity",
    "time"
  )
VALUES (
    'b9833be9-f686-5b71-8b68-99ff7badb5e6',
    (
      SELECT id
      FROM "mainframe_customuser"
      WHERE email = 'hig@emovaw.za'
    ),
    (
      SELECT id
      FROM "mainframe_product"
      WHERE "name" = 'Coca Cola'
    ),
    12,
    '2022-04-24 07:58:39.000000+00'
  ),
  (
    '0319746f-54c1-5680-b877-215af1ca9c46',
    (
      SELECT id
      FROM "mainframe_customuser"
      WHERE email = 'hig@emovaw.za'
    ),
    (
      SELECT id
      FROM "mainframe_product"
      WHERE "name" = 'Coca Light'
    ),
    2,
    '2022-04-20 13:26:39.000000+00'
  ),
  (
    'aa38faaa-26d5-5660-b4a2-5ac55e6dbb26',
    (
      SELECT id
      FROM "mainframe_customuser"
      WHERE email = 'hig@emovaw.za'
    ),
    (
      SELECT id
      FROM "mainframe_product"
      WHERE "name" = 'NutriBoost'
    ),
    9,
    '2022-04-16 09:06:20.000000+00'
  ),
  (
    '2e0eba40-0925-5bc1-ac44-97b157e4f11c',
    (
      SELECT id
      FROM "mainframe_customuser"
      WHERE email = 'hig@emovaw.za'
    ),
    (
      SELECT id
      FROM "mainframe_product"
      WHERE "name" = 'Sting'
    ),
    6,
    '2022-04-12 11:29:55.000000+00'
  ),
  (
    '4d043f07-7094-5333-9bbd-ab3bad36bf10',
    (
      SELECT id
      FROM "mainframe_customuser"
      WHERE email = 'hig@emovaw.za'
    ),
    (
      SELECT id
      FROM "mainframe_product"
      WHERE "name" = 'Black Coffee'
    ),
    10,
    '2022-04-08 16:10:01.000000+00'
  ),
  (
    '0680adc1-f38e-5891-86d8-519ff5ad16a6',
    (
      SELECT id
      FROM "mainframe_customuser"
      WHERE email = 'hig@emovaw.za'
    ),
    (
      SELECT id
      FROM "mainframe_product"
      WHERE "name" = 'Dasani'
    ),
    5,
    '2022-04-04 12:10:01.000000+00'
  );

CREATE TABLE product_product_variants
(
    id              SERIAL PRIMARY KEY,
    variant_id      integer NOT NULL,
    alt             text NULL,
    position        integer NULL,
    image_url       text NOT NULL,
    created_at      timestamp DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (variant_id)
        REFERENCES product_variants(id)
            ON DELETE CASCADE ON UPDATE CASCADE
);

ALTER TABLE product_variants ADD COLUMN image_url TEXT NULL;

ALTER TABLE products ADD COLUMN image_url TEXT NULL;

ALTER TABLE brands ADD COLUMN image_url TEXT NULL;

ALTER TABLE categories ADD COLUMN image_url TEXT NULL;

ALTER TABLE customers ADD COLUMN avatar_url TEXT NULL;
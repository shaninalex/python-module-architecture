CREATE TABLE brands
(
    id    SERIAL PRIMARY KEY,
    title varchar UNIQUE
);

CREATE TABLE categories
(
    id        SERIAL PRIMARY KEY,
    title     varchar(30) UNIQUE,
    parent_id bigint
);

CREATE OR REPLACE VIEW v_categories_tree AS
(
    SELECT
        c1.id,
        c1.title,
        parent.id    AS parent_id,
        parent.title AS parent_title
    FROM
        categories c1
    LEFT JOIN categories parent ON c1.parent_id = parent.id
    ORDER BY title
);

CREATE TABLE products
(
    id                SERIAL PRIMARY KEY,
    title             varchar NOT NULL UNIQUE,
    description       varchar,
    short_description varchar,
    created_at        timestamp DEFAULT now(),
    updated_at        timestamp
);

CREATE TABLE product_variants
(
    id          SERIAL PRIMARY KEY,
    product_id  bigint  NOT NULL,
    title       varchar NOT NULL,
    description varchar NULL,
    sku         varchar NULL UNIQUE,
    barcode     varchar NULL UNIQUE,
    created_at  timestamp DEFAULT now(),
    updated_at  timestamp,

    FOREIGN KEY (product_id)
        REFERENCES products(id)
        ON DELETE CASCADE
);


CREATE TABLE product_categories
(
    product_id  bigint NOT NULL,
    category_id bigint NOT NULL,

    UNIQUE(product_id, category_id),

    FOREIGN KEY (product_id)
        REFERENCES products(id)
        ON DELETE CASCADE,

    FOREIGN KEY (category_id)
        REFERENCES categories(id)
        ON DELETE CASCADE
);

CREATE TABLE product_brands
(
    product_id  bigint NOT NULL,
    brand_id    bigint NOT NULL,

    UNIQUE(product_id, brand_id),

    FOREIGN KEY (product_id)
        REFERENCES products(id)
        ON DELETE CASCADE,

    FOREIGN KEY (brand_id)
        REFERENCES brands(id)
        ON DELETE CASCADE
);

create table product_pricing
(
    id          SERIAL PRIMARY KEY,
    variant_id  bigint  NOT NULL,
    price       DECIMAL(19, 2) NOT NULL,

    UNIQUE (variant_id),

    FOREIGN KEY (variant_id)
        REFERENCES product_variants(id)
        ON DELETE CASCADE
);

CREATE TABLE customers
(
    id          SERIAL PRIMARY KEY,
    full_name   text     NOT NULL,
    email       text     NOT NULL,
    active      boolean DEFAULT FALSE,
    created_at  timestamp DEFAULT CURRENT_TIMESTAMP,
    updated_at  timestamp NULL,

    CONSTRAINT uni_identities_email UNIQUE (email)
);

CREATE TABLE customers_credentials
(
    id                  SERIAL PRIMARY KEY,
    customer_id         integer NOT NULL,
    provider            text    NOT NULL,
    provider_user_id    text,
    email               text,
    password_hash       text,
    created_at          timestamp DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (customer_id)
        REFERENCES customers(id)
            ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE customers_login_history
(
    id              SERIAL PRIMARY KEY,
    logged_in_at    timestamp DEFAULT CURRENT_TIMESTAMP,
    customer_id     integer NOT NULL,

    FOREIGN KEY (customer_id)
        REFERENCES customers(id)
            ON DELETE CASCADE ON UPDATE CASCADE
);
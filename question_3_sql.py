Q_3_sql = """
            WITH accounts_with_opening_dates AS (

            SELECT

                a.customer_no,
                a.account_no,
                a.product_type_code,
                a.account_status,
                c.bill_acct,

                CASE
                    WHEN c.open_date
                    THEN strptime(c.open_date, '%Y%m%d')
                    ELSE a.open_date
                END AS account_open_date,

            FROM account a

            LEFT JOIN credit_card_account c
            ON a.account_no ILIKE  '%' || c.card_no

            ),

            valid_accounts AS (

                SELECT

                    *

                FROM accounts_with_opening_dates

                WHERE (product_type_code = 'BUSS' AND bill_acct = 'Y')
                OR product_type_code IN ('CCRD')
                AND account_status != 'C'
            ),

            open_since_2018 AS (

                SELECT * FROM valid_accounts
                WHERE date_trunc('day', account_open_date) > '2018-07-01'
            ),            

            add_ages AS (

                SELECT 

                    o.customer_no,
                    c.age,

                FROM open_since_2018 o

                LEFT JOIN customer c
                ON c.customer_no = o.customer_no
            ),

            age_range AS (

                SELECT
                    age,
                    count(*) over() AS full_row_count
                FROM add_ages

            ),

            group_by_age AS (

                SELECT

                age,
                count(*) AS age_group_count,
                ANY_VALUE(full_row_count) AS total_count

                FROM age_range
                GROUP BY age
            )            

SELECT 

CASE WHEN age >= 18 AND age <= 29 THEN '18-29'
     WHEN age >= 30 AND age <= 44 THEN '30-44'
     WHEN age >= 45 AND age <= 59 THEN '45-59'
     WHEN age >= 60 THEN '60 +'
END AS 'Age Band',

ROUND(age_group_count / total_count * 100, 1) || '%'  AS '% with Credit Card'

FROM group_by_age

"""
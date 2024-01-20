Q_2_SQL = """
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
                OR product_type_code IN ('CCRD', 'TRAN', 'SAVG', 'HMLN')
                AND account_status != 'C'
            ),
            
            open_since_2018 AS (
            
                SELECT * FROM valid_accounts
                WHERE date_trunc('day', account_open_date) > '2018-07-01'

            ),
            
            no_trans_in_last_3_months AS (

                SELECT * FROM open_since_2018 o
            
                LEFT JOIN transactions t 
                ON o.account_no = t.account_no
                
                WHERE t.trans_date < CURRENT_DATE - INTERVAL '3 months'

            )
            
            SELECT DISTINCT(customer_no) FROM no_trans_in_last_3_months
"""